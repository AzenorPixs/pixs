import { createElement as h, createContext, useContext, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { createRootRoute, createRoute, createRouter, Link, Outlet, RouterProvider } from '@tanstack/react-router';
import { catalogs, resolveLocale } from './catalogs.js';
import './theme.css';

const Presentation = createContext(null);
const usePresentation = () => useContext(Presentation);

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

const rootRoute = createRootRoute({ component: Shell, notFoundComponent: NotFound });
const indexRoute = createRoute({ getParentRoute: () => rootRoute, path: '/', component: Home });
const router = createRouter({ routeTree: rootRoute.addChildren([indexRoute]), defaultPreload: false });

function App() {
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
  return h(Presentation.Provider, { value: { text, locale, setLocale, theme, setTheme } }, h(RouterProvider, { router }));
}

createRoot(document.getElementById('root')).render(h(App));
