// Éditeurs privés React ; les contributions ne reçoivent que des valeurs typées.
import { createElement as h, useState, useRef, useEffect } from 'react';

function fail() { throw new Error('PRESENTATION_FIELDS_INVALID'); }
function ports(value) {
  if (value === null || typeof value !== 'object'
      || ![Object.prototype, null].includes(Object.getPrototypeOf(value))) fail();
  const keys = Reflect.ownKeys(value);
  if (keys.length !== 2 || !keys.includes('label') || !keys.includes('text')) fail();
  for (const key of keys) {
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (!descriptor || !Object.hasOwn(descriptor, 'value') || typeof descriptor.value !== 'function') fail();
  }
  return Object.freeze({ label: value.label, text: value.text });
}
export function createPresentationFields(options) {
  const p = ports(options);
  function ListEditor({ node, args, context }) {
    const initial = node.props.initial;
    const [rows, setRows] = useState(() => initial.map((value, index) => ({ key: index, value })));
    const nextKey = useRef(initial.length);
    const root = useRef(null), pendingFocus = useRef(null);
    useEffect(() => {
      if (pendingFocus.current === null || root.current === null) return;
      const key = pendingFocus.current; pendingFocus.current = null;
      const row = [...root.current.querySelectorAll('[data-pixs-row]')]
        .find(element => element.getAttribute('data-pixs-row') === String(key));
      const target = row?.querySelector('textarea') ?? root.current.querySelector('[data-pixs-add]');
      target?.focus();
    }, [rows]);
    const maximum = Math.min(node.props.maxItems ?? context.limits.maxDataNodes, context.limits.maxDataNodes);
    const columns = node.variant === 'record-list' ? node.props.columns : null;
    const update = (key, column, value) => setRows(previous => previous.map(row => {
      if (row.key !== key) return row;
      return { key, value: columns === null ? value : { ...row.value, [column]: value } };
    }));
    const remove = key => {
      if (args.disabled || rows.length <= node.props.minItems) return;
      setRows(previous => {
        const remaining = previous.filter(row => row.key !== key);
        pendingFocus.current = remaining.length ? remaining[Math.min(previous.findIndex(row => row.key === key), remaining.length - 1)].key : 'add';
        return remaining;
      });
    };
    const add = () => {
      if (rows.length >= maximum || args.disabled) return;
      if (!Number.isSafeInteger(nextKey.current) || nextKey.current === Number.MAX_SAFE_INTEGER) fail();
      const key = nextKey.current++;
      const value = columns === null ? '' : Object.fromEntries(columns.map(column => [column.name, '']));
      pendingFocus.current = key;
      setRows(previous => previous.length >= maximum ? previous : [...previous, { key, value }]);
    };
    const title = p.label(node.props.key, node.props.params, context);
    return h('div', { id: args.id, ref: root, 'data-pixs-list': node.props.name },
      ...rows.map((row, index) => h('div', {
        key: row.key, className: 'presentation-row', 'data-pixs-row': String(row.key),
      },
      ...(columns ?? [{ name: 'value', key: node.props.key, params: node.props.params, required: node.props.itemRequired }]).map(column => {
        const id = args.id + '-row-' + row.key + '-' + column.name;
        const label = columns === null ? title : p.label(column.key, column.params, context);
        return h('label', { key: column.name, htmlFor: id },
          label + ' ' + String(index + 1),
          h('textarea', {
            id, 'data-column': column.name, value: columns === null ? row.value : row.value[column.name],
            disabled: args.disabled, required: column.required, maxLength: args.maxTextLength,
            'aria-describedby': args.describedBy,
            onChange: event => update(row.key, column.name, event.target.value),
          }));
      }),
      h('button', {
        type: 'button', disabled: args.disabled || rows.length <= node.props.minItems,
        'aria-label': p.text('shell.fieldRemove') + ' ' + title + ' ' + String(index + 1),
        onClick: () => remove(row.key),
      }, p.text('shell.fieldRemove')))),
      h('button', {
        type: 'button', 'data-pixs-add': '', disabled: args.disabled || rows.length >= maximum,
        'aria-label': p.text('shell.fieldAdd') + ' ' + title, onClick: add,
      }, p.text('shell.fieldAdd')));
  }
  function field(node, args, context) {
    if (node.variant === 'string-list' || node.variant === 'record-list') {
      return h(ListEditor, { key: JSON.stringify([context.owner, context.id, args.formId, node.props.name, args.modelKey]), node, args, context });
    }
    const common = {
      id: args.id, name: node.props.name, disabled: args.disabled, 'aria-describedby': args.describedBy,
    };
    if (node.variant === 'text') return h('input', {
      ...common, type: 'text', required: node.props.required, defaultValue: node.props.initial, maxLength: args.maxTextLength,
    });
    if (node.variant === 'boolean') return h('input', {
      ...common, type: 'checkbox', defaultChecked: node.props.initial,
    });
    if (node.variant === 'integer') return h('input', {
      ...common, type: 'number', step: 1, required: node.props.required,
      defaultValue: node.props.initial === null ? '' : String(node.props.initial),
      ...(node.props.minimum === null ? {} : { min: node.props.minimum }),
      ...(node.props.maximum === null ? {} : { max: node.props.maximum }),
    });
    fail();
  }
  function readFields(form, names, context, metadata) {
    if (!form || typeof form.querySelectorAll !== 'function' || !metadata
        || !Array.isArray(metadata.fields) || metadata.fields.length !== names.length) fail();
    const output = {};
    for (const node of metadata.fields) {
      const name = node.props.name;
      if (!names.includes(name) || Object.hasOwn(output, name) || !/^[a-z][a-z0-9_]*$/.test(name)) fail();
      let value;
      if (node.variant === 'string-list' || node.variant === 'record-list') {
        const roots = form.querySelectorAll('[data-pixs-list="' + name + '"]');
        if (roots.length !== 1) fail();
        const rows = [...roots[0].querySelectorAll('[data-pixs-row]')];
        if (rows.length > context.limits.maxDataNodes) fail();
        value = rows.map(row => {
          if (node.variant === 'string-list') {
            const inputs = row.querySelectorAll('textarea[data-column="value"]');
            if (inputs.length !== 1) fail();
            return inputs[0].value;
          }
          return Object.fromEntries(node.props.columns.map(column => {
            const inputs = row.querySelectorAll('textarea[data-column="' + column.name + '"]');
            if (inputs.length !== 1) fail();
            return [column.name, inputs[0].value];
          }));
        });
      } else {
        const inputs = form.querySelectorAll('input[name="' + name + '"]');
        if (inputs.length !== 1) fail();
        const input = inputs[0];
        if (node.variant === 'boolean') value = input.checked;
        else if (node.variant === 'integer') {
          if (input.validity?.badInput) fail();
          value = input.value === '' ? null : input.valueAsNumber;
        }
        else if (node.variant === 'text') value = input.value;
        else fail();
      }
      Object.defineProperty(output, name, { value, enumerable: true });
    }
    return output;
  }
  return Object.freeze({ field, readFields });
}
