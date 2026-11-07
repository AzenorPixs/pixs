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
  ["shell.login", "Sign in", "Connexion"],
  ["shell.loginTitle", "Sign in", "Connexion"],
  ["shell.logout", "Sign out", "Déconnexion"],
  ["shell.submit", "Sign in", "Se connecter"],
  ["shell.externalSubject", "Account", "Compte"],
  ["shell.password", "Password", "Mot de passe"],
  ["shell.contextTitle", "Application context", "Contexte applicatif"],
  ["shell.platform", "Platform", "Plateforme"],
  ["shell.tenantId", "Tenant reference", "Référence du tenant"],
  ["shell.scopeId", "Scope reference", "Référence du scope"],
  ["shell.useContext", "Load context", "Charger le contexte"],
  ["shell.chooseContext", "Choose a context", "Choisir un contexte"],
  ["shell.loading", "Loading…", "Chargement…"],
  ["shell.navigation", "Application navigation", "Navigation de l’application"],
  ["shell.offline", "Offline. Reconnect before accessing application data.", "Hors ligne. Reconnectez-vous avant d’accéder aux données applicatives."],
  ["shell.httpBlocked", "Application data requires HTTPS.", "L’accès aux données applicatives exige HTTPS."],
  ["shell.crossTabUnavailable", "Cross-tab coordination is unavailable. Server requests still verify the session.", "La coordination entre onglets est indisponible. Les requêtes serveur vérifient toujours la session."],
  ["shell.authPending", "Checking authentication…", "Vérification de l’authentification…"],
  ["shell.authUnknownRetry", "Outcome unknown. Retry the same operation with the same values.", "Résultat inconnu. Réessayez la même opération avec les mêmes valeurs."],
  ["shell.auditPending", "Signed out; audit recording is pending.", "Déconnexion effectuée ; l’enregistrement de l’audit reste en attente."],
  ["shell.routeUnavailable", "Page unavailable for this context.", "Page indisponible dans ce contexte."],
  ["shell.componentUnavailable", "This content is unavailable.", "Ce contenu est indisponible."],
  ["shell.fieldAdd", "Add item", "Ajouter un élément"],
  ["shell.fieldRemove", "Remove item", "Supprimer l’élément"],
  ["shell.stateIDLE", "Ready.", "Prêt."],
  ["shell.statePENDING", "In progress…", "En cours…"],
  ["shell.stateLOADED", "Data loaded.", "Données chargées."],
  ["shell.stateCONFIRMED", "Operation confirmed.", "Opération confirmée."],
  ["shell.stateREJECTED", "Operation refused.", "Opération refusée."],
  ["shell.stateUNKNOWN", "Outcome unknown. Retry only the same operation.", "Résultat inconnu. Réessayez uniquement la même opération."],
  ["shell.stateUNAVAILABLE", "Operation unavailable.", "Opération indisponible."],
  ["shell.sessionINITIALIZING", "Checking session…", "Vérification de la session…"],
  ["shell.sessionANONYMOUS", "Not signed in.", "Non connecté."],
  ["shell.sessionACTIVE", "Verified session.", "Session vérifiée."],
  ["shell.sessionEXPIRED", "Session expired.", "Session expirée."],
  ["shell.sessionREVOKED", "Session revoked.", "Session révoquée."],
  ["shell.sessionERROR", "Session unavailable. Reload the selected context.", "Session indisponible. Rechargez le contexte choisi."],
  ["shell.connectedFooter", "Application data belongs to the verified session and selected context.", "Les données applicatives dépendent de la session vérifiée et du contexte choisi."],
  ["shell.actionFailed", "The result could not be verified. Check the operation status and session before retrying.", "Le résultat n’a pas pu être vérifié. Consultez l’état de l’opération et la session avant de réessayer."],
  ["shell.stateINVALID", "Check the entered values.", "Vérifiez les valeurs saisies."],
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
