// Layer: 2 (UI sub-component) — pure rendering
// -------------------- Pill ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: OverviewModule, JDFitModule, TopBar, UploadScreen, ProfilePage
export function Pill({ tone = 'default', children, dot = false }) {
  const cls = `pill ${tone !== 'default' ? `pill-${tone}` : ''} ${dot ? 'pill-dot' : ''}`;
  return <span className={cls}>{children}</span>;
}
//-------------------- Pill ------------- END ----------------
