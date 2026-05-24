import { describe, it, expect } from 'vitest';
import {
  calcRadarAngle,
  calcRadarPoint,
  buildRadarPath,
  buildRadarGeometry,
} from '../../../frontend/src/utils/radarUtils.js';

describe('calcRadarAngle', () => {
  it('returns -π/2 when i=0 for any n', () => {
    expect(calcRadarAngle(0, 4)).toBeCloseTo(-Math.PI / 2);
    expect(calcRadarAngle(0, 6)).toBeCloseTo(-Math.PI / 2);
  });

  it('distributes angles evenly across a full circle', () => {
    const n = 4;
    const a0 = calcRadarAngle(0, n);
    const a1 = calcRadarAngle(1, n);
    expect(a1 - a0).toBeCloseTo(Math.PI / 2);
  });

  it('completes a full circle after n steps', () => {
    const n = 6;
    const a0 = calcRadarAngle(0, n);
    const aN = calcRadarAngle(n, n);
    expect(aN - a0).toBeCloseTo(Math.PI * 2);
  });
});

describe('calcRadarPoint', () => {
  it('returns [cx, cy] when v=0', () => {
    const [x, y] = calcRadarPoint(0, 0, 100, 100, 50, 4);
    expect(x).toBeCloseTo(100);
    expect(y).toBeCloseTo(100);
  });

  it('returns [cx, cy-R] at i=0, v=1 (pointing straight up)', () => {
    const [x, y] = calcRadarPoint(0, 1, 100, 100, 50, 4);
    expect(x).toBeCloseTo(100);
    expect(y).toBeCloseTo(50);
  });

  it('returns an array of length 2', () => {
    const pt = calcRadarPoint(0, 0.5, 100, 100, 50, 4);
    expect(pt).toHaveLength(2);
  });
});

describe('buildRadarPath', () => {
  it('starts with "M "', () => {
    const path = buildRadarPath([0.5, 0.8, 0.6], 100, 100, 50, 3);
    expect(path.startsWith('M ')).toBe(true);
  });

  it('ends with " Z"', () => {
    const path = buildRadarPath([0.5, 0.8, 0.6], 100, 100, 50, 3);
    expect(path.endsWith(' Z')).toBe(true);
  });

  it('contains the correct number of " L " separators', () => {
    const values = [0.5, 0.8, 0.6, 0.4];
    const path = buildRadarPath(values, 100, 100, 50, 4);
    const separators = path.split(' L ').length - 1;
    expect(separators).toBe(values.length - 1);
  });

  it('single-value array produces no " L " separators', () => {
    const path = buildRadarPath([0.5], 100, 100, 50, 1);
    expect(path.includes(' L ')).toBe(false);
  });
});

describe('buildRadarGeometry', () => {
  const axes = ['A', 'B', 'C', 'D'];
  const you = [0.8, 0.6, 0.7, 0.5];
  const size = 300;

  it('sets cx and cy to size/2', () => {
    const { cx, cy } = buildRadarGeometry(axes, you, null, size);
    expect(cx).toBe(size / 2);
    expect(cy).toBe(size / 2);
  });

  it('gridRings has exactly 4 entries with correct k values', () => {
    const { gridRings } = buildRadarGeometry(axes, you, null, size);
    expect(gridRings).toHaveLength(4);
    expect(gridRings.map(r => r.k)).toEqual([0.25, 0.5, 0.75, 1]);
  });

  it('axisLines length equals axes.length', () => {
    const { axisLines } = buildRadarGeometry(axes, you, null, size);
    expect(axisLines).toHaveLength(axes.length);
  });

  it('dots length equals you.length', () => {
    const { dots } = buildRadarGeometry(axes, you, null, size);
    expect(dots).toHaveLength(you.length);
  });

  it('labels text is uppercase of input axes', () => {
    const { labels } = buildRadarGeometry(axes, you, null, size);
    labels.forEach((label, i) => {
      expect(label.text).toBe(axes[i].toUpperCase());
    });
  });

  it('targetPath is null when target is not passed', () => {
    const { targetPath } = buildRadarGeometry(axes, you, null, size);
    expect(targetPath).toBeNull();
  });

  it('targetPath is a string when target is provided', () => {
    const target = [0.9, 0.7, 0.8, 0.6];
    const { targetPath } = buildRadarGeometry(axes, you, target, size);
    expect(typeof targetPath).toBe('string');
  });
});
