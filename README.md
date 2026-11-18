<div align="center">

# context-overlap-lab

**Overlap pregunta ↔ contexto ↔ respuesta** · Angel Salazar

`jaccard(q,ctx) · jaccard(a,ctx) · jaccard(q,a)`

</div>

---

### `$ whoami`

Antes de discutir “calidad semántica”, miro overlap léxico. Si `answer_context` es bajo, la respuesta no está anclada.

---

### `$ ./lab.sh`

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
pytest
python -m context_overlap
```

---

Hecho en Lima · Angel Salazar · CIP 404730
