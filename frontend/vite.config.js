import { fileURLToPath } from 'node:url';
import { catalogs } from './src/catalogs.js';

if (Object.keys(catalogs.en).length !== Object.keys(catalogs.fr).length) {
  throw new Error('Invalid shell catalogue');
}

const frontendRoot = fileURLToPath(new URL('.', import.meta.url));

export default {
  root: frontendRoot,
  envDir: false,
  publicDir: false,
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    fs: { strict: true, allow: [frontendRoot] },
  },
  preview: { host: '127.0.0.1', port: 5173, strictPort: true },
};
