import { describe, it, expect, vi, afterEach } from 'vitest';
import {
  cubicEaseOut,
  springStep,
  calcRingGeometry,
  clampNorm,
  calcStepDuration,
  generateTraceId,
} from '../../../frontend/src/utils/animationUtils.js';

afterEach(() => {
  vi.restoreAllMocks();
});

describe('cubicEaseOut', () => {
  it('returns 0 at t=0', () => {
    expect(cubicEaseOut(0)).toBe(0);
  });

  it('returns 1 at t=1', () => {
    expect(cubicEaseOut(1)).toBe(1);
  });

  it('returns 0.875 at t=0.5', () => {
    expect(cubicEaseOut(0.5)).toBeCloseTo(0.875);
  });

  it('is monotonically increasing', () => {
    expect(cubicEaseOut(0.3)).toBeLessThan(cubicEaseOut(0.7));
  });
});

describe('springStep', () => {
  it('returns target when current equals target', () => {
    expect(springStep(5, 5, 0.5)).toBe(5);
  });

  it('returns target when factor=1', () => {
    expect(springStep(0, 10, 1)).toBe(10);
  });

  it('returns current when factor=0', () => {
    expect(springStep(3, 10, 0)).toBe(3);
  });

  it('returns midpoint for factor=0.5', () => {
    expect(springStep(0, 10, 0.5)).toBe(5);
  });
});

describe('clampNorm', () => {
  it('returns 0.5 for value=50, max=100', () => {
    expect(clampNorm(50, 100)).toBe(0.5);
  });

  it('returns 0 for value=0', () => {
    expect(clampNorm(0, 100)).toBe(0);
  });

  it('returns 1 for value=max', () => {
    expect(clampNorm(100, 100)).toBe(1);
  });

  it('clamps to 0 for negative value', () => {
    expect(clampNorm(-10, 100)).toBe(0);
  });

  it('clamps to 1 when value exceeds max', () => {
    expect(clampNorm(150, 100)).toBe(1);
  });
});

describe('calcRingGeometry', () => {
  it('returns object with pct, r, c', () => {
    const result = calcRingGeometry(50, 100, 100);
    expect(result).toHaveProperty('pct');
    expect(result).toHaveProperty('r');
    expect(result).toHaveProperty('c');
  });

  it('computes r as size/2 - 6', () => {
    const { r } = calcRingGeometry(50, 100, 100);
    expect(r).toBe(44);
  });

  it('computes c as 2πr', () => {
    const { r, c } = calcRingGeometry(50, 100, 100);
    expect(c).toBeCloseTo(2 * Math.PI * r);
  });

  it('clamps pct to 1 when value exceeds max', () => {
    const { pct } = calcRingGeometry(200, 100, 100);
    expect(pct).toBe(1);
  });

  it('clamps pct to 0 when value is negative', () => {
    const { pct } = calcRingGeometry(-10, 100, 100);
    expect(pct).toBe(0);
  });

  it('returns pct=0.5 for value=50, max=100', () => {
    const { pct } = calcRingGeometry(50, 100, 100);
    expect(pct).toBe(0.5);
  });
});

describe('calcStepDuration', () => {
  it('returns 350 when Math.random returns 0', () => {
    vi.spyOn(Math, 'random').mockReturnValue(0);
    expect(calcStepDuration()).toBe(350);
  });

  it('returns 650 when Math.random returns 1', () => {
    vi.spyOn(Math, 'random').mockReturnValue(1);
    expect(calcStepDuration()).toBe(650);
  });

  it('returns a number within [350, 650]', () => {
    const result = calcStepDuration();
    expect(result).toBeGreaterThanOrEqual(350);
    expect(result).toBeLessThanOrEqual(650);
  });
});

describe('generateTraceId', () => {
  it('returns 0 when Math.random returns 0', () => {
    vi.spyOn(Math, 'random').mockReturnValue(0);
    expect(generateTraceId()).toBe(0);
  });

  it('returns an integer', () => {
    expect(Number.isInteger(generateTraceId())).toBe(true);
  });

  it('returns a value within [0, 0xfffff]', () => {
    const result = generateTraceId();
    expect(result).toBeGreaterThanOrEqual(0);
    expect(result).toBeLessThanOrEqual(0xfffff);
  });
});
