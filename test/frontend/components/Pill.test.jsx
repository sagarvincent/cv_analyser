import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Pill } from '../../../frontend/src/components/ui/Pill.jsx';

describe('Pill', () => {
  it('renders children text', () => {
    render(<Pill>Senior Engineer</Pill>);
    expect(screen.getByText('Senior Engineer')).toBeInTheDocument();
  });

  it('always applies base "pill" class', () => {
    render(<Pill>text</Pill>);
    expect(screen.getByText('text')).toHaveClass('pill');
  });

  it('default tone does not add a "pill-default" modifier class', () => {
    render(<Pill>text</Pill>);
    expect(screen.getByText('text')).not.toHaveClass('pill-default');
  });

  it('tone="accent" adds "pill-accent" class', () => {
    render(<Pill tone="accent">text</Pill>);
    expect(screen.getByText('text')).toHaveClass('pill-accent');
  });

  it('tone="good" adds "pill-good" class', () => {
    render(<Pill tone="good">text</Pill>);
    expect(screen.getByText('text')).toHaveClass('pill-good');
  });

  it('dot=false (default) does not add "pill-dot" class', () => {
    render(<Pill>text</Pill>);
    expect(screen.getByText('text')).not.toHaveClass('pill-dot');
  });

  it('dot=true adds "pill-dot" class', () => {
    render(<Pill dot>text</Pill>);
    expect(screen.getByText('text')).toHaveClass('pill-dot');
  });

  it('dot=true and tone="accent" applies both modifier classes', () => {
    render(<Pill tone="accent" dot>text</Pill>);
    const el = screen.getByText('text');
    expect(el).toHaveClass('pill-accent');
    expect(el).toHaveClass('pill-dot');
  });
});
