import test from "node:test";
import assert from "node:assert/strict";
import { parseGraphSpec, compileExpr } from "../../lib/graph-spec";

const approx = (actual: number, expected: number, eps = 1e-9) =>
  assert.ok(
    Math.abs(actual - expected) < eps,
    `expected ${actual} ≈ ${expected}`,
  );

// ---------------------------------------------------------------------------
// parseGraphSpec
// ---------------------------------------------------------------------------

test("parseGraphSpec: valid spec parses", () => {
  const res = parseGraphSpec(
    JSON.stringify({
      functions: [{ expr: "x^2", label: "parabola" }],
      domain: [-5, 5],
      samples: 100,
      title: "Quadratic",
    }),
  );
  assert.ok("spec" in res);
  if ("spec" in res) {
    assert.equal(res.spec.functions?.length, 1);
    assert.equal(res.spec.functions?.[0].expr, "x^2");
    assert.equal(res.spec.functions?.[0].label, "parabola");
    assert.deepEqual(res.spec.domain, [-5, 5]);
    assert.equal(res.spec.samples, 100);
    assert.equal(res.spec.title, "Quadratic");
  }
});

test("parseGraphSpec: points-only spec parses", () => {
  const res = parseGraphSpec(
    JSON.stringify({ points: [{ x: 1, y: 2, label: "A" }] }),
  );
  assert.ok("spec" in res);
});

test("parseGraphSpec: malformed JSON → error", () => {
  const res = parseGraphSpec("{ not valid json ");
  assert.ok("error" in res);
});

test("parseGraphSpec: non-object JSON → error", () => {
  assert.ok("error" in parseGraphSpec("[1, 2, 3]"));
  assert.ok("error" in parseGraphSpec("42"));
});

test("parseGraphSpec: empty spec (no functions or points) → error", () => {
  assert.ok("error" in parseGraphSpec("{}"));
});

test("parseGraphSpec: invalid expression → error (not thrown)", () => {
  const res = parseGraphSpec(
    JSON.stringify({ functions: [{ expr: "x; process.exit(1)" }] }),
  );
  assert.ok("error" in res);
});

test("parseGraphSpec: bad domain pair → error", () => {
  assert.ok(
    "error" in
      parseGraphSpec(JSON.stringify({ functions: [{ expr: "x" }], domain: [1] })),
  );
});

// ---------------------------------------------------------------------------
// compileExpr — evaluation
// ---------------------------------------------------------------------------

test("compileExpr: x^2", () => {
  const f = compileExpr("x^2");
  assert.equal(f(3), 9);
  assert.equal(f(-2), 4);
  assert.equal(f(0), 0);
});

test("compileExpr: sin(x)", () => {
  const f = compileExpr("sin(x)");
  approx(f(0), 0);
  approx(f(Math.PI / 2), 1);
});

test("compileExpr: 2*x+1", () => {
  const f = compileExpr("2*x+1");
  assert.equal(f(0), 1);
  assert.equal(f(3), 7);
  assert.equal(f(-2), -3);
});

test("compileExpr: sqrt(abs(x))", () => {
  const f = compileExpr("sqrt(abs(x))");
  assert.equal(f(-9), 3);
  assert.equal(f(16), 4);
});

test("compileExpr: constants pi and e", () => {
  approx(compileExpr("pi")(0), Math.PI);
  approx(compileExpr("e")(0), Math.E);
  approx(compileExpr("2*pi")(0), 2 * Math.PI);
});

test("compileExpr: nested functions and constants", () => {
  approx(compileExpr("cos(pi)")(0), -1);
  approx(compileExpr("ln(e)")(0), 1);
  approx(compileExpr("log(1000)")(0), 3);
});

// ---------------------------------------------------------------------------
// compileExpr — security: no eval / no Function
// ---------------------------------------------------------------------------

test("compileExpr: rejects statement injection", () => {
  assert.throws(() => compileExpr("x; process.exit(1)"));
});

test("compileExpr: rejects IIFE / Function injection", () => {
  assert.throws(() => compileExpr("(function(){})()"));
  assert.throws(() => compileExpr("process.exit(1)"));
  assert.throws(() => compileExpr("globalThis"));
});

test("compileExpr: rejects unknown identifiers and stray symbols", () => {
  assert.throws(() => compileExpr("y + 1"));
  assert.throws(() => compileExpr("x & 1"));
  assert.throws(() => compileExpr(""));
});

test("compileExpr: rejects malformed expressions", () => {
  assert.throws(() => compileExpr("x +"));
  assert.throws(() => compileExpr("(x"));
  assert.throws(() => compileExpr("x)"));
  assert.throws(() => compileExpr("2 x"));
});

// ---------------------------------------------------------------------------
// compileExpr — precedence and unary minus
// ---------------------------------------------------------------------------

test("compileExpr: operator precedence", () => {
  assert.equal(compileExpr("1+2*3")(0), 7);
  assert.equal(compileExpr("(1+2)*3")(0), 9);
  assert.equal(compileExpr("2*3+4")(0), 10);
  assert.equal(compileExpr("8/2/2")(0), 2); // left-assoc
});

test("compileExpr: exponent is right-associative", () => {
  assert.equal(compileExpr("2^3^2")(0), 512); // 2^(3^2)
});

test("compileExpr: unary minus", () => {
  assert.equal(compileExpr("-3+5")(0), 2);
  assert.equal(compileExpr("2*-3")(0), -6);
  assert.equal(compileExpr("-2^2")(0), -4); // -(2^2) math convention
  approx(compileExpr("2^-2")(0), 0.25); // 2^(-2)
  assert.equal(compileExpr("--3")(0), 3);
});
