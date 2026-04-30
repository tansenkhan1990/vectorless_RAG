def build_prompt(query, docs):
    context = "\n\n".join([
        f"{d['file_name']} page {d['page_number']}:\n{d['chunk_text']}"
        for d in docs
    ])

    return f"""
Use ONLY the context below.

If answer is not found, say:
I don't know.

Context:
{context}

Question:
{query}

Answer:
"""