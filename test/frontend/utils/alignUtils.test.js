import { describe, it, expect } from 'vitest';
import {
  calcAlignDelta,
  alignDeltaTone,
  formatAlignDelta,
  buildAlignRows,
} from '../../../frontend/src/utils/alignUtils.js';

describe('calcAlignDelta', () => {
  it('returns you - market', () => {
    expect(calcAlignDelta(0.8, 0.6)).toBeCloseTo(0.2);
  });

  it('returns negative delta when you < market', () => {
    expect(calcAlignDelta(0.4, 0.6)).toBeCloseTo(-0.2);
  });

  it('returns 0 when values are equal', () => {
    expect(calcAlignDelta(0.5, 0.5)).toBe(0);
  });
});

describe('alignDeltaTone', () => {
  it('returns "good" when delta > 0.1', () => {
    expect(alignDeltaTone(0.2)).toBe('good');
  });

  it('returns "bad" when delta < -0.1', () => {
    expect(alignDeltaTone(-0.2)).toBe('bad');
  });

  it('returns "muted" when delta is within [-0.1, 0.1]', () => {
    expect(alignDeltaTone(0.05)).toBe('muted');
    expect(alignDeltaTone(-0.05)).toBe('muted');
    expect(alignDeltaTone(0)).toBe('muted');
  });

  it('returns "muted" at boundary value 0.1 (not strictly greater)', () => {
    expect(alignDeltaTone(0.1)).toBe('muted');
  });

  it('returns "muted" at boundary value -0.1 (not strictly less)', () => {
    expect(alignDeltaTone(-0.1)).toBe('muted');
  });
});

describe('formatAlignDelta', () => {
  it('prepends "+" for positive delta', () => {
    expect(formatAlignDelta(0.155)).toBe('+16');
  });

  it('shows sign naturally for negative delta', () => {
    expect(formatAlignDelta(-0.15)).toBe('-15');
  });

  it('returns "0" for zero delta', () => {
    expect(formatAlignDelta(0)).toBe('0');
  });

  it('rounds correctly', () => {
    expect(formatAlignDelta(0.005)).toBe('+1');
  });
});

describe('buildAlignRows', () => {
  const axes = ['Communication', 'Leadership', 'Technical'];
  const you = [0.9, 0.5, 0.7];
  const market = [0.7, 0.6, 0.7];

  it('returns an array with length equal to axes.length', () => {
    const rows = buildAlignRows(axes, you, market);
    expect(rows).toHaveLength(axes.length);
  });

  it('each row has all required keys', () => {
    const rows = buildAlignRows(axes, you, market);
    const requiredKeys = ['axis', 'youValue', 'delta', 'tone', 'barTone', 'deltaFmt', 'deltaColor'];
    rows.forEach(row => {
      requiredKeys.forEach(key => expect(row).toHaveProperty(key));
    });
  });

  it('barTone is "accent" when tone is "muted"', () => {
    const rows = buildAlignRows(['A'], [0.7], [0.7]);
    expect(rows[0].tone).toBe('muted');
    expect(rows[0].barTone).toBe('accent');
  });

  it('barTone equals tone when tone is "good"', () => {
    const rows = buildAlignRows(['A'], [0.9], [0.7]);
    expect(rows[0].tone).toBe('good');
    expect(rows[0].barTone).toBe('good');
  });

  it('barTone equals tone when tone is "bad"', () => {
    const rows = buildAlignRows(['A'], [0.5], [0.7]);
    expect(rows[0].tone).toBe('bad');
    expect(rows[0].barTone).toBe('bad');
  });

  it('deltaColor is var(--good) when delta is positive', () => {
    const rows = buildAlignRows(['A'], [0.9], [0.7]);
    expect(rows[0].deltaColor).toBe('var(--good)');
  });

  it('deltaColor is var(--bad) when delta is negative', () => {
    const rows = buildAlignRows(['A'], [0.5], [0.7]);
    expect(rows[0].deltaColor).toBe('var(--bad)');
  });

  it('axis value matches input axes label', () => {
    const rows = buildAlignRows(axes, you, market);
    rows.forEach((row, i) => expect(row.axis).toBe(axes[i]));
  });
});
