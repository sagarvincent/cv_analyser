import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'url';
import fs from 'node:fs';

const fromFrontend = (p) => fileURLToPath(new URL(p, import.meta.url));

// Resolve TLS material for the dev server so the browser ↔ Vite leg is HTTPS.
// Paths come from env (VITE_SSL_CERT_FILE / VITE_SSL_KEY_FILE) and default to the
// repo-root certs/ dir. If either file is missing we return undefined so the dev
// server gracefully falls back to HTTP instead of crashing — Vite auto-upgrades
// HMR to wss whenever server.https is set.
const resolveHttps = (certFile, keyFile) => {
  if (!certFile || !keyFile || !fs.existsSync(certFile) || !fs.existsSync(keyFile)) {
    console.warn(
      '[vite] TLS cert/key not found — serving dev server over HTTP. ' +
        'Set VITE_SSL_CERT_FILE / VITE_SSL_KEY_FILE (see certs/README.md) to enable HTTPS.',
    );
    return undefined;
  }
  return { cert: fs.readFileSync(certFile), key: fs.readFileSync(keyFile) };
};

export default defineConfig(({ mode }) => {
  // Load .env.<mode> so proxy config can read VITE_DEV_BACKEND_URL at build time
  const env = loadEnv(mode, process.cwd(), '');
  // process.env takes precedence so Docker env vars override the .env file
  const devBackendUrl = process.env.VITE_DEV_BACKEND_URL || env.VITE_DEV_BACKEND_URL || 'http://localhost:8010';

  const certFile = process.env.VITE_SSL_CERT_FILE || env.VITE_SSL_CERT_FILE || fromFrontend('../certs/fullchain.pem');
  const keyFile = process.env.VITE_SSL_KEY_FILE || env.VITE_SSL_KEY_FILE || fromFrontend('../certs/privkey.pem');
  const https = resolveHttps(certFile, keyFile);

  return {
    plugins: [react()],
    resolve: {
      alias: [
        // Tests live in ../test/frontend/, outside the frontend/ root.
        // Map the testing-library packages to frontend/node_modules so node
        // resolution from sibling test files succeeds.
        { find: '@testing-library/react', replacement: fromFrontend('./node_modules/@testing-library/react') },
        { find: '@testing-library/jest-dom', replacement: fromFrontend('./node_modules/@testing-library/jest-dom') },
      ],
    },
    server: {
      // Serve the dev server over HTTPS when certs are available (see resolveHttps).
      https,
      fs: {
        allow: ['..'],
      },
      // Only proxy in dev_cluster mode — dev_local has no backend, production
      // uses direct absolute URLs set via VITE_API_BASE_URL.
      proxy: mode === 'dev_cluster' ? { '/api': devBackendUrl } : {},
    },
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: ['./vitest.setup.js'],
      include: ['../test/frontend/**/*.test.{js,jsx}'],
      reporters: ['verbose'],
      coverage: {
        provider: 'v8',
        include: ['src/utils/**', 'src/components/ui/**'],
        reporter: ['text', 'html', 'json-summary'],
      },
    },
  };
});
