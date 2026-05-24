import { describe, it, expect } from 'vitest';
import {
  colorForSkill,
  calcCellPosition,
  calcDotRadius,
} from '../../../frontend/src/utils/skillHeatmapUtils.js';

describe('colorForSkill', () => {
  it('returns var(--surface-3) for null', () => {
    expect(colorForSkill(null)).toBe('var(--surface-3)');
  });

  it('returns var(--surface-3) for undefined', () => {
    expect(colorForSkill(undefined)).toBe('var(--surface-3)');
  });

  it('v=0.1 (< 0.25) returns oklch string with 0.30 lightness', () => {
    const result = colorForSkill(0.1);
    expect(result).toContain('oklch(0.30');
  });

  it('v=0.4 (0.25–0.55) returns oklch string with 0.55 lightness', () => {
    const result = colorForSkill(0.4);
    expect(result).toContain('oklch(0.55');
  });

  it('v=0.65 (0.55–0.75) returns oklch string with 0.74 lightness', () => {
    const result = colorForSkill(0.65);
    expect(result).toContain('oklch(0.74');
  });

  it('v=0.9 (≥ 0.75) returns oklch string with 0.85 lightness', () => {
    const result = colorForSkill(0.9);
    expect(result).toContain('oklch(0.85');
  });
});

describe('calcCellPosition', () => {
  it('returns correct cx and cy for ri=0, ci=0', () => {
    const result = calcCellPosition(0, 0, 60, 30, 40, 35);
    expect(result).toEqual({ cx: 60, cy: 30 });
  });

  it('returns correct cx and cy for ri=1, ci=2', () => {
    const result = calcCellPosition(1, 2, 60, 30, 40, 35);
    expect(result).toEqual({ cx: 60 + 2 * 40, cy: 30 + 1 * 35 });
  });
});

describe('calcDotRadius', () => {
  it('returns 0 for null', () => {
    expect(calcDotRadius(null)).toBe(0);
  });

  it('returns 0 for undefined', () => {
    expect(calcDotRadius(undefined)).toBe(0);
  });

  it('returns 4 for v=0', () => {
    expect(calcDotRadius(0)).toBe(4);
  });

  it('returns 14 for v=1', () => {
    expect(calcDotRadius(1)).toBe(14);
  });

  it('returns 9 for v=0.5', () => {
    expect(calcDotRadius(0.5)).toBe(9);
  });
});
