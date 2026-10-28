import { fileURLToPath } from 'node:url';
import { types as utilTypes } from 'node:util';
import { catalogs } from './src/catalogs.js';
import { createPixsCompositionPlugin } from './scripts/pixs-composition-plugin-v1.mjs';

if (Object.keys(catalogs.en).length !== Object.keys(catalogs.fr).length) {
  throw new Error('Invalid shell catalogue');
}

const frontendRoot = fileURLToPath(new URL('.', import.meta.url));

export function createFrontendViteConfig(options) {
  if (options === null || typeof options !== 'object' || Array.isArray(options)
      || utilTypes.isProxy(options) || ![Object.prototype, null].includes(Object.getPrototypeOf(options))
      || Reflect.ownKeys(options).length !== 2) throw new Error('PLUGIN_OPTIONS_INVALID');
  const modeDescriptor = Object.getOwnPropertyDescriptor(options, 'mode');
  const compositionDescriptor = Object.getOwnPropertyDescriptor(options, 'composition');
  if (!modeDescriptor || !Object.hasOwn(modeDescriptor, 'value')
      || !compositionDescriptor || !Object.hasOwn(compositionDescriptor, 'value')) throw new Error('PLUGIN_OPTIONS_INVALID');
  const mode = modeDescriptor.value;
  const composition = compositionDescriptor.value;
  if (mode !== 'STANDALONE' && mode !== 'COMPOSED') throw new Error('PLUGIN_MODE_INVALID');
  if (mode === 'STANDALONE' && composition !== null) throw new Error('PLUGIN_OPTIONS_INVALID');
  const plugin = createPixsCompositionPlugin({ mode, composition });
  const config = {
    root: frontendRoot,
    envDir: false,
    envPrefix: [],
    publicDir: false,
    server: {
      host: '127.0.0.1',
      port: 5173,
      strictPort: true,
      fs: { strict: true, allow: [frontendRoot] },
    },
    preview: { host: '127.0.0.1', port: 5173, strictPort: true },
    build: {
      sourcemap: false,
      assetsInlineLimit: 0,
      rolldownOptions: { output: { codeSplitting: false } },
    },
    plugins: [plugin],
  };
  if (mode === 'COMPOSED') {
    config.optimizeDeps = { noDiscovery: true, include: ['react', 'react-dom/client', '@tanstack/react-router'] };
    config.server.hmr = false;
  }
  return config;
}

export default createFrontendViteConfig({ mode: 'STANDALONE', composition: null });
