const entries = [
  ['shell.title', 'Pixs', 'Pixs'],
  ['shell.skip', 'Skip to content', 'Aller au contenu'],
  ['shell.development', 'Local development', 'Développement local'],
  ['shell.heading', 'Your application starts here', 'Votre application commence ici'],
  ['shell.description', 'The initial interface is available. Application services are not connected yet.', 'L’interface initiale est disponible. Les services applicatifs ne sont pas encore connectés.'],
  ['shell.language', 'Language', 'Langue'],
  ['shell.english', 'English', 'Anglais'],
  ['shell.french', 'French', 'Français'],
  ['shell.theme', 'Appearance', 'Apparence'],
  ['shell.system', 'System', 'Système'],
  ['shell.light', 'Light', 'Clair'],
  ['shell.dark', 'Dark', 'Sombre'],
  ['shell.notFound', 'Page unavailable', 'Page indisponible'],
  ['shell.notFoundDescription', 'This address is not part of the initial interface.', 'Cette adresse ne fait pas partie de l’interface initiale.'],
  ['shell.home', 'Back to home', 'Retour à l’accueil'],
  ['shell.footer', 'No application data is loaded by this interface.', 'Cette interface ne charge aucune donnée applicative.'],
];

export function createCatalogs(source) {
  if (!Array.isArray(source) || source.length === 0) {
    throw new Error('Invalid shell catalogue');
  }
  const en = Object.create(null);
  const fr = Object.create(null);
  for (const entry of source) {
    if (!Array.isArray(entry) || entry.length !== 3 ||
        typeof entry[0] !== 'string' || !/^shell\.[a-zA-Z]+$/.test(entry[0]) ||
        Object.hasOwn(en, entry[0]) ||
        entry.slice(1).some(value => typeof value !== 'string' || value.trim() === '')) {
      throw new Error('Invalid shell catalogue');
    }
    en[entry[0]] = entry[1];
    fr[entry[0]] = entry[2];
  }
  return Object.freeze({ en: Object.freeze(en), fr: Object.freeze(fr) });
}

export const catalogs = createCatalogs(entries);

export function resolveLocale(preferences = [], fallback = 'en') {
  if (!Object.hasOwn(catalogs, fallback) || !Array.isArray(preferences)) {
    throw new Error('Invalid shell locale');
  }
  for (const preference of preferences) {
    if (typeof preference !== 'string') continue;
    const language = preference.toLowerCase().split('-')[0];
    if (Object.hasOwn(catalogs, language)) return language;
  }
  return fallback;
}
