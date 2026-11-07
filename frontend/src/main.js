// main.js — shell React : STANDALONE inchangé, COMPOSED raccordé aux vrais runtimes.
// Aucune API fictive : renderContribution -> {tree, context} ; pas de getPresentationContext.
// Le graphe, les usines et le moteur restent privés au runtime de composition.
import { createElement as h, Component, createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { createRoot } from 'react-dom/client';
import { createRootRoute, createRoute, createRouter, Link, Outlet, RouterProvider, redirect, useParams, useRouterState } from '@tanstack/react-router';
import { catalogs, resolveLocale } from './catalogs.js';
import { createSessionRuntime } from './shell/session-runtime-v1.js';
import { createCompositionRuntime } from './shell/composition-runtime-v1.js';
import { createPresentationAdapter } from './shell/presentation-adapter-v1.js';
import { createPresentationFields } from './shell/presentation-fields-v1.js';
import * as composition from 'virtual:pixs-composition/v1';
import './theme.css';

const Presentation = createContext(null);
const usePresentation = () => useContext(Presentation);
const COMPOSED = composition.mode === 'COMPOSED';

// ---------- STANDALONE : comportement actuel préservé, sans session ni réseau ----------
function Home() {
  const { text } = usePresentation();
  return h('section', { className: 'panel', 'aria-labelledby': 'home-heading' },
    h('p', { className: 'eyebrow' }, text['shell.development']),
    h('h1', { id: 'home-heading' }, text['shell.heading']),
    h('p', null, text['shell.description']));
}
function NotFound() {
  const { text } = usePresentation();
  return h('section', { className: 'panel', 'aria-labelledby': 'unavailable-heading' },
    h('h1', { id: 'unavailable-heading' }, text['shell.notFound']),
    h('p', null, text['shell.notFoundDescription']),
    h(Link, { to: '/' }, text['shell.home']));
}
function Shell() {
  const { text, locale, setLocale, theme, setTheme } = usePresentation();
  return h('div', { className: 'shell' },
    h('a', { className: 'skip-link', href: '#content' }, text['shell.skip']),
    h('header', { className: 'header' },
      h(Link, { className: 'brand', to: '/' }, text['shell.title']),
      h('div', { className: 'preferences' },
        h('label', null, text['shell.language'],
          h('select', { value: locale, onChange: event => setLocale(event.target.value) },
            h('option', { value: 'en' }, text['shell.english']),
            h('option', { value: 'fr' }, text['shell.french']))),
        h('label', null, text['shell.theme'],
          h('select', { value: theme, onChange: event => setTheme(event.target.value) },
            ...['system', 'light', 'dark'].map(value => h('option', { key: value, value }, text['shell.' + value]))))),
    ),
    h('main', { id: 'content', tabIndex: -1 }, h(Outlet)),
    h('footer', null, text['shell.footer']));
}

// ---------- COMPOSED : ports exacts, une seule session et un seul runtime privés ----------
// Convertit un chemin graphe {param} en chemin TanStack $param.
function toTanStack(path) {
  if (path === '/') return '/';
  return '/' + path.slice(1).split('/').map(part =>
    part.startsWith('{') && part.endsWith('}') ? '$' + part.slice(1, -1) : part).join('/');
}
// Segment opaque : refusé avant tout envoi si manquant, encodé sans injection de chemin.
function encodeSegment(value) {
  if (typeof value !== 'string' || !value || value === '.' || value === '..') throw new Error('COMPOSITION_ROUTE_INVALID');
  if (value.includes(String.fromCharCode(0))) throw new Error('COMPOSITION_ROUTE_INVALID');
  return encodeURIComponent(value);
}
function hrefFor(route, params) {
  if (route === '/') return '/';
  return '/' + route.slice(1).split('/').map(part => {
    if (part.startsWith('{') && part.endsWith('}')) {
      const name = part.slice(1, -1);
      if (!Object.hasOwn(params, name)) throw new Error('COMPOSITION_ROUTE_INVALID');
      return encodeSegment(params[name]);
    }
    return part;
  }).join('/');
}
// Substitution stricte des paramètres de catalogue (aucun HTML construit ici).
function fillText(template, params) {
  return template.replace(/\{([A-Za-z][A-Za-z0-9_]*)\}/g, (all, name) => {
    if (!Object.hasOwn(params, name)) throw new Error('COMPOSITION_LABEL_UNKNOWN');
    const value = params[name];
    if (typeof value !== 'string' && typeof value !== 'number' && typeof value !== 'boolean') throw new Error('COMPOSITION_LABEL_UNKNOWN');
    return String(value);
  });
}

// Ressources privées de l’instance React, sans exposition aux contributions ni à window.
function createRuntimes(localeRef, notifyError, routerRef) {
  // Horloge et origine réelles du navigateur ; aucun stockage, aucun cookie, aucun secret journalisé.
  const channel = (() => {
    try {
      if (typeof BroadcastChannel !== 'function') return null;
      return new BroadcastChannel('pixs-shell');
    } catch (cause) {
      if (['SecurityError', 'NotSupportedError'].includes(cause?.name)) return null;
      throw cause;
    }
  })();
  const session = createSessionRuntime({
    fetchImpl: (url, init) => fetch(url, init), // same-origin imposé par le runtime (credentials/redirect/origin vérifiés)
    origin: window.location.origin,
    clock: { now: () => Date.now(), setTimeout: (...args) => window.setTimeout(...args), clearTimeout: (...args) => window.clearTimeout(...args) },
    createId: () => window.crypto.randomUUID(),
    fingerprint: async (data) => {
      const digest = await window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(data));
      return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
    },
    channel,
    getLocale: () => localeRef.current,
  });
  const translate = (key, params = {}, presentationContext = null) => {
    const locale = localeRef.current;
    const table = key.startsWith('shell.')
      ? catalogs[locale]
      : presentationContext?.catalogs[locale];
    if (!table || !Object.hasOwn(table, key)) throw new Error('COMPOSITION_LABEL_UNKNOWN');
    return fillText(table[key], params ?? {});
  };
  let runtime;
  try { runtime = createCompositionRuntime({
    graph: composition.graph,
    factories: composition.factories, // usines privées : jamais transmises aux contributions
    session,
    translate,
    navigate: (path, params = {}) => {
      if (!routerRef.current) throw new Error('COMPOSITION_NAVIGATE_UNAVAILABLE');
      return routerRef.current.navigate({ to: hrefFor(path, params) });
    },
    presentationLimits: composition.presentationLimits,
    points: composition.points, // registre réel {points, metadata}, pas un tableau
    createId: () => window.crypto.randomUUID(),
    fingerprint: async (data) => {
      const digest = await window.crypto.subtle.digest('SHA-256', new TextEncoder().encode(data));
      return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
    },
    onError: (code) => notifyError(typeof code === 'string' && code ? code : 'COMPOSITION_ACTION_FAILED'),
  }); } catch (cause) {
    try { session.dispose(); }
    catch (cleanupCause) { throw new AggregateError([cause, cleanupCause], 'SHELL_INITIALIZATION_FAILED'); }
    throw cause;
  }
  return Object.freeze({ session, runtime, translate });
}

// Générateur d'id DOM : stable par instance de rendu, unique document, court, sans donnée sensible.
let globalIdSeq = 0;
function makeIdGenerator(instanceKey) {
  const table = new Map();
  const prefix = 'p' + (globalIdSeq++).toString(36) + (typeof instanceKey === 'string' && instanceKey ? instanceKey.length.toString(36) : '0');
  return (local) => {
    if (typeof local !== 'string' || !local) throw new Error('ADAPTER_ID_INVALID');
    if (!table.has(local)) table.set(local, prefix + 'n' + table.size.toString(36));
    return table.get(local);
  };
}

function substituteRouteParams(route, scope) {
  // Remplit {tenant_id}/{scope_id} depuis le contexte actif vérifié ; autre paramètre -> indisponible.
  const params = {};
  for (const part of route.slice(1).split('/')) {
    if (!part.startsWith('{')) continue;
    const name = part.slice(1, -1);
    if ((name === 'tenant_id' || name === 'scope_id') && scope && typeof scope[name] === 'string' && scope[name]) params[name] = scope[name];
    else return null;
  }
  return params;
}

function ComposedSlot({ point, ctx, ancestors, instanceKey, params = {} }) {
  const { runtime, text } = useComposed();
  let items = null;
  try {
    items = ctx ? runtime.slotContributions(point, ctx) : runtime.slotContributions(point);
  } catch { return h('p', { role: 'alert' }, text['shell.componentUnavailable']); }
  if (!items.length) return null;
  return h('div', { className: 'present-slot-append' }, ...items.map(item =>
    h('div', { key: item.owner + '/' + item.id },
      h(ComposedComponent, { owner: item.owner, id: item.id, params, parentCtx: null, ancestors, instanceKey: instanceKey + 's' + item.id }))));
}

function ComposedComponent({ owner, id, params, parentCtx, ancestors, instanceKey }) {
  const { runtime, text } = useComposed();
  const key = owner + '/' + id;
  if (ancestors.includes(key)) return h('p', null, text['shell.componentUnavailable']); // cycle réel coupé
  let produced;
  try {
    produced = parentCtx
      ? runtime.renderComponent(parentCtx, owner, id, params ?? {})
      : runtime.renderContribution(owner, id, params ?? {});
  } catch { return h('p', { role: 'alert' }, text['shell.componentUnavailable']); } // emplacement seul, sans écraser le reste
  return h(PresentationView, { tree: produced.tree, ctx: produced.context, params, ancestors: [...ancestors, key], instanceKey: (instanceKey ?? '') + 'c' });
}

function PresentationView({ tree, ctx, ancestors, instanceKey, params = {} }) {
  const env = useComposed();
  const envRef = useRef(env); envRef.current = env;
  const idRef = useRef(null), fieldsRef = useRef(null);
  if (idRef.current === null) idRef.current = makeIdGenerator(instanceKey);
  const label = (key, values, context) => {
    const table = context.catalogs[envRef.current.locale];
    if (!Object.hasOwn(table, key)) throw new Error('COMPOSITION_LABEL_UNKNOWN');
    return fillText(table[key], values ?? {});
  };
  if (fieldsRef.current === null) fieldsRef.current = createPresentationFields({
    label, text: key => envRef.current.text[key],
  });
  const fields = fieldsRef.current;
  let childIndex = 0;
  // Les ports privés gardent le contexte authentique ; la copie de l’adapter reste une donnée.
  const adapter = createPresentationAdapter({
    h, Link, label, id: local => idRef.current(local),
    state: action => env.runtime.actionState(action, ctx),
    submit: (action, intent, values) => env.runtime.submit(action, intent, values, ctx),
    readFields: fields.readFields,
    slot: point => h(ComposedSlot, {
      point, ctx, params, ancestors, instanceKey: instanceKey + '-s-' + childIndex++,
    }),
    component: (owner, id) => h(ComposedComponent, {
      owner, id, params, parentCtx: ctx, ancestors, instanceKey: instanceKey + '-c-' + childIndex++,
    }),
    onError: (action, code) => {
      try { env.runtime.reportError(action, code, ctx); }
      catch (cause) { env.notifyError(cause?.code ?? 'COMPOSITION_ACTION_FAILED'); }
      env.notifyError(code);
    },
    field: fields.field,
  });
  try { return adapter.render(tree, ctx); }
  catch { return h('p', { role: 'alert' }, env.text['shell.componentUnavailable']); }
}

const ComposedContext = createContext(null);
function useComposed() { return useContext(ComposedContext); }

// Écran explicite de choix de contexte : vide initial admis, valeurs opaques saisies telles quelles.
function ContextChoice() {
  const { session, text, router } = useComposed();
  const [kind, setKind] = useState('');
  const [tenantId, setTenantId] = useState('');
  const [scopeId, setScopeId] = useState('');
  const [pending, setPending] = useState(false);
  const [error, setError] = useState(null);
  const submit = async (event) => {
    event.preventDefault();
    setPending(true);
    setError(null);
    try {
      if (!['platform', 'tenant', 'scope'].includes(kind)) throw new Error('SESSION_CONTEXT_REQUIRED');
      const scope = kind === 'platform'
        ? { scope_type: 'PLATFORM', tenant_id: null, scope_id: null }
        : kind === 'tenant'
          ? { scope_type: 'TENANT', tenant_id: tenantId, scope_id: null }
          : { scope_type: 'TENANT', tenant_id: tenantId, scope_id: scopeId };
      await session.load(scope); // vrai GET shell/context, aucun grant local
      await router.navigate({ to: contextHref(scope) });
    } catch (cause) { setError(cause?.code ?? 'COMPOSITION_ACTION_FAILED'); }
    finally { setPending(false); }
  };
  return h('section', { className: 'panel', 'aria-labelledby': 'context-heading' },
    h('h2', { id: 'context-heading' }, text['shell.contextTitle']),
    h('form', { onSubmit: submit },
      h('label', null, text['shell.contextTitle'],
        h('select', { value: kind, required: true, onChange: event => setKind(event.target.value) },
          h('option', { value: '' }, text['shell.chooseContext']),
          h('option', { value: 'platform' }, text['shell.platform']),
          h('option', { value: 'tenant' }, text['shell.tenantId']),
          h('option', { value: 'scope' }, text['shell.scopeId']))),
      kind && kind !== 'platform' ? h('label', null, text['shell.tenantId'],
        h('input', { type: 'text', required: true, value: tenantId, onChange: event => setTenantId(event.target.value) })) : null,
      kind === 'scope' ? h('label', null, text['shell.scopeId'],
        h('input', { type: 'text', required: true, value: scopeId, onChange: event => setScopeId(event.target.value) })) : null,
      error ? h('p', { role: 'alert' }, text['shell.actionFailed']) : null,
      h('button', { className: 'present-button-primary', type: 'submit', disabled: pending || !kind || session.getAuthStatus().phase === 'PENDING' || session.getAuthStatus().phase === 'UNKNOWN' || session.getConnectionState().transport !== 'HTTPS' || !session.getConnectionState().online },
        pending ? text['shell.loading'] : text['shell.useContext'])));
}

// Login : mot de passe jamais en state React, effacé du DOM après tentative ; UNKNOWN exige ressaisie.
function LoginForm() {
  const { session, text, setAuthAction, router } = useComposed();
  const subjectRef = useRef(null);
  const passwordRef = useRef(null);
  const [auth, setAuth] = useState(() => readAuth(session));
  const [error, setError] = useState(null);
  useEffect(() => session.subscribe(() => setAuth(readAuth(session))), [session]);
  const submit = async (event) => {
    event.preventDefault();
    const externalSubject = subjectRef.current?.value ?? '';
    const password = passwordRef.current?.value ?? '';
    if (passwordRef.current) passwordRef.current.value = ''; // purge immédiate du DOM
    setError(null);
    try {
      const scope = activeScope(session); // contexte explicite choisi au préalable
      setAuthAction('login');
      await session.login(scope, { external_subject: externalSubject, password });
      if (session.getState().state === 'ACTIVE') await router.navigate({ to: contextHref(session.getState().scope) });
    } catch (cause) {
      // UNKNOWN : le runtime conserve clef/empreinte, la ressaisie est exigée (champ déjà purgé).
      setError(cause?.code ?? 'COMPOSITION_ACTION_FAILED');
    }
  };
  return h('section', { className: 'panel', 'aria-labelledby': 'login-heading' },
    h('h1', { id: 'login-heading' }, text['shell.loginTitle']),
    auth.phase === 'PENDING' ? h('p', { role: 'status' }, text['shell.authPending']) : null,
    auth.phase === 'UNKNOWN' ? h('p', { role: 'alert' }, text['shell.authUnknownRetry']) : null,
    auth.phase === 'CONFIRMED' && auth.error_code ? h('p', { role: 'status' }, text['shell.auditPending']) : null,
    error ? h('p', { role: 'alert' }, text['shell.actionFailed']) : null,
    h('form', { onSubmit: submit },
      h('label', null, text['shell.externalSubject'],
        h('input', { ref: subjectRef, required: true, type: 'text', autoComplete: 'username' })),
      h('label', null, text['shell.password'],
        h('input', { ref: passwordRef, required: true, type: 'password', autoComplete: 'current-password' })),
      h('button', { className: 'present-button-primary', type: 'submit', disabled: auth.phase === 'PENDING' || session.getTargetScope() === null || session.getConnectionState().transport !== 'HTTPS' || !session.getConnectionState().online }, text['shell.submit'])));
}
function readAuth(session) { return session.getAuthStatus(); }
function contextHref(scope) {
  if (scope.scope_type === 'PLATFORM') return '/platform';
  return hrefFor(scope.scope_id === null ? '/tenants/{tenant_id}' : '/tenants/{tenant_id}/scopes/{scope_id}', scope);
}
function activeScope(session) {
  const state = session.getState();
  const scope = state.state === 'ACTIVE' ? state.scope : session.getTargetScope();
  if (scope === null) throw new Error('SESSION_CONTEXT_REQUIRED');
  return scope;
}
function ConnectionBanner() {
  const { session, text } = useComposed();
  const connection = session.getConnectionState();
  return h('div', null,
    !connection.online ? h('p', { role: 'alert' }, text['shell.offline']) : null,
    connection.transport !== 'HTTPS' ? h('p', { role: 'alert' }, text['shell.httpBlocked']) : null,
    connection.crossTab === 'UNAVAILABLE' ? h('p', { role: 'status' }, text['shell.crossTabUnavailable']) : null);
}

function navigationLabel(owner, key, locale) {
  const tables = composition.graph.contributions.filter(node => node.owner === owner && node.type === 'TRANSLATION');
  for (const node of tables) if (Object.hasOwn(node.payload.catalog[locale], key)) return fillText(node.payload.catalog[locale][key], {});
  throw new Error('COMPOSITION_LABEL_UNKNOWN');
}
function ComposedNavigation() {
  const { runtime, session, text, locale } = useComposed();
  const current = session.getState();
  const scope = current.state === 'ACTIVE' ? current.scope : null;
  let items = [];
  try { items = runtime.visibleNavigation(); } catch { return h('p', null, text['shell.routeUnavailable']); }
  if (!items.length) return null;
  return h('nav', { 'aria-label': text['shell.navigation'] }, h('ul', null, ...items.map(item => {
    const params = substituteRouteParams(item.payload.route, scope);
    if (params === null) return h('li', { key: item.owner + '/' + item.id }, h('span', null, text['shell.routeUnavailable']));
    return h('li', { key: item.owner + '/' + item.id },
      h(Link, { to: hrefFor(item.payload.route, params) }, navigationLabel(item.owner, item.payload.labelKey, locale)));
  })));
}

function ComposedRouteView({ owner, id }) {
  const { runtime, text, epoch } = useComposed();
  const params = useParams({ strict: false });
  let produced;
  try { produced = runtime.renderContribution(owner, id, params); }
  catch { return h('p', { role: 'alert' }, text['shell.routeUnavailable']); }
  return h('div', { key: epoch },
    h(PresentationView, { tree: produced.tree, ctx: produced.context, params, ancestors: [owner + '/' + id], instanceKey: owner + '/' + id }));
}
function ComposedHome() {
  const { text } = useComposed();
  return h('section', { className: 'panel' }, h('h1', null, text['shell.heading']), h(ContextChoice));
}
function ContextPage() {
  const { text, session } = useComposed();
  const state = session.getState();
  return h('section', { className: 'panel' },
    h('h1', null, text['shell.contextTitle']),
    h('p', { role: 'status' }, text['shell.session' + state.state]),
    h(ContextChoice));
}
function LoginPage() { return h('div', null, h(ContextChoice), h(LoginForm)); }
function RouteUnavailable() {
  const { text } = useComposed();
  return h('section', { className: 'panel' }, h('h1', null, text['shell.routeUnavailable']),
    h(Link, { to: '/login' }, text['shell.login']), h(ContextChoice));
}

function ComposedShell() {
  const env = useComposed();
  const { text, locale, setLocale, theme, setTheme, session } = env;
  const pathname = useRouterState({ select: state => state.location.pathname });
  useEffect(() => { document.getElementById('content')?.focus(); }, [pathname]);
  const sessionState = session.getState(), auth = session.getAuthStatus();
  const logout = async () => {
    try { env.setAuthAction('logout'); await session.logout(); } // UNKNOWN : même body conservé par la session ; audit pending distinct affiché
    catch (cause) { env.notifyError(cause?.code ?? 'COMPOSITION_ACTION_FAILED'); }
  };
  return h('div', { className: 'shell', 'data-mode': 'COMPOSED' },
    h('a', { className: 'skip-link', href: '#content' }, text['shell.skip']),
    h('header', { className: 'header' },
      h(Link, { className: 'brand', to: '/' }, text['shell.title']),
      h(Link, { to: '/login' }, text['shell.login']),
      h(ComposedNavigation, null),
      h(ComposedSlot, { key: env.epoch, point: 'pixs.shell.header', ancestors: [], instanceKey: 'header' }),
      h('div', { className: 'preferences' },
        h('label', null, text['shell.language'],
          h('select', { value: locale, onChange: event => setLocale(event.target.value) },
            h('option', { value: 'en' }, text['shell.english']),
            h('option', { value: 'fr' }, text['shell.french']))),
        h('label', null, text['shell.theme'],
          h('select', { value: theme, onChange: event => setTheme(event.target.value) },
            ...['system', 'light', 'dark'].map(value => h('option', { key: value, value }, text['shell.' + value])))),
        (sessionState.state === 'ACTIVE' || auth.phase === 'UNKNOWN' && env.authAction === 'logout') ? h('button', { type: 'button', onClick: logout, disabled: auth.phase === 'PENDING' || !session.getConnectionState().online }, text['shell.logout']) : null)),
    h(ConnectionBanner, null),
    h('p', { role: 'status' }, text['shell.session' + sessionState.state]),
    auth.phase === 'UNKNOWN' ? h('p', { role: 'alert' }, text['shell.authUnknownRetry']) : null,
    auth.error_code === 'SESSION_AUDIT_PENDING' ? h('p', { role: 'status' }, text['shell.auditPending']) : null,
    h(ComposedSlot, { key: 'nav-' + env.epoch, point: 'pixs.shell.navigation', ancestors: [], instanceKey: 'navigation' }),
    h('main', { id: 'content', tabIndex: -1 }, h(Outlet),
      h(ComposedSlot, { key: 'main-' + env.epoch, point: 'pixs.shell.main', ancestors: [], instanceKey: 'main' })),
    h('footer', null, text['shell.connectedFooter'],
      h(ComposedSlot, { key: 'footer-' + env.epoch, point: 'pixs.shell.footer', ancestors: [], instanceKey: 'footer' })));
}

function ComposedApp() {
  const [locale, setLocale] = useState(() => resolveLocale(navigator.languages));
  const [theme, setTheme] = useState('system');
  const localeRef = useRef(locale), routerRef = useRef(null);
  localeRef.current = locale;
  const [bus, setBus] = useState(null), [authAction, setAuthAction] = useState(null);
  const notifyError = useCallback(code => setBus(typeof code === 'string' ? code : 'COMPOSITION_ACTION_FAILED'), []);
  const [{ session, runtime }] = useState(() => createRuntimes(localeRef, notifyError, routerRef));
  const version = useSyncExternalStore(
    useCallback(notify => runtime.subscribe(notify), [runtime]),
    useCallback(() => runtime.getVersion(), [runtime]));
  const epoch = session.getState().epoch;
  const text = catalogs[locale];
  useEffect(() => {
    const online = () => session.setOnline(navigator.onLine);
    online();
    window.addEventListener('online', online);
    window.addEventListener('offline', online);
    return () => {
      window.removeEventListener('online', online); window.removeEventListener('offline', online);
      const errors = [];
      try { runtime.dispose(); } catch (cause) { errors.push(cause); }
      try { session.dispose(); } catch (cause) { errors.push(cause); }
      if (errors.length) throw new AggregateError(errors, 'SHELL_DISPOSE_FAILED');
    };
  }, [session, runtime]);
  useEffect(() => { runtime.refreshPresentation(); }, [locale, runtime]);
  useEffect(() => {
    document.documentElement.lang = locale;
    document.title = text['shell.title'];
  }, [locale, text]);
  useEffect(() => {
    const preference = window.matchMedia?.('(prefers-color-scheme: dark)');
    const apply = () => { document.documentElement.dataset.theme = theme === 'system' ? (preference?.matches ? 'dark' : 'light') : theme; };
    apply(); preference?.addEventListener('change', apply);
    return () => preference?.removeEventListener('change', apply);
  }, [theme]);
  const router = useMemo(() => {
    const root = createRootRoute({ component: ComposedShell, notFoundComponent: NotFound, errorComponent: RouteUnavailable });
    const fromParams = params => {
      if (params.tenant_id === undefined && params.scope_id !== undefined) throw new Error('SESSION_CONTEXT_REQUIRED');
      return params.tenant_id === undefined ? null
        : { scope_type: 'TENANT', tenant_id: params.tenant_id, scope_id: params.scope_id ?? null };
    };
    const leave = () => runtime.leaveRoute();
    const children = [
      createRoute({ getParentRoute: () => root, path: '/', beforeLoad: leave, component: ComposedHome }),
      createRoute({ getParentRoute: () => root, path: '/login', beforeLoad: leave, component: LoginPage }),
      ...['/platform', '/tenants/$tenant_id', '/tenants/$tenant_id/scopes/$scope_id'].map(path => createRoute({
        getParentRoute: () => root, path,
        beforeLoad: async ({ params }) => {
          leave();
          await session.load(fromParams(params) ?? { scope_type: 'PLATFORM', tenant_id: null, scope_id: null });
        },
        component: ContextPage, errorComponent: RouteUnavailable,
      })),
      // Toutes les routes du graphe sont enregistrées, même celles momentanément masquées.
      ...composition.graph.contributions.filter(node => node.type === 'ROUTE').map(node => createRoute({
        getParentRoute: () => root, path: toTanStack(node.payload.path),
        beforeLoad: async ({ params }) => {
          leave();
          if (node.activation_scope !== 'PUBLIC') {
            let scope = fromParams(params);
            if (scope === null && node.activation_scope === 'PLATFORM_SCOPED') scope = { scope_type: 'PLATFORM', tenant_id: null, scope_id: null };
            if (scope === null) scope = session.getState().state === 'ACTIVE' ? session.getState().scope : session.getTargetScope();
            if (scope === null || node.activation_scope === 'TENANT_SCOPED' && scope.scope_type !== 'TENANT') throw redirect({ to: '/login' });
            try { await session.load(scope); }
            catch (cause) {
              if (cause?.code === 'SESSION_CONTEXT_REFUSED') throw redirect({ to: '/login' });
              throw cause;
            }
          }
          runtime.openRoute(node.owner, node.id, params);
        },
        component: () => h(ComposedRouteView, { owner: node.owner, id: node.id }),
        errorComponent: RouteUnavailable,
      })),
    ];
    const built = createRouter({ routeTree: root.addChildren(children), defaultPreload: false });
    routerRef.current = built;
    return built;
  }, [session, runtime]);
  const env = { session, runtime, text, locale, setLocale, theme, setTheme, version, epoch, notifyError, authAction, setAuthAction, router };
  return h(Presentation.Provider, { value: env },
    h(ComposedContext.Provider, { value: env },
      bus ? h('p', { role: 'alert' }, text['shell.actionFailed']) : null,
      h(RouterProvider, { router })));
}

function StandaloneApp() {
  const [locale, setLocale] = useState(() => resolveLocale(navigator.languages));
  const [theme, setTheme] = useState('system');
  const text = catalogs[locale];
  useEffect(() => {
    document.documentElement.lang = locale;
    document.title = text['shell.title'];
  }, [locale, text]);
  useEffect(() => {
    const preference = window.matchMedia?.('(prefers-color-scheme: dark)');
    const apply = () => {
      document.documentElement.dataset.theme = theme === 'system' ? (preference?.matches ? 'dark' : 'light') : theme;
    };
    apply();
    preference?.addEventListener('change', apply);
    return () => preference?.removeEventListener('change', apply);
  }, [theme]);
  const router = useMemo(() => {
    const rootRoute = createRootRoute({ component: Shell, notFoundComponent: NotFound });
    const indexRoute = createRoute({ getParentRoute: () => rootRoute, path: '/', component: Home });
    return createRouter({ routeTree: rootRoute.addChildren([indexRoute]), defaultPreload: false });
  }, []);
  return h(Presentation.Provider, { value: { text, locale, setLocale, theme, setTheme } }, h(RouterProvider, { router }));
}

class BootstrapBoundary extends Component {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  render() {
    if (!this.state.failed) return this.props.children;
    const text = catalogs[resolveLocale(navigator.languages)];
    return h('main', { className: 'panel', role: 'alert' }, h('h1', null, text['shell.routeUnavailable']));
  }
}
createRoot(document.getElementById('root')).render(h(BootstrapBoundary, null, h(COMPOSED ? ComposedApp : StandaloneApp)));
