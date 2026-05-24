import { describe, it, expect } from 'vitest';
import { buildSparklineGeometry } from '../../../frontend/src/utils/sparklineUtils.js';

describe('buildSparklineGeometry', () => {
  it('returns an object with pts, lastX, lastY', () => {
    const result = buildSparklineGeometry([1, 2, 3], 100, 50);
    expect(result).toHaveProperty('pts');
    expect(result).toHaveProperty('lastX');
    expect(result).toHaveProperty('lastY');
  });

  it('lastX equals width', () => {
    const { lastX } = buildSparklineGeometry([1, 2, 3], 100, 50);
    expect(lastX).toBeCloseTo(100);
  });

  it('lastY is 0 when the last value is the maximum (top of SVG)', () => {
    const { lastY } = buildSparklineGeometry([0, 5, 10], 100, 50);
    expect(lastY).toBeCloseTo(0);
  });

  it('lastY equals height when the last value is the minimum', () => {
    const { lastY } = buildSparklineGeometry([10, 5, 0], 100, 50);
    expect(lastY).toBeCloseTo(50);
  });

  it('pts has one coordinate pair per data point', () => {
    const data = [1, 2, 3, 4, 5];
    const { pts } = buildSparklineGeometry(data, 100, 50);
    const pairs = pts.trim().split(' ');
    expect(pairs).toHaveLength(data.length);
  });

  it('edge case: all-equal values do not throw (range defaults to 1)', () => {
    expect(() => buildSparklineGeometry([5, 5, 5], 100, 50)).not.toThrow();
  });

  it('edge case: all-equal values return valid lastX and lastY', () => {
    const { lastX, lastY } = buildSparklineGeometry([5, 5, 5], 100, 50);
    expect(Number.isFinite(lastX)).toBe(true);
    expect(Number.isFinite(lastY)).toBe(true);
  });
});
