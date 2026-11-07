// Recettes des cinq éditeurs privés : vrai React, vrai DOM, ports explicites.
import test from 'node:test';
import assert from 'node:assert/strict';
import { createElement as h } from 'react';
import { createRoot } from 'react-dom/client';
import { flushSync } from 'react-dom';
import { createPresentationFields } from '../src/shell/presentation-fields-v1.js';

const context = () => ({ owner: 'acme.demo', id: 'acme.demo.page',
  limits: { maxDataNodes: 64 } });
const editor = () => createPresentationFields({
  label: key => key, text: key => key,
});
const node = (variant, more = {}) => ({
  kind: 'field', variant, children: [],
  props: { name: 'value', key: 'acme.demo.value', params: {}, required: false,
    initial: '', ...more },
});
const args = (more = {}) => ({
  id: 'field-value', formId: 'form-demo', disabled: false,
  maxTextLength: 1024, describedBy: 'field-help', modelKey: 'model-1', ...more,
});
function fixture(n, options = {}) {
  const api = editor(), ctx = options.context ?? context();
  const box = document.createElement('div');
  document.body.append(box);
  const root = createRoot(box);
  let current = n, currentArgs = args(options.args);
  function render(next = current, nextArgs = currentArgs) {
    current = next; currentArgs = nextArgs;
    flushSync(() => root.render(h('form', { id: 'form-demo' },
      api.field(current, currentArgs, ctx))));
  }
  try { render(); } catch (error) {
    flushSync(() => root.unmount()); box.remove(); throw error;
  }
  return {
    box, ctx, api, render,
    get form() { return box.querySelector('form'); },
    read() { return api.readFields(this.form, [current.props.name], ctx, { fields: [current] }); },
    close() { try { flushSync(() => root.unmount()); } finally { box.remove(); } },
  };
}
function click(element) {
  flushSync(() => element.click());
}
function change(element, value) {
  const prototype = element instanceof HTMLTextAreaElement
    ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
  Object.getOwnPropertyDescriptor(prototype, 'value').set.call(element, value);
  flushSync(() => element.dispatchEvent(new Event('input', { bubbles: true })));
}
const stringList = more => node('string-list', {
  initial: [], minItems: 0, maxItems: 3, itemRequired: false, ...more,
});
const columns = [
  { name: 'label', key: 'acme.demo.label', params: {}, required: true },
  { name: 'note', key: 'acme.demo.note', params: {}, required: false },
];

test('champs DOM : ports fermes et accesseurs jamais invoques', () => {
  for (const value of [null, {}, { label() {}, text() {}, extra: true }]) {
    assert.throws(() => createPresentationFields(value), /PRESENTATION_FIELDS_INVALID/);
  }
  let reads = 0;
  const value = { text() {} };
  Object.defineProperty(value, 'label', { enumerable: true,
    get() { reads++; return () => ''; } });
  assert.throws(() => createPresentationFields(value), /PRESENTATION_FIELDS_INVALID/);
  assert.equal(reads, 0);
});

test('champs DOM : texte natif libelle borne et valeur courante', () => {
  const f = fixture(node('text', { initial: 'avant', required: true }));
  try {
    const input = f.form.querySelector('input');
    assert.ok(input instanceof HTMLInputElement);
    assert.equal(input.type, 'text');
    assert.equal(input.id, 'field-value');
    assert.equal(input.getAttribute('aria-describedby'), 'field-help');
    assert.equal(input.required, true);
    assert.equal(input.maxLength, 1024);
    change(input, 'apres');
    assert.deepEqual(f.read(), { value: 'apres' });
    assert.equal(input.getAttribute('style'), null);
  } finally { f.close(); }
});

test('champs DOM : booleen false conserve puis true lu sans chaine', () => {
  const f = fixture(node('boolean', { initial: false }));
  try {
    const input = f.form.querySelector('input');
    assert.equal(input.type, 'checkbox');
    assert.deepEqual(f.read(), { value: false });
    click(input);
    assert.deepEqual(f.read(), { value: true });
    click(input);
    assert.deepEqual(f.read(), { value: false });
  } finally { f.close(); }
});

test('champs DOM : entier facultatif null et nombre avec bornes', () => {
  const f = fixture(node('integer', { initial: null, minimum: 1, maximum: 9 }));
  try {
    const input = f.form.querySelector('input');
    assert.equal(input.type, 'number');
    assert.equal(input.step, '1');
    assert.equal(input.min, '1'); assert.equal(input.max, '9');
    assert.deepEqual(f.read(), { value: null });
    change(input, '7');
    assert.deepEqual(f.read(), { value: 7 });
    change(input, '');
    assert.deepEqual(f.read(), { value: null });
  } finally { f.close(); }
});

test('champs DOM : liste preserve LF ordre doublons et copie', () => {
  const original = ['b\nc', 'a', 'a'];
  const f = fixture(stringList({ initial: original }));
  try {
    assert.deepEqual(f.read(), { value: original });
    const copy = f.read(); copy.value[0] = 'hors DOM';
    assert.deepEqual(f.read(), { value: original });
    const area = f.form.querySelector('textarea');
    assert.equal(area.maxLength, 1024);
    assert.ok(area.labels.length > 0);
    change(area, 'nouveau\ntexte');
    assert.deepEqual(f.read(), { value: ['nouveau\ntexte', 'a', 'a'] });
    assert.deepEqual(original, ['b\nc', 'a', 'a']);
  } finally { f.close(); }
});

test('champs DOM : enregistrements conservent colonnes LF et doublons', () => {
  const initial = [{ label: 'x', note: 'n\nm' }, { label: 'x', note: 'n\nm' }];
  const f = fixture(node('record-list', { initial, columns, minItems: 0, maxItems: 3 }));
  try {
    assert.equal(f.form.querySelectorAll('textarea').length, 4);
    assert.deepEqual(f.read(), { value: initial });
    const first = f.form.querySelector('textarea[data-column="label"]');
    assert.equal(first.required, true);
    change(first, 'z');
    assert.deepEqual(f.read(), { value: [{ label: 'z', note: 'n\nm' }, initial[1]] });
    click(f.form.querySelector('[data-pixs-add]'));
    assert.deepEqual(f.read().value[2], { label: '', note: '' });
    const copy = f.read(); copy.value[0].note = 'autre';
    assert.equal(f.read().value[0].note, 'n\nm');
  } finally { f.close(); }
});

test('champs DOM : ajout retrait respectent minimum maximum et disabled', () => {
  const f = fixture(stringList({ initial: ['a'], minItems: 1, maxItems: 2 }));
  try {
    let remove = f.form.querySelector('[data-pixs-row] button');
    assert.equal(remove.disabled, true);
    click(remove); assert.equal(f.read().value.length, 1);
    const add = () => f.form.querySelector('[data-pixs-add]');
    click(add()); assert.equal(f.read().value.length, 2);
    assert.equal(add().disabled, true, 'ajout courant desactive au maximum');
    click(add()); assert.equal(f.read().value.length, 2);
    remove = f.form.querySelectorAll('[data-pixs-row] button')[1];
    click(remove); assert.equal(f.read().value.length, 1);
    f.render(undefined, args({ disabled: true }));
    assert.equal(f.form.querySelector('textarea').disabled, true);
    assert.equal(f.form.querySelector('[data-pixs-add]').disabled, true);
    click(f.form.querySelector('[data-pixs-add]'));
    assert.equal(f.read().value.length, 1);
  } finally { f.close(); }
});

test('champs DOM : focus apres ajout retrait et retour au bouton', () => {
  const f = fixture(stringList());
  try {
    click(f.form.querySelector('[data-pixs-add]'));
    assert.equal(document.activeElement, f.form.querySelector('textarea'));
    click(f.form.querySelector('[data-pixs-add]'));
    assert.equal(document.activeElement, f.form.querySelectorAll('textarea')[1]);
    click(f.form.querySelectorAll('[data-pixs-row] button')[1]);
    assert.equal(document.activeElement, f.form.querySelector('textarea'));
    click(f.form.querySelector('[data-pixs-row] button'));
    assert.equal(document.activeElement, f.form.querySelector('[data-pixs-add]'));
  } finally { f.close(); }
});

test('champs DOM : modele stable garde brouillon puis nouvelle cle le purge', () => {
  const n = stringList(), f = fixture(n);
  try {
    click(f.form.querySelector('[data-pixs-add]'));
    change(f.form.querySelector('textarea'), 'brouillon');
    f.render(n);
    assert.deepEqual(f.read(), { value: ['brouillon'] });
    f.render(n, args({ modelKey: 'model-2' }));
    assert.deepEqual(f.read(), { value: [] });
  } finally { f.close(); }
});

test('champs DOM : deux proprietaires et modeles restent isoles', () => {
  const a = fixture(stringList({ initial: ['A'] }));
  const b = fixture(stringList({ initial: ['B'] }), {
    context: { ...context(), owner: 'acme.other', id: 'acme.other.page' },
    args: { id: 'other-value', formId: 'form-other', modelKey: 'other-model' },
  });
  try {
    click(a.form.querySelector('[data-pixs-add]'));
    assert.deepEqual(a.read(), { value: ['A', ''] });
    assert.deepEqual(b.read(), { value: ['B'] });
  } finally { a.close(); b.close(); }
});

test('champs DOM : lecteur refuse absent doublon colonne et budget', () => {
  const f = fixture(node('text', { initial: '' }));
  try {
    const clone = f.form.querySelector('input').cloneNode(true);
    f.form.append(clone);
    try { assert.throws(() => f.read(), /PRESENTATION_FIELDS_INVALID/); }
    finally { clone.remove(); }
    assert.throws(() => f.api.readFields(f.form, ['autre'], f.ctx,
      { fields: [node('text')] }), /PRESENTATION_FIELDS_INVALID/);
    assert.throws(() => f.api.readFields(null, ['value'], f.ctx,
      { fields: [node('text')] }), /PRESENTATION_FIELDS_INVALID/);
    assert.throws(() => f.api.readFields(f.form, ['value', 'value'], f.ctx,
      { fields: [node('text'), node('text')] }), /PRESENTATION_FIELDS_INVALID/);
  } finally { f.close(); }
  const list = fixture(stringList({ initial: ['a', 'b'] }),
    { context: { ...context(), limits: { maxDataNodes: 1 } } });
  try { assert.throws(() => list.read(), /PRESENTATION_FIELDS_INVALID/); }
  finally { list.close(); }
  const record = fixture(node('record-list', {
    initial: [{ label: 'x', note: '' }], columns, minItems: 0, maxItems: 2,
  }));
  try {
    const area = record.form.querySelector('textarea[data-column="label"]');
    const extra = area.cloneNode(true); area.parentElement.append(extra);
    try { assert.throws(() => record.read(), /PRESENTATION_FIELDS_INVALID/); }
    finally { extra.remove(); }
  } finally { record.close(); }
});

test('champs DOM : variantes fermees et signal badInput refuse explicitement', () => {
  const f = fixture(node('integer', {
    initial: 3, minimum: 1, maximum: 5, required: true,
  }));
  try {
    const input = f.form.querySelector('input');
    assert.equal(input.required, true);
    // Double local du seul signal validity ; ceci ne simule pas une frappe navigateur.
    Object.defineProperty(input, 'validity', { configurable: true, value: { badInput: true } });
    assert.throws(() => f.read(), /PRESENTATION_FIELDS_INVALID/);
    delete input.validity;
    assert.deepEqual(f.read(), { value: 3 });
    assert.throws(() => f.api.field(node('inconnu'), args(), f.ctx), /PRESENTATION_FIELDS_INVALID/);
  } finally { f.close(); }
});
