import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Card } from '../../../frontend/src/components/ui/Card.jsx';

describe('Card', () => {
  it('renders children content', () => {
    render(<Card>Card body</Card>);
    expect(screen.getByText('Card body')).toBeInTheDocument();
  });

  it('renders title when provided', () => {
    render(<Card title="Overview">body</Card>);
    expect(screen.getByText('Overview')).toBeInTheDocument();
  });

  it('renders eyebrow when provided', () => {
    render(<Card eyebrow="Module">body</Card>);
    expect(screen.getByText('Module')).toBeInTheDocument();
  });

  it('renders badge when provided', () => {
    render(<Card badge={<span>New</span>}>body</Card>);
    expect(screen.getByText('New')).toBeInTheDocument();
  });

  it('renders action when provided', () => {
    render(<Card action={<button>Edit</button>}>body</Card>);
    expect(screen.getByText('Edit')).toBeInTheDocument();
  });

  it('does not render a header when no header props are passed', () => {
    const { container } = render(<Card>body only</Card>);
    // The header div has borderBottom style — no header props means no header div
    const divs = container.querySelectorAll('div');
    // Only the outer card div and the content div should exist (2 divs)
    expect(divs).toHaveLength(2);
  });

  it('renders a header div when title is provided (3 divs total)', () => {
    const { container } = render(<Card title="Title">body</Card>);
    const divs = container.querySelectorAll('div');
    expect(divs.length).toBeGreaterThan(2);
  });

  it('applies custom className to the outer element', () => {
    const { container } = render(<Card className="custom-card">body</Card>);
    expect(container.firstChild).toHaveClass('card');
    expect(container.firstChild).toHaveClass('custom-card');
  });

  it('pad=true: content div style attribute contains var(--pad)', () => {
    const { container } = render(<Card pad>body</Card>);
    // Use lastElementChild to get the content div (not the optional header div)
    const contentDiv = container.querySelector('.card').lastElementChild;
    // jsdom may not expose CSS custom properties via style accessor; check raw attribute
    const styleAttr = contentDiv.getAttribute('style') || '';
    expect(styleAttr).toContain('var(--pad)');
  });

  it('pad=false: content div has zero padding', () => {
    const { container } = render(<Card pad={false}>body</Card>);
    const contentDiv = container.querySelector('.card').lastElementChild;
    // jsdom may return '0px' or '0' — parseFloat handles both
    expect(parseFloat(contentDiv.style.padding || '0')).toBe(0);
  });
});
