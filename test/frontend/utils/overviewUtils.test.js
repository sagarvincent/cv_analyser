import { describe, it, expect } from 'vitest';
import { overviewCellBorders } from '../../../frontend/src/utils/overviewUtils.js';

describe('overviewCellBorders', () => {
  it('grid i=0: borderRight is set and borderBottom is set (first row, not last col)', () => {
    const result = overviewCellBorders(0, 6, 'grid');
    expect(result.borderRight).toBe('1px solid var(--border)');
    expect(result.borderBottom).toBe('1px solid var(--border)');
  });

  it('grid i=1 (middle of first row): both borders set', () => {
    const result = overviewCellBorders(1, 6, 'grid');
    expect(result.borderRight).toBe('1px solid var(--border)');
    expect(result.borderBottom).toBe('1px solid var(--border)');
  });

  it('grid i=2 (last col in first row, i%3===2): borderRight is none', () => {
    const result = overviewCellBorders(2, 6, 'grid');
    expect(result.borderRight).toBe('none');
    expect(result.borderBottom).toBe('1px solid var(--border)');
  });

  it('grid i=3 (first of second row, i>=3): borderBottom is none', () => {
    const result = overviewCellBorders(3, 6, 'grid');
    expect(result.borderRight).toBe('1px solid var(--border)');
    expect(result.borderBottom).toBe('none');
  });

  it('grid i=5 (last col, second row): both borders none', () => {
    const result = overviewCellBorders(5, 6, 'grid');
    expect(result.borderRight).toBe('none');
    expect(result.borderBottom).toBe('none');
  });

  it('list i=0 (not last): borderRight is none, borderBottom is set', () => {
    const result = overviewCellBorders(0, 3, 'list');
    expect(result.borderRight).toBe('none');
    expect(result.borderBottom).toBe('1px solid var(--border)');
  });

  it('list i=2 (last item): both borders none', () => {
    const result = overviewCellBorders(2, 3, 'list');
    expect(result.borderRight).toBe('none');
    expect(result.borderBottom).toBe('none');
  });

  it('returns object with exactly borderRight and borderBottom keys', () => {
    const result = overviewCellBorders(0, 6, 'grid');
    expect(Object.keys(result).sort()).toEqual(['borderBottom', 'borderRight']);
  });
});
