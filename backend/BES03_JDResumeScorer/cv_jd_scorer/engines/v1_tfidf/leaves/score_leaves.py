from typing import Literal


# -------------------- clamp_100 ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: jd_fit.score, ats.score
def clamp_100(v: float) -> int:
    return int(max(0, min(100, round(v))))
# -------------------- clamp_100 ------------- END ----------------


# -------------------- clamp_unit ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: jd_fit.score
def clamp_unit(v: float) -> float:
    return max(0.0, min(1.0, v))
# -------------------- clamp_unit ------------- END ----------------


# -------------------- tone_for ----------- START ----------
# -- Calls : nothing (leaf)
# -- Called by: jd_fit.score, ats.score
def tone_for(score: int) -> Literal["good", "warn", "bad"]:
    if score >= 75:
        return "good"
    if score >= 50:
        return "warn"
    return "bad"
# -------------------- tone_for ------------- END ----------------
