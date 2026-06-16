import importlib
import os

from cv_jd_scorer.engine_base import ScorerEngine

_REGISTRY: dict[str, str] = {
    "v1_tfidf": "cv_jd_scorer.engines.v1_tfidf.engine",
    "v2_ml":    "cv_jd_scorer.engines.v2_ml.engine",
}
_DEFAULT = "v1_tfidf"


def _load_engine(engine_id: str) -> ScorerEngine:
    path = _REGISTRY.get(engine_id)
    if not path:
        raise RuntimeError(
            f"SCORER_ENGINE='{engine_id}' is not a valid engine. "
            f"Known engines: {', '.join(_REGISTRY)}"
        )
    # importlib ensures only the chosen engine's module is imported — v2's
    # torch/transformers dependencies never load when running v1_tfidf.
    return importlib.import_module(path).engine


# Resolved once at process startup. A bad SCORER_ENGINE value raises here,
# failing the container health check immediately rather than on the first request.
active_engine: ScorerEngine = _load_engine(
    os.environ.get("SCORER_ENGINE", _DEFAULT)
)
