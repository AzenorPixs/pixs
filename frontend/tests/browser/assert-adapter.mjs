// Subset strict porte sur appels reels : ok/equal/notEqual/deepEqual/match/throws/rejects/fail + appel direct.
class AssertionError extends Error { constructor(m) { super(m); this.name = 'AssertionError'; } }
function fmt(v) { try { return JSON.stringify(v); } catch { return String(v); } }
function protoOf(v) { return Object.getPrototypeOf(v); }
function isPlain(v) { return v !== null && typeof v === 'object' && (protoOf(v) === Object.prototype || protoOf(v) === null); }
function deepEqual(a, b) {
  if (Object.is(a, b)) return true;
  if (typeof a === 'string' || typeof b === 'string' || typeof a === 'boolean' || typeof b === 'boolean' || typeof a === 'number' || typeof b === 'number') return false;
  if (a === null || b === null) return false;
  if (typeof a !== 'object' || typeof b !== 'object') return false;
  const aa = Array.isArray(a), bb = Array.isArray(b);
  if (aa !== bb) return false;
  if (aa) {
    if (protoOf(a) !== Array.prototype || protoOf(b) !== Array.prototype) return false;
    if (a.length !== b.length) return false;
    if (Reflect.ownKeys(a).length !== a.length + 1 || Reflect.ownKeys(b).length !== b.length + 1) return false;
    for (let i = 0; i < a.length; i++) { const da = Object.getOwnPropertyDescriptor(a, String(i)), db = Object.getOwnPropertyDescriptor(b, String(i)); if (!da || !db || !Object.hasOwn(da, 'value') || !Object.hasOwn(db, 'value')) return false; if (!deepEqual(da.value, db.value)) return false; }
    return true;
  }
  if (!isPlain(a) || !isPlain(b)) return false;
  if (protoOf(a) !== protoOf(b)) return false;
  const ka = Reflect.ownKeys(a), kb = Reflect.ownKeys(b);
  if (ka.length !== kb.length) return false;
  for (const k of ka) { if (typeof k !== 'string') return false; if (!Object.hasOwn(b, k)) return false; const da = Object.getOwnPropertyDescriptor(a, k), db = Object.getOwnPropertyDescriptor(b, k); if (!da || !db || !Object.hasOwn(da, 'value') || !Object.hasOwn(db, 'value')) return false; if (!deepEqual(da.value, db.value)) return false; }
  return true;
}
function checkThrow(e, exp) {
  if (exp === undefined) return;
  if (exp !== null && typeof exp === 'object' && !Array.isArray(exp) && Object.keys(exp).length === 1 && Object.hasOwn(exp, 'message') && typeof exp.message === 'string') { if (String(e?.message ?? e) !== exp.message) throw new AssertionError('Expected message ' + fmt(exp.message) + ' got ' + fmt(String(e?.message ?? e))); return; }
  if (exp instanceof RegExp) { if (typeof (e?.message ?? e) !== 'string' || !exp.test(String(e?.message ?? e))) throw new AssertionError('Expected ' + fmt(String(e?.message ?? e)) + ' to match ' + exp); return; }
  if (typeof exp === 'function') { let r; try { r = exp(e); } catch (err) { throw new AssertionError('Predicate threw'); } if (r !== true) throw new AssertionError('Predicate returned ' + fmt(r)); return; }
  throw new AssertionError('Unsupported throws expectation');
}
function assert(v, m) { if (!v) throw new AssertionError(m ?? 'Expected value to be truthy'); }
assert.ok = (v, m) => { if (!v) throw new AssertionError(m ?? 'Expected value to be truthy'); };
assert.equal = (a, b, m) => { if (!Object.is(a, b)) throw new AssertionError(m ?? ('Expected ' + fmt(a) + ' to equal ' + fmt(b))); };
assert.notEqual = (a, b, m) => { if (Object.is(a, b)) throw new AssertionError(m ?? ('Expected not equal ' + fmt(a))); };
assert.deepEqual = (a, b, m) => { if (!deepEqual(a, b)) throw new AssertionError(m ?? 'Expected values to be strictly deep-equal'); };
assert.match = (v, re, m) => { if (typeof v !== 'string' || !(re instanceof RegExp) || !re.test(v)) throw new AssertionError(m ?? ('Expected ' + fmt(v) + ' to match ' + re)); };
assert.fail = (m) => { throw new AssertionError(m ?? 'Failed'); };
assert.throws = (fn, exp, m) => { if (typeof fn !== 'function') throw new AssertionError('throws requires function'); let e, caught = false; try { fn(); } catch (err) { caught = true; e = err; } if (!caught) throw new AssertionError(m ?? 'Expected function to throw'); checkThrow(e, exp); };
assert.rejects = async (p, exp, m) => { let e, caught = false; try { await (typeof p === 'function' ? p() : p); } catch (err) { caught = true; e = err; } if (!caught) throw new AssertionError(m ?? 'Expected rejection'); checkThrow(e, exp); };
export default assert;
