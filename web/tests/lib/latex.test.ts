import test from "node:test";
import assert from "node:assert/strict";
import { convertLatexDelimiters } from "../../lib/latex";

// ---------------------------------------------------------------------------
// Currency false positives: a bare `$` used as money must NOT become math.
// ---------------------------------------------------------------------------

test("currency: lone $ amounts are left untouched", () => {
  const input = "it costs $5 and $10";
  const result = convertLatexDelimiters(input);
  assert.equal(result, input);
  assert.ok(!result.includes("$$"), "must not introduce a math block");
});

test("currency: $ mixed with real \\(...\\) math", () => {
  const result = convertLatexDelimiters("pay $5 for \\(x\\) apples");
  // The explicit \( ... \) becomes inline math; the $5 stays as-is.
  assert.ok(result.includes("$x$"), "explicit math should convert");
  assert.ok(result.includes("$5"), "currency should survive");
});

// ---------------------------------------------------------------------------
// \[...\] spanning multiple newlines → $$...$$ block.
// ---------------------------------------------------------------------------

test("multiline \\[...\\] converts to a $$ block", () => {
  const input = "\\[\na = b\n+ c\n\\]";
  const result = convertLatexDelimiters(input);
  assert.ok(result.includes("$$"), "should produce a block delimiter");
  assert.ok(result.includes("a = b"), "content preserved");
  assert.ok(result.includes("+ c"), "later lines preserved");
  assert.ok(!result.includes("\\["), "opening delimiter removed");
  assert.ok(!result.includes("\\]"), "closing delimiter removed");
});

// ---------------------------------------------------------------------------
// Nested $$ \( ... \) $$ collapses to a single $$...$$.
// ---------------------------------------------------------------------------

test("nested $$ \\( ... \\) $$ collapses to a single block", () => {
  const result = convertLatexDelimiters("$$ \\(x^2\\) $$");
  assert.ok(result.includes("$$\nx^2\n$$"));
  assert.ok(!result.includes("\\("), "inner \\( removed");
  assert.ok(!result.includes("\\)"), "inner \\) removed");
});

// ---------------------------------------------------------------------------
// Plain text passes straight through.
// ---------------------------------------------------------------------------

test("plain text passthrough is unchanged", () => {
  const input = "Just a normal sentence with no math at all.";
  assert.equal(convertLatexDelimiters(input), input);
});
