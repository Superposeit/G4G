/**
 * Deterministic graph rendering support.
 *
 * Small local LLMs are bad at *drawing* graphs (ASCII art, ad-hoc SVG,
 * malformed mermaid). Instead we ask the model to emit a structured spec in a
 * ```graph fenced block and let the UI draw it. This module parses/validates
 * that spec and provides a *safe* math expression evaluator.
 *
 * SECURITY: `compileExpr` never uses `eval` or the `Function` constructor. It
 * tokenizes the expression, converts it to RPN via the shunting-yard algorithm
 * and evaluates that RPN over a numeric stack. Anything that is not a
 * recognised number/variable/operator/function is rejected with a clear Error.
 */

export interface GraphFunctionSpec {
  expr: string;
  label?: string;
}

export interface GraphPointSpec {
  x: number;
  y: number;
  label?: string;
}

export interface GraphSpec {
  functions?: GraphFunctionSpec[];
  domain?: [number, number];
  range?: [number, number];
  samples?: number;
  points?: GraphPointSpec[];
  title?: string;
  xLabel?: string;
  yLabel?: string;
}

// ---------------------------------------------------------------------------
// Safe expression evaluator
// ---------------------------------------------------------------------------

const CONSTANTS: Record<string, number> = {
  pi: Math.PI,
  e: Math.E,
};

const FUNCTIONS: Record<string, (value: number) => number> = {
  sin: Math.sin,
  cos: Math.cos,
  tan: Math.tan,
  asin: Math.asin,
  acos: Math.acos,
  atan: Math.atan,
  sqrt: Math.sqrt,
  abs: Math.abs,
  log: Math.log10,
  ln: Math.log,
  exp: Math.exp,
  floor: Math.floor,
  ceil: Math.ceil,
  round: Math.round,
};

type BinaryOp = "+" | "-" | "*" | "/" | "^";
type OpSymbol = BinaryOp | "u-";

type Token =
  | { type: "num"; value: number }
  | { type: "var" }
  | { type: "op"; op: OpSymbol }
  | { type: "func"; name: string }
  | { type: "lparen" }
  | { type: "rparen" };

function isDigit(ch: string): boolean {
  return ch >= "0" && ch <= "9";
}

function isAlpha(ch: string): boolean {
  return (ch >= "a" && ch <= "z") || (ch >= "A" && ch <= "Z");
}

function tokenize(input: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;

  const previous = (): Token | undefined => tokens[tokens.length - 1];

  while (i < input.length) {
    const ch = input[i];

    if (ch === " " || ch === "\t" || ch === "\n" || ch === "\r") {
      i += 1;
      continue;
    }

    // Number literal (supports leading-dot form like `.5`).
    if (isDigit(ch) || (ch === "." && isDigit(input[i + 1] ?? ""))) {
      let j = i + 1;
      while (j < input.length && (isDigit(input[j]) || input[j] === ".")) {
        j += 1;
      }
      const numStr = input.slice(i, j);
      if ((numStr.match(/\./g)?.length ?? 0) > 1) {
        throw new Error(`Invalid number "${numStr}"`);
      }
      const value = Number(numStr);
      if (!Number.isFinite(value)) {
        throw new Error(`Invalid number "${numStr}"`);
      }
      tokens.push({ type: "num", value });
      i = j;
      continue;
    }

    // Identifier: variable `x`, a constant, or a function name.
    if (isAlpha(ch)) {
      let j = i + 1;
      while (j < input.length && (isAlpha(input[j]) || isDigit(input[j]))) {
        j += 1;
      }
      const name = input.slice(i, j).toLowerCase();
      i = j;

      if (name === "x") {
        tokens.push({ type: "var" });
      } else if (name in CONSTANTS) {
        tokens.push({ type: "num", value: CONSTANTS[name] });
      } else if (name in FUNCTIONS) {
        tokens.push({ type: "func", name });
      } else {
        throw new Error(`Unknown identifier "${name}"`);
      }
      continue;
    }

    if (ch === "(") {
      tokens.push({ type: "lparen" });
      i += 1;
      continue;
    }

    if (ch === ")") {
      tokens.push({ type: "rparen" });
      i += 1;
      continue;
    }

    if (ch === "+" || ch === "-" || ch === "*" || ch === "/" || ch === "^") {
      i += 1;
      const prev = previous();
      // A `+`/`-` is unary when it starts the expression or follows another
      // operator, an opening paren, or a function name.
      const unaryContext =
        !prev ||
        prev.type === "op" ||
        prev.type === "lparen" ||
        prev.type === "func";

      if (ch === "+" && unaryContext) {
        // Unary plus is a no-op; drop it.
        continue;
      }
      if (ch === "-" && unaryContext) {
        tokens.push({ type: "op", op: "u-" });
        continue;
      }
      tokens.push({ type: "op", op: ch });
      continue;
    }

    throw new Error(`Unexpected character "${ch}"`);
  }

  return tokens;
}

function precedence(op: OpSymbol): number {
  switch (op) {
    case "+":
    case "-":
      return 2;
    case "*":
    case "/":
      return 3;
    case "u-":
      return 4;
    case "^":
      return 5;
  }
}

function isRightAssociative(op: OpSymbol): boolean {
  // `^` and unary minus bind right-to-left. Keeping unary minus below `^`
  // means `-2^2` parses as `-(2^2)` (the common math convention).
  return op === "^" || op === "u-";
}

function toRpn(tokens: Token[]): Token[] {
  const output: Token[] = [];
  const stack: Token[] = [];

  for (const token of tokens) {
    switch (token.type) {
      case "num":
      case "var":
        output.push(token);
        break;
      case "func":
        stack.push(token);
        break;
      case "op": {
        // Prefix unary minus is pushed directly: nothing to its left binds to
        // it, so it must not pop higher-precedence operators (e.g. in `2^-2`).
        if (token.op === "u-") {
          stack.push(token);
          break;
        }
        while (stack.length > 0) {
          const top = stack[stack.length - 1];
          if (top.type === "op") {
            const topPrec = precedence(top.op);
            const curPrec = precedence(token.op);
            if (
              topPrec > curPrec ||
              (topPrec === curPrec && !isRightAssociative(token.op))
            ) {
              output.push(stack.pop() as Token);
              continue;
            }
          } else if (top.type === "func") {
            output.push(stack.pop() as Token);
            continue;
          }
          break;
        }
        stack.push(token);
        break;
      }
      case "lparen":
        stack.push(token);
        break;
      case "rparen": {
        let matched = false;
        while (stack.length > 0) {
          const top = stack.pop() as Token;
          if (top.type === "lparen") {
            matched = true;
            break;
          }
          output.push(top);
        }
        if (!matched) {
          throw new Error("Mismatched parentheses");
        }
        const top = stack[stack.length - 1];
        if (top && top.type === "func") {
          output.push(stack.pop() as Token);
        }
        break;
      }
    }
  }

  while (stack.length > 0) {
    const top = stack.pop() as Token;
    if (top.type === "lparen" || top.type === "rparen") {
      throw new Error("Mismatched parentheses");
    }
    output.push(top);
  }

  return output;
}

function evalRpn(rpn: Token[], x: number): number {
  const stack: number[] = [];

  for (const token of rpn) {
    if (token.type === "num") {
      stack.push(token.value);
    } else if (token.type === "var") {
      stack.push(x);
    } else if (token.type === "func") {
      if (stack.length < 1) {
        throw new Error("Invalid expression");
      }
      const a = stack.pop() as number;
      stack.push(FUNCTIONS[token.name](a));
    } else if (token.type === "op") {
      if (token.op === "u-") {
        if (stack.length < 1) {
          throw new Error("Invalid expression");
        }
        stack.push(-(stack.pop() as number));
        continue;
      }
      if (stack.length < 2) {
        throw new Error("Invalid expression");
      }
      const b = stack.pop() as number;
      const a = stack.pop() as number;
      switch (token.op) {
        case "+":
          stack.push(a + b);
          break;
        case "-":
          stack.push(a - b);
          break;
        case "*":
          stack.push(a * b);
          break;
        case "/":
          stack.push(a / b);
          break;
        case "^":
          stack.push(Math.pow(a, b));
          break;
      }
    }
  }

  if (stack.length !== 1) {
    throw new Error("Invalid expression");
  }
  return stack[0];
}

/**
 * Compile a math expression in `x` into a safe evaluator function.
 * Throws a clear Error for anything malformed or unsupported. Never uses
 * `eval` or the `Function` constructor.
 */
export function compileExpr(expr: string): (x: number) => number {
  if (typeof expr !== "string" || expr.trim() === "") {
    throw new Error("Empty expression");
  }

  const tokens = tokenize(expr);
  if (tokens.length === 0) {
    throw new Error("Empty expression");
  }

  const rpn = toRpn(tokens);

  // Validate structure once so malformed expressions (dangling operators,
  // missing operands, etc.) fail here rather than silently at draw time.
  evalRpn(rpn, 0);

  return (x: number) => evalRpn(rpn, x);
}

// ---------------------------------------------------------------------------
// Spec parsing / validation
// ---------------------------------------------------------------------------

function isFiniteNumber(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

function validatePair(value: unknown, name: string): [number, number] {
  if (
    !Array.isArray(value) ||
    value.length !== 2 ||
    !isFiniteNumber(value[0]) ||
    !isFiniteNumber(value[1])
  ) {
    throw new Error(`"${name}" must be a [min, max] pair of finite numbers`);
  }
  if (value[0] === value[1]) {
    throw new Error(`"${name}" min and max must differ`);
  }
  return value[0] < value[1] ? [value[0], value[1]] : [value[1], value[0]];
}

/**
 * Parse and validate the JSON body of a ```graph fenced block.
 * Returns `{ spec }` on success or `{ error }` on any problem so the caller can
 * surface a message without the renderer ever throwing.
 */
export function parseGraphSpec(
  source: string,
): { spec: GraphSpec } | { error: string } {
  let raw: unknown;
  try {
    raw = JSON.parse(source);
  } catch (err) {
    return { error: `Invalid graph JSON: ${(err as Error).message}` };
  }

  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) {
    return { error: "Graph spec must be a JSON object" };
  }

  try {
    const obj = raw as Record<string, unknown>;
    const spec: GraphSpec = {};

    if (obj.functions !== undefined) {
      if (!Array.isArray(obj.functions)) {
        throw new Error(`"functions" must be an array`);
      }
      spec.functions = obj.functions.map((entry, idx) => {
        if (typeof entry !== "object" || entry === null) {
          throw new Error(`functions[${idx}] must be an object`);
        }
        const fn = entry as Record<string, unknown>;
        if (typeof fn.expr !== "string" || fn.expr.trim() === "") {
          throw new Error(`functions[${idx}].expr must be a non-empty string`);
        }
        // Surface expression errors here so bad specs become an error string.
        compileExpr(fn.expr);
        const out: GraphFunctionSpec = { expr: fn.expr };
        if (fn.label !== undefined) {
          if (typeof fn.label !== "string") {
            throw new Error(`functions[${idx}].label must be a string`);
          }
          out.label = fn.label;
        }
        return out;
      });
    }

    if (obj.domain !== undefined) {
      spec.domain = validatePair(obj.domain, "domain");
    }

    if (obj.range !== undefined) {
      spec.range = validatePair(obj.range, "range");
    }

    if (obj.samples !== undefined) {
      if (!isFiniteNumber(obj.samples) || obj.samples < 2) {
        throw new Error(`"samples" must be a number >= 2`);
      }
      spec.samples = Math.min(Math.floor(obj.samples), 5000);
    }

    if (obj.points !== undefined) {
      if (!Array.isArray(obj.points)) {
        throw new Error(`"points" must be an array`);
      }
      spec.points = obj.points.map((entry, idx) => {
        if (typeof entry !== "object" || entry === null) {
          throw new Error(`points[${idx}] must be an object`);
        }
        const pt = entry as Record<string, unknown>;
        if (!isFiniteNumber(pt.x) || !isFiniteNumber(pt.y)) {
          throw new Error(`points[${idx}] must have finite x and y`);
        }
        const out: GraphPointSpec = { x: pt.x, y: pt.y };
        if (pt.label !== undefined) {
          if (typeof pt.label !== "string") {
            throw new Error(`points[${idx}].label must be a string`);
          }
          out.label = pt.label;
        }
        return out;
      });
    }

    for (const key of ["title", "xLabel", "yLabel"] as const) {
      const value = obj[key];
      if (value !== undefined) {
        if (typeof value !== "string") {
          throw new Error(`"${key}" must be a string`);
        }
        spec[key] = value;
      }
    }

    const hasFunctions = !!spec.functions && spec.functions.length > 0;
    const hasPoints = !!spec.points && spec.points.length > 0;
    if (!hasFunctions && !hasPoints) {
      throw new Error("Graph spec must include at least one function or point");
    }

    return { spec };
  } catch (err) {
    return { error: (err as Error).message };
  }
}
