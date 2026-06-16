# Bump on every behavioural parser change; stamped onto bulk-parsed JSONL
# rows so eval data can distinguish parser versions.
# 1.0.0 — original parser (blank-line experience splitting, single alias list)
# 1.1.0 — ftfy/NFKC cleaning, strict/fuzzy header split, date-anchored
#         entry splitting, headline routing, education year fallback,
#         skills noise filters
PARSER_VERSION = "1.1.0"
