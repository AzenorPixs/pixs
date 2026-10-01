import test from 'node:test';
import assert from 'node:assert/strict';
import { catalogs, createCatalogs, resolveLocale } from '../src/catalogs.js';

test('canonical and French catalogues are complete, immutable and namespaced', () => {
  assert.deepEqual(Object.keys(catalogs.en), Object.keys(catalogs.fr));
  assert.ok(Object.keys(catalogs.en).length > 0);
  for (const language of ['en', 'fr']) {
    assert.ok(Object.isFrozen(catalogs[language]));
    for (const [key, value] of Object.entries(catalogs[language])) {
      assert.match(key, /^shell\.[a-zA-Z]+$/);
      assert.equal(typeof value, 'string');
      assert.ok(value.trim().length > 0);
    }
  }
});

test('catalogue rejects duplicate, missing and invalid translations', () => {
  const invalid = [
    [], null, {},
    [['shell.title', 'Title']],
    [['shell.title', '', 'Titre']],
    [['shell.title', 'Title', '  ']],
    [['shell.title', 'Title', null]],
    [['other.title', 'Title', 'Titre']],
    [['shell.title', 'Title', 'Titre'], ['shell.title', 'Other', 'Autre']],
    [['shell.title', 'Title', 'Titre', 'extra']],
  ];
  for (const source of invalid) {
    assert.throws(() => createCatalogs(source), { message: 'Invalid shell catalogue' });
  }
});

test('locale follows the first supported preference, then explicit fallback', () => {
  assert.equal(resolveLocale(['de-DE', 'fr-CA', 'en-US']), 'fr');
  assert.equal(resolveLocale(['EN-gb', 'fr']), 'en');
  assert.equal(resolveLocale(['ar', 'de']), 'en');
  assert.equal(resolveLocale([], 'fr'), 'fr');
  assert.equal(resolveLocale([null, 42, 'fr-FR']), 'fr');
  assert.equal(resolveLocale(['__proto__', 'constructor']), 'en');
  assert.throws(() => resolveLocale([], '__proto__'), { message: 'Invalid shell locale' });
  assert.throws(() => resolveLocale('fr'), { message: 'Invalid shell locale' });
});
