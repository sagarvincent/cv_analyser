# Pure scoring/assembly leaves — operate on plain numbers so they are testable
# without loading the embedding model.

_MINUS = "−"  # U+2212 minus sign (matches the frontend heatmap convention)

_OVER_NOTE = "You exceed the JD's demand in this area — lead with it."
_SMALLEST_GAP_NOTE = "Your closest area to the JD's bar, though still under it."
_GAP_NOTE = "The JD asks for more than your CV currently signals here."
_EDGE_NOTE = "Even your weakest area clears the JD's ask."
_MATCH_NOTE = "Your coverage aligns closely with the JD's expectation."


# -------------------- aggregate_sim ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: scorer.score_rows, jd_categories.build_rows
def aggregate_sim(sims: list[float]) -> float:
    """Collapse a set of phrase→target cosine similarities into one [0,1] coverage
    score. Blends the peak signal with the average breadth, then clamps."""
    clamped = [max(0.0, min(1.0, s)) for s in sims]
    if not clamped:
        return 0.0
    peak = max(clamped)
    mean = sum(clamped) / len(clamped)
    return max(0.0, min(1.0, 0.7 * peak + 0.3 * mean))
# -------------------- aggregate_sim ------------- END ----------------


# -------------------- format_delta ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: build_delta_cards
def format_delta(delta_val: float) -> str:
    """Format a [-1,1] delta as a signed integer string, e.g. '+27' or '−42'."""
    pts = abs(int(round(delta_val * 100)))
    return f"+{pts}" if delta_val >= 0 else f"{_MINUS}{pts}"
# -------------------- format_delta ------------- END ----------------


# -------------------- build_delta_cards ----------- START ----------
# -- Calls : format_delta
# -- Called by: builder.build_skill_matrix
def build_delta_cards(names: list[str], you_vals: list[float], jd_ask_vals: list[float]) -> list[dict]:
    """Three cards off the YOU − JD-ASK deltas: the strongest position, the biggest
    gap, and the closest match. Labels, colours, and notes follow the actual sign —
    the top delta is only an 'OVER-INDEX' when it is genuinely positive."""
    if not names:
        return []

    deltas = [you_vals[i] - jd_ask_vals[i] for i in range(len(names))]
    order = sorted(range(len(names)), key=lambda i: deltas[i])
    under_i = order[0]
    over_i = order[-1]

    used = {over_i, under_i}
    remaining = [i for i in range(len(names)) if i not in used]
    pool = remaining if remaining else list(range(len(names)))
    closest_i = min(pool, key=lambda i: abs(deltas[i]))

    # Top delta: an over-index only if positive, otherwise it's the smallest gap.
    if deltas[over_i] > 0:
        top = _card("OVER-INDEX", names[over_i], deltas[over_i], "var(--good)", _OVER_NOTE)
    else:
        top = _card("SMALLEST GAP", names[over_i], deltas[over_i], "var(--text-2)", _SMALLEST_GAP_NOTE)

    # Bottom delta: a gap only if negative, otherwise everything clears the ask.
    if deltas[under_i] < 0:
        bottom = _card("BIGGEST GAP", names[under_i], deltas[under_i], "var(--warn)", _GAP_NOTE)
    else:
        bottom = _card("STRONGEST EDGE", names[under_i], deltas[under_i], "var(--good)", _EDGE_NOTE)

    closest = _card("CLOSEST MATCH", names[closest_i], deltas[closest_i], "var(--text-2)", _MATCH_NOTE)
    return [top, bottom, closest]
# -------------------- build_delta_cards ------------- END ----------------


# -------------------- _card ----------- START ----------
# -- Calls : format_delta
# -- Called by: build_delta_cards
def _card(label: str, topic: str, delta_val: float, color: str, note: str) -> dict:
    return {
        "label": label,
        "topic": topic,
        "delta": format_delta(delta_val),
        "color": color,
        "note": note,
    }
# -------------------- _card ------------- END ----------------
