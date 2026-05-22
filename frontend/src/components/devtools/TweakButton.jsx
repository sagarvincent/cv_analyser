// Layer: 2 (devtools sub-component) — pure rendering
// -------------------- TweakButton ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: App
export function TweakButton({ label, onClick }) {
  return <button type="button" className="twk-btn" onClick={onClick}>{label}</button>;
}
//-------------------- TweakButton ------------- END ----------------
