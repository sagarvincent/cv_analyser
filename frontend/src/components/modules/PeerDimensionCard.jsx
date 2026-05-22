// Layer: 2 (module sub-component) — one peer dimension card (you, p50, bar, delta)
import { Bar } from '../ui';
import { formatPeerDelta } from '../../utils/peerUtils';

// -------------------- PeerDimensionCard ----------- START ----------
// -- Calls : Bar, formatPeerDelta
// -- Called by: PeerModule
export function PeerDimensionCard({ dim, isLast }) {
  return (
    <div style={{
      padding: 22, background: 'var(--surface)',
      borderRight: isLast ? 'none' : '1px solid var(--border)',
    }}>
      <div className="t-label" style={{ marginBottom: 14 }}>{dim.dim}</div>
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 10 }}>
        <span className="t-num" style={{ fontSize: 32, color: 'var(--accent)' }}>{dim.you}</span>
        <span className="t-mono" style={{ fontSize: 11, color: 'var(--muted)' }}>P50 · {dim.p50}</span>
      </div>
      <Bar value={dim.you} tone="accent" height={3} />
      <div style={{ marginTop: 8, fontSize: 11, color: 'var(--muted)' }}>{formatPeerDelta(dim.you, dim.p50)} vs median</div>
    </div>
  );
}
//-------------------- PeerDimensionCard ------------- END ----------------
