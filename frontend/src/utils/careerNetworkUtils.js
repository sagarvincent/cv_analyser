// Layer: Leaf — pure geometry and color utilities for CareerNetwork. No JSX, no React.

// -------------------- colorForFit ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: CareerNetwork
export function colorForFit(fit) {
  return fit > 0.85 ? 'var(--accent)'
    : fit > 0.7  ? 'var(--good)'
    : fit > 0.55 ? 'var(--warn)'
    : 'var(--muted)';
}
//-------------------- colorForFit ------------- END ----------------

// -------------------- findPlacedNode ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: CareerNetwork
export function findPlacedNode(placed, id, cx, cy) {
  return placed.find(n => n.id === id) || { x: cx, y: cy };
}
//-------------------- findPlacedNode ------------- END ----------------

// -------------------- placeOnRing ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: buildCareerNetworkLayout
export function placeOnRing(arr, R, cx, cy, offset = 0) {
  return arr.map((n, i) => {
    const a = (i / arr.length) * Math.PI * 2 + offset;
    return { ...n, x: cx + Math.cos(a) * R, y: cy + Math.sin(a) * R };
  });
}
//-------------------- placeOnRing ------------- END ----------------

// -------------------- buildCareerNetworkLayout ----------- START ----------
// -- Calls : placeOnRing
// -- Called by: CareerNetwork
export function buildCareerNetworkLayout(nodes, W, H) {
  const cx = W / 2, cy = H / 2;
  const ring1R = 130, ring2R = 215;
  const r1 = nodes.filter(n => n.ring === 1);
  const r2 = nodes.filter(n => n.ring === 2);
  const placed = [
    ...placeOnRing(r1, ring1R, cx, cy, -Math.PI / 2),
    ...placeOnRing(r2, ring2R, cx, cy, -Math.PI / 2 + Math.PI / r2.length),
  ];
  return { placed, cx, cy, ring1R, ring2R };
}
//-------------------- buildCareerNetworkLayout ------------- END ----------------

// -------------------- calcNodeRadius ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: CareerNetwork
export function calcNodeRadius(fit, chartStyle) {
  return chartStyle === 'dots' ? 8 + fit * 12 : 22;
}
//-------------------- calcNodeRadius ------------- END ----------------

// -------------------- formatFitPct ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: CareerNetworkNode
export function formatFitPct(fit) {
  return Math.round(fit * 100);
}
//-------------------- formatFitPct ------------- END ----------------

// -------------------- resolveLinkEndpoints ----------- START ----------
// -- Calls : findPlacedNode
// -- Called by: CareerNetwork
export function resolveLinkEndpoints(link, placed, cx, cy) {
  const a = link.from === 'center' ? { x: cx, y: cy } : findPlacedNode(placed, link.from, cx, cy);
  const b = findPlacedNode(placed, link.to, cx, cy);
  return { a, b };
}
//-------------------- resolveLinkEndpoints ------------- END ----------------

// -------------------- calcLinkStrokeWidth ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: CareerNetworkLink
export function calcLinkStrokeWidth(fit) {
  return 0.5 + (fit ?? 0.5) * 1.5;
}
//-------------------- calcLinkStrokeWidth ------------- END ----------------
