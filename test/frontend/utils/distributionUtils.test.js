import { describe, it, expect } from 'vitest';
import {
  distributionBarFill,
  buildDistributionGeometry,
} from '../../../frontend/src/utils/distributionUtils.js';

describe('distributionBarFill', () => {
  it('returns var(--accent) when isYou=true', () => {
    expect(distributionBarFill(true, false)).toBe('var(--accent)');
  });

  it('returns var(--warn) when isP50=true and isYou=false', () => {
    expect(distributionBarFill(false, true)).toBe('var(--warn)');
  });

  it('returns var(--muted-2) when both are false', () => {
    expect(distributionBarFill(false, false)).toBe('var(--muted-2)');
  });

  it('isYou takes priority over isP50', () => {
    expect(distributionBarFill(true, true)).toBe('var(--accent)');
  });
});

describe('buildDistributionGeometry', () => {
  const buckets = [2, 5, 8, 6, 3];
  const you = 2;
  const p50 = 3;
  const W = 300, H = 200, padL = 20, padR = 20, padT = 10, padB = 10;

  it('returns the correct number of bars', () => {
    const { bars } = buildDistributionGeometry(buckets, you, p50, W, H, padL, padR, padT, padB);
    expect(bars).toHaveLength(buckets.length);
  });

  it('marks the correct bar as isYou', () => {
    const { bars } = buildDistributionGeometry(buckets, you, p50, W, H, padL, padR, padT, padB);
    expect(bars[you].isYou).toBe(true);
    expect(bars.filter(b => b.isYou)).toHaveLength(1);
  });

  it('marks the correct bar as isP50', () => {
    const { bars } = buildDistributionGeometry(buckets, you, p50, W, H, padL, padR, padT, padB);
    expect(bars[p50].isP50).toBe(true);
    expect(bars.filter(b => b.isP50)).toHaveLength(1);
  });

  it('computes bw as innerW / buckets.length', () => {
    const { bw } = buildDistributionGeometry(buckets, you, p50, W, H, padL, padR, padT, padB);
    const innerW = W - padL - padR;
    expect(bw).toBeCloseTo(innerW / buckets.length);
  });

  it('computes youLabelX as padL + (you + 0.5) * bw', () => {
    const { bw, youLabelX } = buildDistributionGeometry(buckets, you, p50, W, H, padL, padR, padT, padB);
    expect(youLabelX).toBeCloseTo(padL + (you + 0.5) * bw);
  });

  it('each bar has all required keys', () => {
    const { bars } = buildDistributionGeometry(buckets, you, p50, W, H, padL, padR, padT, padB);
    const requiredKeys = ['v', 'i', 'h', 'x', 'y', 'cx', 'isYou', 'isP50', 'fill', 'dotCount', 'dotPositions'];
    bars.forEach(bar => {
      requiredKeys.forEach(key => expect(bar).toHaveProperty(key));
    });
  });

  it('bar with maximum bucket value has h equal to innerH', () => {
    const innerH = H - padT - padB;
    const maxIndex = buckets.indexOf(Math.max(...buckets));
    const { bars } = buildDistributionGeometry(buckets, you, p50, W, H, padL, padR, padT, padB);
    expect(bars[maxIndex].h).toBeCloseTo(innerH);
  });
});
