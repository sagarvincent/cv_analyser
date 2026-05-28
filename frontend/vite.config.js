import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'url';

const fromFrontend = (p) => fileURLToPath(new URL(p, import.meta.url));

export default defineConfig(({ mode }) => {
  // Load .env.<mode> so proxy config can read VITE_DEV_BACKEND_URL at build time
  const env = loadEnv(mode, process.cwd(), '');
  // process.env takes precedence so Docker env vars override the .env file
  const devBackendUrl = process.env.VITE_DEV_BACKEND_URL || env.VITE_DEV_BACKEND_URL || 'http://localhost:8001';

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
