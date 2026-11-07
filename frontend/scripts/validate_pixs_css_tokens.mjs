export class CssTokenError extends Error {
  constructor(code, detail) { super(code + (detail ? ': ' + detail : '')); this.name='CssTokenError'; this.code=code; }
}
const OWNER_SUFFIX = '/frontend/src/theme.css';
const TOKEN_NAMES = new Set(['--surface','--panel','--text','--muted','--accent','--border','--focus','--space-small','--space','--space-large','--radius','--line-height','--heading-line-height','--body-size','--small-size','--heading-size','--brand-size','--weight','--strong-weight','--control-height','--content-width','--border-width','--focus-width','--focus-offset','--page-padding','--layout-field-min','--checkbox-size','--state-disabled-opacity','--z-index-skip','--skip-link-hidden-shift']);
const DARK_OVERRIDES = new Set(['--surface','--panel','--text','--muted','--accent','--border','--focus']);
const OBSERVED_PROPS = new Set(['color-scheme','box-sizing','margin','background','color','font','outline','outline-offset','max-inline-size','margin-inline','padding','display','flex-wrap','align-items','justify-content','gap','margin-block-end','font-size','font-weight','text-decoration','flex-direction','border','border-radius','padding-inline','min-inline-size','overflow-wrap','margin-block','line-height','position','inset-block-start','inset-inline-start','transform','z-index','flex','inline-size','block-size','min-block-size','accent-color','cursor','opacity','border-color','white-space','resize','padding-inline-start','border-inline-start','border-inline-start-style','list-style','margin-block-start']);
const ALLOW_PAIR = new Set(['box-sizing:border-box','margin:0','max-inline-size:100%','min-inline-size:0','inline-size:100%','padding:0','list-style:none','text-decoration:none','text-decoration:underline','cursor:default','cursor:pointer','overflow-wrap:anywhere','display:grid','display:flex','display:block','flex-wrap:wrap','border-inline-start-style:dashed','resize:vertical','white-space:pre-wrap','transform:none','font:inherit','margin-inline:auto','color-scheme:light','color-scheme:dark','align-items:center','align-items:start','justify-content:space-between','flex-direction:column','flex-direction:row','position:absolute','margin-block:0var(--space)','padding:var(--space-small)var(--space)','flex:11var(--layout-field-min)','min-block-size:calc(var(--control-height)*2)','border:var(--border-width)solidvar(--border)','outline:var(--focus-width)solidvar(--focus)','border-inline-start:var(--focus-width)solidvar(--border)','font:var(--weight)var(--body-size)/var(--line-height)system-ui,sans-serif']);
const VAR_RE = /var\(--[a-z-]+\)/g;
function lineOfUpTo(t,i){let n=1;for(let k=0;k<i;k++)if(t[k]==='\n')n++;return n;}
const normV = s => s.replace(/\s+/g,'');
export function validatePixsCssTokens(cssText,{file,isOwner}={}){
  if(typeof cssText!=='string'||!cssText||typeof file!=='string'||!file)throw new CssTokenError('CSS_INPUT_INVALID',file);
  const clean=file.split('?')[0].replace(/\\/g,'/');
  const computed=clean.endsWith(OWNER_SUFFIX);
  if(isOwner!==undefined&&isOwner!==computed)throw new CssTokenError('CSS_OWNER_MISMATCH',file);
  const owner=computed;
  const noC=cssText.replace(/\/\*[\s\S]*?\*\//g,m=>'\n'.repeat(m.split('\n').length-1));
  if(/\/\*/.test(noC))throw new CssTokenError('CSS_COMMENT_UNCLOSED',file);
  if(/@[a-zA-Z]/.test(noC))throw new CssTokenError('CSS_ATRULE_REFUSED',file);
  if(/[&]/.test(noC))throw new CssTokenError('CSS_NESTING_REFUSED',file);
  if(/url\s*\(/i.test(noC))throw new CssTokenError('CSS_URL_REFUSED',file);
  if(/!important/i.test(noC))throw new CssTokenError('CSS_IMPORTANT_REFUSED',file);
  if((noC.match(/{/g)||[]).length!==(noC.match(/}/g)||[]).length)throw new CssTokenError('CSS_BLOCK_UNCLOSED',file);
  const seenL=new Set(),seenD=new Set();
  let pos=0;
  while(pos<noC.length){
    const open=noC.indexOf('{',pos);
    if(open===-1){if(noC.slice(pos).trim()!=='')throw new CssTokenError('CSS_DECL_OUTSIDE_BLOCK',file);break;}
    const sel=noC.slice(pos,open).trim().replace(/\s+/g,' ');
    const close=noC.indexOf('}',open);
    if(close===-1)throw new CssTokenError('CSS_BLOCK_UNCLOSED',file);
    if(noC.slice(open+1,close).includes('{'))throw new CssTokenError('CSS_NESTING_REFUSED',file);
    if(!sel)throw new CssTokenError('CSS_SELECTOR_EMPTY',file);
    const isRoot=/^:root(\[data-theme=(['"]?)dark\2\])?$/.test(sel);
    const isDark=isRoot&&sel.includes('dark');
    const body=noC.slice(open+1,close);
    let dpos=0;
    for(const raw of body.split(';')){
      const segStart=open+1+body.indexOf(raw,dpos);dpos+=raw.length+1;
      const d=raw.trim();if(!d)continue;
      const ci=raw.indexOf(':');if(ci===-1)throw new CssTokenError('CSS_DECL_INVALID',file+':'+lineOfUpTo(noC,segStart));
      const prop=raw.slice(0,ci).trim(),val=raw.slice(ci+1).trim(),ln=file+':'+lineOfUpTo(noC,segStart);
      if(!prop||!val)throw new CssTokenError('CSS_DECL_INVALID',ln);
      if(prop.startsWith('--')){
        if(!(isRoot&&owner))throw new CssTokenError('CSS_TOKEN_OWNER_VIOLATION',ln);
        if(!TOKEN_NAMES.has(prop))throw new CssTokenError('CSS_TOKEN_UNKNOWN',ln);
        const seen=isDark?seenD:seenL;
        if(seen.has(prop))throw new CssTokenError('CSS_TOKEN_DUPLICATE',ln);
        seen.add(prop);continue;
      }
      if(!OBSERVED_PROPS.has(prop))throw new CssTokenError('CSS_PROP_UNKNOWN',ln);
      if(ALLOW_PAIR.has(prop+':'+normV(val)))continue;
      for(const m of val.matchAll(/var\(/g)){
        const sub=val.slice(m.index,m.index+64);
        const ok=/^var\(--[a-z-]+\)/.test(sub);
        if(!ok)throw new CssTokenError('CSS_VAR_SYNTAX_REFUSED',ln);
        if(!TOKEN_NAMES.has(sub.slice(4,sub.indexOf(')'))))throw new CssTokenError('CSS_VAR_UNKNOWN_TOKEN',ln);
      }
      const stripped=val.replace(VAR_RE,'«V»');
      if(/var\(/.test(stripped))throw new CssTokenError('CSS_VAR_SYNTAX_REFUSED',ln);
      if(/^\s*«V»(\s*[,/]?\s*«V»)*\s*$/.test(stripped))continue;
      throw new CssTokenError('CSS_TOKEN_VIOLATION',ln);
    }
    pos=close+1;
  }
  if(!owner)return true;
  if(seenL.size!==30||![...TOKEN_NAMES].every(k=>seenL.has(k)))throw new CssTokenError('CSS_TOKENS_INCOMPLETE',file);
  if(seenD.size!==7||![...DARK_OVERRIDES].every(k=>seenD.has(k)))throw new CssTokenError('CSS_DARK_INCOMPLETE',file);
  return true;
}
