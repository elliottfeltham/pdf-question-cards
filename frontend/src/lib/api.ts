import type { Question } from "../types";

export async function exportNotebook(title: string, items: Question[]) {
  const res = await fetch('/api/export/notebook', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ title, items }),
  });
  if (!res.ok) throw new Error(await res.text());
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${(title || 'Lecture_Notebook').replace(/\s+/g,'_')}.ipynb`;
  a.click();
  URL.revokeObjectURL(url);
}
