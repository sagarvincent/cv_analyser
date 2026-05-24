import { describe, it, expect } from 'vitest';
import { scorePassword } from '../../../frontend/src/utils/passwordUtils.js';

describe('scorePassword', () => {
  it('returns 0 for empty string', () => {
    expect(scorePassword('')).toBe(0);
  });

  it('returns 0 for null/undefined (falsy)', () => {
    expect(scorePassword(null)).toBe(0);
    expect(scorePassword(undefined)).toBe(0);
  });

  it('returns 0 for a short lowercase-only string (no criteria met)', () => {
    expect(scorePassword('abcde')).toBe(0);
  });

  it('returns 1 for a 10-char lowercase string (length ≥10 only)', () => {
    expect(scorePassword('abcdefghij')).toBe(1);
  });

  it('returns 2 for a 14-char lowercase string (two length criteria)', () => {
    expect(scorePassword('abcdefghijklmn')).toBe(2);
  });

  it('returns 5 for a strong password meeting all criteria', () => {
    // 14 chars, upper+lower, digit, special → all 5 criteria
    expect(scorePassword('AbcdefghijK1!x')).toBe(5);
  });

  it('mixed case adds 1 point', () => {
    const withMixed = scorePassword('Abcdefghij');
    const withoutMixed = scorePassword('abcdefghij');
    expect(withMixed - withoutMixed).toBe(1);
  });

  it('digit adds 1 point', () => {
    const withDigit = scorePassword('abcdefghi1');
    const withoutDigit = scorePassword('abcdefghij');
    expect(withDigit - withoutDigit).toBe(1);
  });

  it('special character adds 1 point', () => {
    const withSpecial = scorePassword('abcdefghi!');
    const withoutSpecial = scorePassword('abcdefghij');
    expect(withSpecial - withoutSpecial).toBe(1);
  });
});
