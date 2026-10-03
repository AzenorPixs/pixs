// Subset strict de node:assert/strict limite aux methodes reellement utilisees.
class AssertionError extends Error {
  constructor(message) { super(message); this.name = 'AssertionError'; }
}

// Strict : primitives via Object.is ; tableaux reellement utilises compares
// en longueur puis element par element avec Object.is. Ni [] ni {} ne sont
// assimiles a un autre type ; tout autre type non couvert est inegal.
function deepEqual(a, b) {
  if (Object.is(a, b)) return true;
  if (Array.isArray(a) && Array.isArray(b)) {
    if (Object.getPrototypeOf(a) !== Object.getPrototypeOf(b) || a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) {
      if (Object.hasOwn(a, i) !== Object.hasOwn(b, i)) return false;
      if (Object.hasOwn(a, i) && !Object.is(a[i], b[i])) return false;
    }
    return true;
  }
  return false;
}

function fmt(value) { try { return JSON.stringify(value); } catch { return String(value); } }

const assert = {
  ok(value, message) {
    if (!value) throw new AssertionError(message ?? 'Expected value to be truthy');
  },
  equal(actual, expected, message) {
    if (!Object.is(actual, expected)) throw new AssertionError(message ?? `Expected ${fmt(actual)} to equal ${fmt(expected)}`);
  },
  deepEqual(actual, expected, message) {
    if (!deepEqual(actual, expected)) throw new AssertionError(message ?? 'Expected values to be strictly deep-equal');
  },
  match(value, regexp, message) {
    if (typeof value !== 'string' || !regexp.test(value)) throw new AssertionError(message ?? `Expected ${fmt(value)} to match ${regexp}`);
  },
  throws(fn, expectation, message) {
    if (typeof fn !== 'function') throw new AssertionError('throws requires a function callback');
    if (expectation === null || typeof expectation !== 'object' ||
        Object.keys(expectation).length !== 1 || !Object.hasOwn(expectation, 'message') ||
        typeof expectation.message !== 'string') {
      throw new AssertionError('Unsupported throws expectation; expected {message:string}');
    }
    const want = expectation.message;
    let caught; let threw = false;
    try { fn(); } catch (e) { threw = true; caught = e; }
    if (!threw) throw new AssertionError(message ?? 'Expected function to throw');
    if (want !== undefined && String(caught?.message ?? caught) !== want) {
      throw new AssertionError(message ?? `Expected error message "${want}", got "${caught?.message}"`);
    }
  },
};

export default assert;
