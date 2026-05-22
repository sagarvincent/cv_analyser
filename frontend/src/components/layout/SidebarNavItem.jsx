// Layer: 2 (layout sub-component) — single module nav button in the Sidebar

// -------------------- SidebarNavItem ----------- START ----------
// -- Calls : nothing (leaf render)
// -- Called by: Sidebar
export function SidebarNavItem({ module, isActive, onClick }) {
  return (
    <button onClick={onClick}
      style={{
        display: 'flex', alignItems: 'center', gap: 12, width: '100%',
        padding: '10px 14px', marginBottom: 1,
        background: isActive ? 'var(--surface-2)' : 'transparent',
        border: 0,
        borderLeft: `2px solid ${isActive ? 'var(--accent)' : 'transparent'}`,
        color: isActive ? 'var(--text)' : 'var(--text-2)',
        fontSize: 13, cursor: 'pointer', textAlign: 'left',
        fontFamily: 'var(--font-sans)',
        transition: '120ms ease',
      }}
      onMouseEnter={(e) => { if (!isActive) e.currentTarget.style.background = 'var(--surface)'; }}
      onMouseLeave={(e) => { if (!isActive) e.currentTarget.style.background = 'transparent'; }}
    >
      <span className="t-mono" style={{ fontSize: 10, color: isActive ? 'var(--accent)' : 'var(--muted)', letterSpacing: '0.08em', minWidth: 18 }}>
        {module.code}
      </span>
      <span style={{ flex: 1 }}>{module.label}</span>
      {isActive && <span style={{ color: 'var(--accent)', fontSize: 11 }}>●</span>}
    </button>
  );
}
//-------------------- SidebarNavItem ------------- END ----------------
