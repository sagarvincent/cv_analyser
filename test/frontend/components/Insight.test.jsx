import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Insight } from '../../../frontend/src/components/ui/Insight.jsx';

describe('Insight', () => {
  it('renders text content', () => {
    render(<Insight text="Skills matter more than titles." />);
    expect(screen.getByText(/"Skills matter more than titles\."/)).toBeInTheDocument();
  });

  it('wraps text in double quotes', () => {
    const { container } = render(<Insight text="Test insight" />);
    expect(container.textContent).toContain('"Test insight"');
  });

  it('applies italic font style', () => {
    const { container } = render(<Insight text="italic text" />);
    expect(container.firstChild.style.fontStyle).toBe('italic');
  });

  it('renders source when provided', () => {
    render(<Insight text="Some insight" source="LinkedIn Data" />);
    expect(screen.getByText('LinkedIn Data')).toBeInTheDocument();
  });

  it('does not render source element when source is omitted', () => {
    render(<Insight text="Some insight" />);
    expect(screen.queryByText('LinkedIn Data')).not.toBeInTheDocument();
  });

  it('source element is not rendered when source prop is undefined', () => {
    const { container } = render(<Insight text="insight only" />);
    // Only one child div (no source div)
    expect(container.firstChild.children).toHaveLength(0);
  });
});
