WHOLE_PROMPT = """You generate concise study items from a full lecture.
Return ONLY JSON object: {{"items":[ ... ]}}.
Each item fields:
- type: "theory" or "coding"
- prompt_md: <= 25 words, one idea
- solution_md: <= 80 words explaining the answer
- solution_code should be provided for coding questions (Python if used)
- Don't include starter code
Create up to {max_items} high-value, non-duplicate items.

TEXT:
---
{lecture_text}
---
"""
