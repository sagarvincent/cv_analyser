import { describe, it, expect } from 'vitest';
import { scaleCompValue, formatComp } from '../../../frontend/src/utils/compBandUtils.js';

describe('scaleCompValue', () => {
  it('returns padL when v equals min', () => {
    expect(scaleCompValue(50000, 50000, 150000, 20, 260)).toBe(20);
  });

  it('returns padL + innerW when v equals max', () => {
    expect(scaleCompValue(150000, 50000, 150000, 20, 260)).toBe(280);
  });

  it('returns midpoint when v is halfway between min and max', () => {
    expect(scaleCompValue(100000, 50000, 150000, 20, 260)).toBe(150);
  });
});

describe('formatComp', () => {
  it('formats dollars to k notation with $ symbol', () => {
    expect(formatComp(75000, '$')).toBe('$75k');
  });

  it('formats with euro symbol', () => {
    expect(formatComp(100000, '€')).toBe('€100k');
  });

  it('rounds to nearest k', () => {
    expect(formatComp(1500, '$')).toBe('$2k');
  });

  it('rounds down when below midpoint', () => {
    expect(formatComp(1400, '$')).toBe('$1k');
  });
});
