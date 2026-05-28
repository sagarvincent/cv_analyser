// Layer: 3 — pure config, no JSX, no hooks

const MODE = import.meta.env.VITE_APP_MODE || 'dev_local';

if (!['dev_local', 'dev_cluster', 'production'].includes(MODE)) {
  console.warn(`[appConfig] Unknown VITE_APP_MODE "${MODE}", falling back to dev_local`);
}

// -------------------- appConfig ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: UploadScreen, any module that needs API or mock-data routing
export const appConfig = {
  mode: MODE,

  // true only in dev_local — skips all network calls and uses mockData instead
  useMockData: MODE === 'dev_local',

  // Base path for API calls.
  //   dev_local  : unused (useMockData is true)
  //   dev_cluster: '/api'  — Vite dev-server proxy forwards to VITE_DEV_BACKEND_URL
  //   production : absolute URL from VITE_API_BASE_URL env var
  apiBaseUrl: MODE === 'production'
    ? (import.meta.env.VITE_API_BASE_URL || '')
    : '/api',
};
// -------------------- appConfig ------------- END ----------------
