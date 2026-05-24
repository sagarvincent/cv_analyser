import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { CountUp } from '../../../frontend/src/components/ui/CountUp.jsx';

describe('CountUp', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('renders suffix immediately', () => {
    render(<CountUp to={100} suffix="%" duration={900} />);
    expect(screen.getByText(/%/)).toBeInTheDocument();
  });

  it('renders initial value of 0 before animation runs', () => {
    render(<CountUp to={100} duration={900} />);
    expect(screen.getByText('0')).toBeInTheDocument();
  });

  it('renders 0% initially when suffix is provided', () => {
    render(<CountUp to={100} suffix="%" duration={900} />);
    expect(screen.getByText('0%')).toBeInTheDocument();
  });

  it('animates to target value after duration elapses', () => {
    render(<CountUp to={100} duration={500} />);

    act(() => {
      vi.advanceTimersByTime(600);
    });

    expect(screen.getByText('100')).toBeInTheDocument();
  });

  it('renders target value with suffix after animation completes', () => {
    render(<CountUp to={75} suffix="%" duration={500} />);

    act(() => {
      vi.advanceTimersByTime(600);
    });

    expect(screen.getByText('75%')).toBeInTheDocument();
  });

  it('uses toFixed format when decimals > 0', () => {
    render(<CountUp to={99.5} duration={500} decimals={1} />);

    act(() => {
      vi.advanceTimersByTime(600);
    });

    expect(screen.getByText('99.5')).toBeInTheDocument();
  });
});
