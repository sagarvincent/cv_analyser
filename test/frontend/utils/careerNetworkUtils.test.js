import { describe, it, expect } from 'vitest';
import {
  colorForFit,
  findPlacedNode,
  placeOnRing,
  buildCareerNetworkLayout,
  calcNodeRadius,
  formatFitPct,
  resolveLinkEndpoints,
  calcLinkStrokeWidth,
} from '../../../frontend/src/utils/careerNetworkUtils.js';

describe('colorForFit', () => {
  it('returns var(--accent) when fit > 0.85', () => {
    expect(colorForFit(0.9)).toBe('var(--accent)');
  });

  it('returns var(--good) when fit > 0.7 but ≤ 0.85', () => {
    expect(colorForFit(0.75)).toBe('var(--good)');
  });

  it('returns var(--warn) when fit > 0.55 but ≤ 0.7', () => {
    expect(colorForFit(0.6)).toBe('var(--warn)');
  });

  it('returns var(--muted) when fit ≤ 0.55', () => {
    expect(colorForFit(0.3)).toBe('var(--muted)');
  });

  it('boundary 0.85 falls to var(--good)', () => {
    expect(colorForFit(0.85)).toBe('var(--good)');
  });

  it('boundary 0.7 falls to var(--warn)', () => {
    expect(colorForFit(0.7)).toBe('var(--warn)');
  });

  it('boundary 0.55 falls to var(--muted)', () => {
    expect(colorForFit(0.55)).toBe('var(--muted)');
  });
});

describe('findPlacedNode', () => {
  const placed = [
    { id: 'a', x: 10, y: 20 },
    { id: 'b', x: 30, y: 40 },
  ];

  it('returns the node with matching id', () => {
    const result = findPlacedNode(placed, 'a', 100, 100);
    expect(result).toEqual({ id: 'a', x: 10, y: 20 });
  });

  it('returns { x: cx, y: cy } when id is not found', () => {
    expect(findPlacedNode(placed, 'z', 100, 100)).toEqual({ x: 100, y: 100 });
  });

  it('returns { x: cx, y: cy } for empty placed array', () => {
    expect(findPlacedNode([], 'a', 50, 60)).toEqual({ x: 50, y: 60 });
  });
});

describe('placeOnRing', () => {
  const nodes = [{ id: 'n1', label: 'A' }, { id: 'n2', label: 'B' }];

  it('returns same number of nodes as input', () => {
    expect(placeOnRing(nodes, 100, 200, 200)).toHaveLength(nodes.length);
  });

  it('each node has x and y added', () => {
    const result = placeOnRing(nodes, 100, 200, 200);
    result.forEach(n => {
      expect(n).toHaveProperty('x');
      expect(n).toHaveProperty('y');
    });
  });

  it('preserves original fields on each node', () => {
    const result = placeOnRing(nodes, 100, 200, 200);
    expect(result[0].id).toBe('n1');
    expect(result[0].label).toBe('A');
  });
});

describe('buildCareerNetworkLayout', () => {
  const nodes = [
    { id: 'a', ring: 1 },
    { id: 'b', ring: 2 },
    { id: 'c', ring: 2 },
  ];

  it('returns object with placed, cx, cy, ring1R, ring2R', () => {
    const result = buildCareerNetworkLayout(nodes, 600, 500);
    expect(result).toHaveProperty('placed');
    expect(result).toHaveProperty('cx');
    expect(result).toHaveProperty('cy');
    expect(result).toHaveProperty('ring1R');
    expect(result).toHaveProperty('ring2R');
  });

  it('cx equals W/2 and cy equals H/2', () => {
    const { cx, cy } = buildCareerNetworkLayout(nodes, 600, 500);
    expect(cx).toBe(300);
    expect(cy).toBe(250);
  });

  it('ring1R is 130 and ring2R is 215', () => {
    const { ring1R, ring2R } = buildCareerNetworkLayout(nodes, 600, 500);
    expect(ring1R).toBe(130);
    expect(ring2R).toBe(215);
  });

  it('placed contains all input nodes', () => {
    const { placed } = buildCareerNetworkLayout(nodes, 600, 500);
    expect(placed).toHaveLength(nodes.length);
  });
});

describe('calcNodeRadius', () => {
  it('returns 8 + fit*12 for chartStyle="dots"', () => {
    expect(calcNodeRadius(0.5, 'dots')).toBe(14);
  });

  it('returns 20 for fit=1 in dots style', () => {
    expect(calcNodeRadius(1, 'dots')).toBe(20);
  });

  it('returns 8 for fit=0 in dots style', () => {
    expect(calcNodeRadius(0, 'dots')).toBe(8);
  });

  it('returns 22 for any other chartStyle', () => {
    expect(calcNodeRadius(0.8, 'blocks')).toBe(22);
    expect(calcNodeRadius(0.5, 'circles')).toBe(22);
  });
});

describe('formatFitPct', () => {
  it('converts 0.75 to 75', () => {
    expect(formatFitPct(0.75)).toBe(75);
  });

  it('converts 1 to 100', () => {
    expect(formatFitPct(1)).toBe(100);
  });

  it('converts 0 to 0', () => {
    expect(formatFitPct(0)).toBe(0);
  });
});

describe('resolveLinkEndpoints', () => {
  const placed = [
    { id: 'n1', x: 50, y: 80 },
    { id: 'n2', x: 120, y: 200 },
  ];

  it('uses cx/cy as "a" when link.from is "center"', () => {
    const { a } = resolveLinkEndpoints({ from: 'center', to: 'n1' }, placed, 100, 150);
    expect(a).toEqual({ x: 100, y: 150 });
  });

  it('resolves "a" from placed when link.from is a node id', () => {
    const { a } = resolveLinkEndpoints({ from: 'n1', to: 'n2' }, placed, 100, 150);
    expect(a).toEqual({ id: 'n1', x: 50, y: 80 });
  });

  it('resolves "b" from placed via findPlacedNode', () => {
    const { b } = resolveLinkEndpoints({ from: 'center', to: 'n2' }, placed, 100, 150);
    expect(b).toEqual({ id: 'n2', x: 120, y: 200 });
  });

  it('returns object with a and b each having x and y', () => {
    const { a, b } = resolveLinkEndpoints({ from: 'center', to: 'n1' }, placed, 100, 150);
    expect(a).toHaveProperty('x');
    expect(a).toHaveProperty('y');
    expect(b).toHaveProperty('x');
    expect(b).toHaveProperty('y');
  });
});

describe('calcLinkStrokeWidth', () => {
  it('returns 2 for fit=1', () => {
    expect(calcLinkStrokeWidth(1)).toBe(2);
  });

  it('returns 0.5 for fit=0', () => {
    expect(calcLinkStrokeWidth(0)).toBe(0.5);
  });

  it('returns 1.25 for fit=0.5', () => {
    expect(calcLinkStrokeWidth(0.5)).toBe(1.25);
  });

  it('defaults fit to 0.5 when null, returning 1.25', () => {
    expect(calcLinkStrokeWidth(null)).toBe(1.25);
  });
});
