import { describe, it, expect } from 'vitest';
import { formatStrengthPct, impactTone } from '../../../frontend/src/utils/jdFitUtils.js';

describe('formatStrengthPct', () => {
  it('converts 0.75 to 75', () => {
    expect(formatStrengthPct(0.75)).toBe(75);
  });

  it('converts 0 to 0', () => {
    expect(formatStrengthPct(0)).toBe(0);
  });

  it('converts 1 to 100', () => {
    expect(formatStrengthPct(1)).toBe(100);
  });

  it('rounds 0.999 to 100', () => {
    expect(formatStrengthPct(0.999)).toBe(100);
  });

  it('rounds 0.504 to 50', () => {
    expect(formatStrengthPct(0.504)).toBe(50);
  });

  it('rounds 0.505 to 51', () => {
    expect(formatStrengthPct(0.505)).toBe(51);
  });
});

describe('impactTone', () => {
  it('returns "bad" for "HIGH"', () => {
    expect(impactTone('HIGH')).toBe('bad');
  });

  it('returns "warn" for "MED"', () => {
    expect(impactTone('MED')).toBe('warn');
  });

  it('returns "muted" for "LOW"', () => {
    expect(impactTone('LOW')).toBe('muted');
  });

  it('returns "muted" for any unknown string', () => {
    expect(impactTone('CRITICAL')).toBe('muted');
    expect(impactTone('')).toBe('muted');
  });
});
