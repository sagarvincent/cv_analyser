import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Bar } from '../../../frontend/src/components/ui/Bar.jsx';

// 4 levels deep: testing-library wrapper > outer div > track div > fill div
const getFillDiv = (container) => container.querySelector('div > div > div > div');

describe('Bar', () => {
  it('renders without crashing', () => {
    const { container } = render(<Bar value={50} />);
    expect(container.firstChild).toBeInTheDocument();
  });

  it('value=0 renders fill div with width 0', () => {
    const { container } = render(<Bar value={0} />);
    // jsdom may normalize '0%' to '' — use parseFloat with fallback
    expect(parseFloat(getFillDiv(container).style.width || '0')).toBe(0);
  });

  it('value=100, max=100 renders fill div with width 100%', () => {
    const { container } = render(<Bar value={100} max={100} />);
    expect(getFillDiv(container).style.width).toBe('100%');
  });

  it('value=150, max=100 clamps to width 100%', () => {
    const { container } = render(<Bar value={150} max={100} />);
    expect(getFillDiv(container).style.width).toBe('100%');
  });

  it('negative value clamps to width 0', () => {
    const { container } = render(<Bar value={-10} />);
    expect(parseFloat(getFillDiv(container).style.width || '0')).toBe(0);
  });

  it('renders label text when label prop is provided', () => {
    render(<Bar value={50} label="Skills" />);
    expect(screen.getByText('Skills')).toBeInTheDocument();
  });

  it('renders right text when right prop is provided', () => {
    render(<Bar value={50} right="75%" />);
    expect(screen.getByText('75%')).toBeInTheDocument();
  });

  it('does not render label row when neither label nor right is provided', () => {
    const { container } = render(<Bar value={50} />);
    // Outer div → track div → fill div: 3 divs total; no label row
    const divs = container.querySelectorAll('div');
    expect(divs).toHaveLength(3);
  });

  it('renders label row when label is provided', () => {
    const { container } = render(<Bar value={50} label="Score" />);
    const divs = container.querySelectorAll('div');
    expect(divs.length).toBeGreaterThan(3);
  });
});
