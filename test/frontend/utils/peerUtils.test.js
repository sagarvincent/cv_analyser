import { describe, it, expect } from 'vitest';
import { formatPeerDelta } from '../../../frontend/src/utils/peerUtils.js';

describe('formatPeerDelta', () => {
  it('returns "+2" when you=5 and p50=3', () => {
    expect(formatPeerDelta(5, 3)).toBe('+2');
  });

  it('returns "-2" when you=3 and p50=5', () => {
    expect(formatPeerDelta(3, 5)).toBe('-2');
  });

  it('returns "0" when you equals p50', () => {
    expect(formatPeerDelta(5, 5)).toBe('0');
  });

  it('returns "+10" for a larger positive delta', () => {
    expect(formatPeerDelta(15, 5)).toBe('+10');
  });
});
