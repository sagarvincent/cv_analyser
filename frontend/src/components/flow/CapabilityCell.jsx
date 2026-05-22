// Layer: 2 (flow sub-component) — one number+label cell in the UploadScreen capability strip

// -------------------- CapabilityCell ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: UploadScreen
export function CapabilityCell({ value, label }) {
  return (
    <div style={{ padding: '22px 18px', borderRight: '1px solid var(--border)' }}>
      <div className="t-num" style={{ fontSize: 34, lineHeight: 1 }}>{value}</div>
      <div className="t-label" style={{ marginTop: 8 }}>{label}</div>
    </div>
  );
}
//-------------------- CapabilityCell ------------- END ----------------
