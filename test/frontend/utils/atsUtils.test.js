import { describe, it, expect } from 'vitest';
import { countPassedChecks } from '../../../frontend/src/utils/atsUtils.js';

describe('countPassedChecks', () => {
  it('returns total count when all checks pass', () => {
    const checks = [{ pass: true }, { pass: true }, { pass: true }];
    expect(countPassedChecks(checks)).toBe(3);
  });

  it('returns 0 when no checks pass', () => {
    const checks = [{ pass: false }, { pass: false }];
    expect(countPassedChecks(checks)).toBe(0);
  });

  it('counts only passing checks in a mixed array', () => {
    const checks = [{ pass: true }, { pass: false }, { pass: true }, { pass: false }];
    expect(countPassedChecks(checks)).toBe(2);
  });

  it('returns 0 for an empty array', () => {
    expect(countPassedChecks([])).toBe(0);
  });
});
