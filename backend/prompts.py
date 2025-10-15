WHOLE_PROMPT = """You generate concise study items from a full lecture.
Return ONLY JSON object: {{"items":[ ... ]}}.
Each item fields:
- type: "theory" or "coding"
- prompt_md: <= 25 words, one idea
- solution_md: <= 80 words explaining the answer
- starter_code / solution_code optional (Python if used)
Create up to {max_items} high-value, non-duplicate items.

TEXT:
---
{lecture_text}
---
"""
