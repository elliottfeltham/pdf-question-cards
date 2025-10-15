import nbformat as nbf
from typing import List, Dict

def _strip_fences(s: str | None) -> str:
    if not s: return ""
    t = s.strip()
    if t.startswith("```json"): t = t[7:].strip()
    elif t.startswith("```python"): t = t[9:].strip()
    elif t.startswith("```"): t = t[3:].strip()
    if t.endswith("```"): t = t[:-3].strip()
    return t

def items_to_notebook(title: str, items: List[Dict]):
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name":"Python 3","language":"python","name":"python3"}

    # Title cell
    nb.cells.append(nbf.v4.new_markdown_cell(f"# {title}\n\nGenerated practice notebook."))

    for i, item in enumerate(items, start=1):
        prompt = item.get("prompt_md", "(missing)")
        nb.cells.append(nbf.v4.new_markdown_cell(f"## {i}. {prompt}"))

        if item.get("type") == "coding":
            starter = _strip_fences(item.get("starter_code")) or "# Your solution here\n"
            nb.cells.append(nbf.v4.new_code_cell(starter))
            # Optional reference solution as hidden details (markdown)
            sol_code = _strip_fences(item.get("solution_code"))
            sol_md = item.get("solution_md")
            if sol_code or sol_md:
                body = []
                if sol_md: body.append(sol_md)
                if sol_code: body.append("```python\n" + sol_code + "\n```")
                md = "\n\n".join(body)
                nb.cells.append(nbf.v4.new_markdown_cell(f"<details><summary><strong>Show reference</strong></summary>\n\n{md}\n\n</details>"))
        else:
            # Theory question: give a code cell for the user to type an answer
            nb.cells.append(nbf.v4.new_code_cell("# Write your answer here\n"))
            sol_md = item.get("solution_md")
            if sol_md:
                nb.cells.append(nbf.v4.new_markdown_cell(f"<details><summary><strong>Show reference</strong></summary>\n\n{sol_md}\n\n</details>"))

    return nb