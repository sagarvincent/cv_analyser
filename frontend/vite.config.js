import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'url';

const fromFrontend = (p) => fileURLToPath(new URL(p, import.meta.url));

export default defineConfig({
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
});
