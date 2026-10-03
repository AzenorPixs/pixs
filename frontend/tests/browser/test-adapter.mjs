// Collecteur de cas pour execution navigateur ; seule interface utilisee par shell.test.mjs.
export const cases = [];

export default function test(name, fn) {
  if (typeof name !== 'string' || name.trim() === '' || typeof fn !== 'function') {
    throw new Error('Invalid test registration');
  }
  if (cases.some(c => c.name === name)) {
    throw new Error(`Duplicate test registration: ${name}`);
  }
  cases.push({ name, fn });
}
