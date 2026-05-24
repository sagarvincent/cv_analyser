import { describe, it, expect } from 'vitest';
import { toneToColor } from '../../../frontend/src/utils/colorUtils.js';

describe('toneToColor', () => {
  it('maps "good" to var(--good)', () => {
    expect(toneToColor('good')).toBe('var(--good)');
  });

  it('maps "warn" to var(--warn)', () => {
    expect(toneToColor('warn')).toBe('var(--warn)');
  });

  it('maps "bad" to var(--bad)', () => {
    expect(toneToColor('bad')).toBe('var(--bad)');
  });

  it('maps "muted" to var(--muted)', () => {
    expect(toneToColor('muted')).toBe('var(--muted)');
  });

  it('unknown tone returns var(--accent)', () => {
    expect(toneToColor('accent')).toBe('var(--accent)');
  });

  it('empty string returns var(--accent)', () => {
    expect(toneToColor('')).toBe('var(--accent)');
  });

  it('undefined returns var(--accent)', () => {
    expect(toneToColor(undefined)).toBe('var(--accent)');
  });
});
