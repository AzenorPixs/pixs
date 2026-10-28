// Adapter privé vers le moteur injecté, sans preuve de serveur ni d’isolation.
import { validatePresentationTree, validatePresentationFieldInput } from './presentation-contract-v1.js';

export const PRESENTATION_ADAPTER_VERSION = '1.0.0';

export const PRESENTATION_ADAPTER_CODES = Object.freeze([
  'ADAPTER_PORTS_INVALID',
  'ADAPTER_TREE_INVALID',
  'ADAPTER_LABEL_INVALID',
  'ADAPTER_ID_INVALID',
  'ADAPTER_STATE_INVALID',
  'ADAPTER_FIELDS_INVALID',
  'ADAPTER_SUBMIT_INVALID',
  'ADAPTER_SLOT_INVALID',
  'ADAPTER_COMPONENT_INVALID',
  'ADAPTER_ON_ERROR_INVALID',
]);

// Classes sémantiques requises pour la prochaine unité CSS/main (aucun style
// inline/HTML brut/moteur importé ici ; l'adapter n'émet que ces className).
export const PRESENTATION_CLASSES = Object.freeze({
  'action': 'present-action',
  'section.panel': 'panel present-section-panel',
  'section.stack': 'present-section-stack',
  'section.row': 'present-section-row',
  'heading.page': 'present-heading-page',
  'heading.section': 'present-heading-section',
  'text.body': 'present-text-body',
  'text.muted': 'present-text-muted',
  'link.default': 'present-link-default',
  'button.primary': 'present-button-primary',
  'button.secondary': 'present-button-secondary',
  'field.text': 'present-field-text',
  'field.boolean': 'present-field-boolean',
  'field.integer': 'present-field-integer',
  'field.string-list': 'present-field-string-list',
  'field.record-list': 'present-field-record-list',
  'form.stack': 'panel present-form-stack',
  'slot.append': 'present-slot-append',
  'status.command': 'present-status-command',
  'status.query': 'present-status-query',
  'component.public': 'present-component-public',
});

const ADAPTER_STATES = new Set(['IDLE', 'PENDING', 'CONFIRMED', 'REJECTED', 'UNKNOWN', 'UNAVAILABLE', 'INVALID', 'LOADED']);
const SUBMIT_ON_ERROR_CODE = 'PRESENTATION_SUBMIT_FAILED';

export class PresentationAdapterError extends Error {
  constructor(code, options) {
    super(code, options);
    this.name = 'PresentationAdapterError';
    this.code = code;
  }
}

function fail(code) {
  throw new PresentationAdapterError(code);
}

function isPlainRecord(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}

function intentKindOf(intent) {
  if (intent === null) return null;
  if (Object.hasOwn(intent, 'query')) return 'QUERY';
  if (Object.hasOwn(intent, 'command')) return 'COMMAND';
  return null;
}
function closedPorts(ports) {
  if (ports === null || typeof ports !== 'object' || Array.isArray(ports)) fail('ADAPTER_PORTS_INVALID');
  const proto = Object.getPrototypeOf(ports);
  if (proto !== Object.prototype && proto !== null) fail('ADAPTER_PORTS_INVALID');
  const required = ['h', 'Link', 'label', 'id', 'state', 'submit', 'readFields', 'slot', 'component', 'onError'];
  const keys = Reflect.ownKeys(ports);
  const hasField = Object.hasOwn(ports, 'field');
  if (!hasField) {
    if (keys.length !== required.length) fail('ADAPTER_PORTS_INVALID');
    for (const key of required) {
      if (!Object.hasOwn(ports, key)) fail('ADAPTER_PORTS_INVALID');
      const descriptor = Object.getOwnPropertyDescriptor(ports, key);
      if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('ADAPTER_PORTS_INVALID');
    }
  } else {
    if (keys.length !== required.length + 1) fail('ADAPTER_PORTS_INVALID');
    for (const key of required) {
      if (!Object.hasOwn(ports, key)) fail('ADAPTER_PORTS_INVALID');
      const descriptor = Object.getOwnPropertyDescriptor(ports, key);
      if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('ADAPTER_PORTS_INVALID');
    }
    const fieldDescriptor = Object.getOwnPropertyDescriptor(ports, 'field');
    if (!fieldDescriptor || !Object.hasOwn(fieldDescriptor, 'value')) fail('ADAPTER_PORTS_INVALID');
    if (typeof ports.field !== 'function') fail('ADAPTER_PORTS_INVALID');
  }
  if (typeof ports.h !== 'function') fail('ADAPTER_PORTS_INVALID');
  const linkProto = ports.Link !== null && (typeof ports.Link === 'function' || typeof ports.Link === 'object');
  if (!linkProto) fail('ADAPTER_PORTS_INVALID');
  for (const name of ['label', 'id', 'state', 'submit', 'readFields', 'slot', 'component', 'onError']) {
    if (typeof ports[name] !== 'function') fail('ADAPTER_PORTS_INVALID');
  }
  return ports;
}

function checkedDomId(value) {
  if (typeof value !== 'string' || !/^[A-Za-z][A-Za-z0-9_-]*$/.test(value)) fail('ADAPTER_ID_INVALID');
  for (let index = 0; index < value.length; index += 1) {
    const unit = value.charCodeAt(index);
    if (unit < 32 || unit === 127) fail('ADAPTER_ID_INVALID');
    if (value[index] === ' ' || value[index] === '"' || value[index] === "'" || value[index] === '<' || value[index] === '>' || value[index] === '`') {
      fail('ADAPTER_ID_INVALID');
    }
  }
  return value;
}

function checkedState(value, maxText) {
  if (!isPlainRecord(value)) fail('ADAPTER_STATE_INVALID');
  const keys = Reflect.ownKeys(value);
  if (keys.length !== 4) fail('ADAPTER_STATE_INVALID');
  for (const key of ['state', 'message', 'canSubmit', 'fieldsDisabled']) {
    if (!Object.hasOwn(value, key)) fail('ADAPTER_STATE_INVALID');
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail('ADAPTER_STATE_INVALID');
  }
  if (!ADAPTER_STATES.has(value.state)) fail('ADAPTER_STATE_INVALID');
  if (typeof value.message !== 'string' || value.message.length > maxText) fail('ADAPTER_STATE_INVALID');
  if (typeof value.canSubmit !== 'boolean' || typeof value.fieldsDisabled !== 'boolean') fail('ADAPTER_STATE_INVALID');
  return value;
}

function buildLinkHref(route, routeParams) {
  if (route === '/') return '/';
  const parts = route.slice(1).split('/');
  const rendered = parts.map((part) => {
    if (part.startsWith('{') && part.endsWith('}')) {
      const name = part.slice(1, -1);
      return encodeURIComponent(routeParams[name]);
    }
    return part;
  });
  return '/' + rendered.join('/');
}


export function createPresentationAdapter(ports){
  const source=closedPorts(ports);
  const basePorts=['h','Link','label','id','state','submit','readFields','slot','component','onError'];
  const portNames=Object.hasOwn(source,'field')?[...basePorts,'field']:basePorts;
  const p=Object.freeze(Object.fromEntries(portNames.map(k=>[k,source[k]])));
  return Object.freeze({
    render(tree,context){
      const valid=validatePresentationTree(tree,context);
      const ctx=JSON.parse(JSON.stringify(context)),freeze=[ctx];
      while(freeze.length){const v=freeze.pop();for(const child of Object.values(v))if(child!==null&&typeof child==='object')freeze.push(child);Object.freeze(v);}
      const maxText=ctx.limits.maxTextLength,records=[],metadata=new Map(),built=new Map(),ids=new Set(),statusByAction=new Map(),formFields=new Map(),formModelKey=new Map(),actionKind=new Map();
      const takeId=local=>{
        const value=checkedDomId(p.id(local,ctx));
        if(value.length>maxText||ids.has(value))fail('ADAPTER_ID_INVALID');
        ids.add(value);return value;
      };
      const pending=[{node:valid,form:null}];
      while(pending.length){
        const frame=pending.pop(),n=frame.node,index=records.length;
        if(index>=ctx.limits.maxNodes)fail('ADAPTER_TREE_INVALID');
        const form=n.kind==='form'?n.props.id:frame.form;
        const m={index,form,id:null};
        records.push(n);metadata.set(n,m);
        if(n.kind==='heading'||n.kind==='field'||n.kind==='form'||n.kind==='button'||n.kind==='status')m.id=takeId('node-'+index);
        if(n.kind==='form'){
          formFields.set(n.props.id,[]);
          formModelKey.set(n.props.id,Object.hasOwn(n.props,'modelKey')?n.props.modelKey:null);
          actionKind.set(n.props.id,intentKindOf(n.props.intent));
        }
        if(n.kind==='field')formFields.get(form).push(n);
        if(n.kind==='button'&&!n.props.submit)actionKind.set(n.props.id,intentKindOf(n.props.intent));
        if(n.kind==='status'&&!statusByAction.has(n.props.for))statusByAction.set(n.props.for,m.id);
        for(let i=n.children.length-1;i>=0;i--)pending.push({node:n.children[i],form});
      }
      const autoStatus=new Map();
      for(const n of records)if(n.kind==='form'||n.kind==='button'&&!n.props.submit){
        if(!statusByAction.has(n.props.id)){
          const id=takeId('auto-'+metadata.get(n).index);
          autoStatus.set(n.props.id,id);statusByAction.set(n.props.id,id);
        }
      }
      const label=n=>{
        const value=p.label(n.props.key,n.props.params,ctx);
        if(typeof value!=='string'||value.length>maxText||((n.kind!=='text')&&value.trim().length===0))fail('ADAPTER_LABEL_INVALID');
        return value;
      };
      const state=id=>{
        const value=checkedState(p.state(id,ctx),maxText),kind=actionKind.get(id);
        if(kind==='COMMAND'&&value.state==='LOADED')fail('ADAPTER_STATE_INVALID');
        if(kind==='QUERY'&&['CONFIRMED','UNKNOWN'].includes(value.state))fail('ADAPTER_STATE_INVALID');
        return value;
      };
      const outputKind=id=>actionKind.get(id)==='QUERY'?'QUERY':'COMMAND';
      const output=(id,dom)=>{
        const s=state(id);
        const kind=outputKind(id);
        if(kind==='QUERY')return p.h('output',{id:dom,className:PRESENTATION_CLASSES['status.query'],role:'status','aria-live':'polite','data-query-state':s.state},s.message);
        return p.h('output',{id:dom,className:PRESENTATION_CLASSES['status.command'],role:'status','aria-live':'polite','data-command-state':s.state},s.message);
      };
      const execute=async(event,id,intent,fields)=>{
        if(!event||typeof event.preventDefault!=='function')fail('ADAPTER_SUBMIT_INVALID');
        event.preventDefault();
        const fresh=state(id);if(!fresh.canSubmit||fresh.state==='PENDING')return;
        try{
          const names=fields.map(f=>f.props.name);
          const raw=fields.length?p.readFields(event.currentTarget,names,ctx,{formId:id,fields}):{};
          if(!isPlainRecord(raw)||Reflect.ownKeys(raw).length!==fields.length)fail('ADAPTER_FIELDS_INVALID');
          const values={};
          for(const f of fields){
            const name=f.props.name;
            const d=Object.getOwnPropertyDescriptor(raw,name);
            if(!d||!Object.hasOwn(d,'value'))fail('ADAPTER_FIELDS_INVALID');
            const checked=validatePresentationFieldInput(f,d.value,ctx.limits);
            Object.defineProperty(values,name,{value:checked,enumerable:true});
          }
          await p.submit(id,intent,Object.freeze(values),ctx);
        }catch{
          await p.onError(id,SUBMIT_ON_ERROR_CODE,ctx);
        }
      };
      for(let i=records.length-1;i>=0;i--){
        const n=records[i],m=metadata.get(n),children=n.children.map(c=>built.get(c)),props={className:PRESENTATION_CLASSES[n.kind+'.'+n.variant],key:'node-'+m.index};
        let element;
        if(n.kind==='section'){
          const heading=n.children.find(c=>c.kind==='heading');
          if(heading)props['aria-labelledby']=metadata.get(heading).id;
          element=p.h('section',props,...children);
        }else if(n.kind==='heading'){
          props.id=m.id;element=p.h(n.variant==='page'?'h1':'h2',props,label(n));
        }else if(n.kind==='text'){
          element=p.h('p',props,label(n));
        }else if(n.kind==='link'){
          props.to=buildLinkHref(n.props.route,n.props.routeParams);element=p.h(p.Link,props,label(n));
        }else if(n.kind==='slot'){
          element=p.h('div',props,p.slot(n.props.point,ctx));
        }else if(n.kind==='component'){
          element=p.h('div',props,p.component(n.props.owner,n.props.id,ctx));
        }else if(n.kind==='status'){
          element=output(n.props.for,m.id);
        }else if(n.kind==='field'){
          const s=state(m.form),modelKey=formModelKey.get(m.form)??null;
          const fieldArgs={id:m.id,formId:m.form,disabled:s.fieldsDisabled,describedBy:statusByAction.get(m.form),maxTextLength:maxText,modelKey};
          let input;
          if(Object.hasOwn(p,'field')){
            input=p.field(n,fieldArgs,ctx);
          }else{
            if(n.variant!=='text')fail('ADAPTER_PORTS_INVALID');
            input=p.h('input',{id:m.id,name:n.props.name,type:'text',required:n.props.required,defaultValue:n.props.initial,maxLength:maxText,disabled:s.fieldsDisabled,'aria-describedby':statusByAction.get(m.form)});
          }
          if(n.variant==='string-list'||n.variant==='record-list'){
            props.disabled=s.fieldsDisabled;
            props['aria-describedby']=statusByAction.get(m.form);
            element=p.h('fieldset',props,p.h('legend',{},label(n)),input);
          }else{
            props.htmlFor=m.id;element=p.h('label',props,label(n),input);
          }
        }else if(n.kind==='button'){
          const action=n.props.submit?m.form:n.props.id,s=state(action);
          props.id=m.id;props.type=n.props.submit?'submit':'button';props.disabled=!s.canSubmit||s.state==='PENDING';props['aria-disabled']=props.disabled;props['aria-describedby']=statusByAction.get(action);
          if(!n.props.submit)props.onClick=event=>execute(event,n.props.id,n.props.intent,[]);
          const button=p.h('button',props,label(n));
          element=!n.props.submit&&autoStatus.has(action)?p.h('div',{className:PRESENTATION_CLASSES.action,key:'action-'+m.index},button,output(action,autoStatus.get(action))):button;
        }else if(n.kind==='form'){
          const s=state(n.props.id);
          props.id=m.id;props['aria-label']=label(n);props['aria-busy']=s.state==='PENDING';props['aria-describedby']=statusByAction.get(n.props.id);
          if(Object.hasOwn(n.props,'modelKey'))props.key=props.key+'::'+n.props.modelKey;
          props.onSubmit=event=>execute(event,n.props.id,n.props.intent,formFields.get(n.props.id));
          if(autoStatus.has(n.props.id))children.push(output(n.props.id,autoStatus.get(n.props.id)));
          element=p.h('form',props,...children);
        }else fail('ADAPTER_TREE_INVALID');
        built.set(n,element);
      }
      return built.get(valid);
    },
  });
}
