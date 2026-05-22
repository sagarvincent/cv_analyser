// Layer: 1 (module screen) — peer comparison module
import { Card, SectionHeader } from '../ui';
import { Distribution } from '../charts';
import { PeerDimensionCard } from './PeerDimensionCard';
import { peerSummary, peerBuckets, peerYouBucket, peerP50Bucket, peerDimensions } from '../../data/mockData';

// -------------------- PeerModule ----------- START ----------
// -- Calls : SectionHeader, Card, Distribution, PeerDimensionCard
// -- Called by: App (via MODULE_COMPONENTS)
export function PeerModule({ chartStyle }) {
  return (
    <div className="fade-in">
      <SectionHeader
        eyebrow={peerSummary.eyebrow}
        title={
          <>You sit at the <span className="t-italic" style={{ color: 'var(--accent)' }}>{peerSummary.titlePercentile}</span></>
        }
        sub={peerSummary.sub}
      />

      <Card eyebrow="DISTRIBUTION" title="Overall composite score · your cohort">
        <div style={{ padding: '8px 0' }}>
          <Distribution buckets={peerBuckets} you={peerYouBucket} p50={peerP50Bucket} label={['LOW', 'HIGH']} chartStyle={chartStyle} />
        </div>
      </Card>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 0, marginTop: 24, border: '1px solid var(--border)', borderRadius: 8, overflow: 'hidden' }}>
        {peerDimensions.map((d, i) => (
          <PeerDimensionCard key={d.dim} dim={d} isLast={i === peerDimensions.length - 1} />
        ))}
      </div>
    </div>
  );
}
//-------------------- PeerModule ------------- END ----------------
