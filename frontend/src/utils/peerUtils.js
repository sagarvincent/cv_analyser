// Layer: Leaf — pure formatting for PeerModule. No JSX, no React.

// -------------------- formatPeerDelta ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: PeerModule
export function formatPeerDelta(you, p50) {
  const d = you - p50;
  return `${d > 0 ? '+' : ''}${d}`;
}
//-------------------- formatPeerDelta ------------- END ----------------
