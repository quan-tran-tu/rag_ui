A simple RAG application using Ollama, Milvus and Dash

1. Installation
- Install [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
- Install dependencies
```bash
git clone https://github.com/quan-tran-tu/rag_ui.git
cd rag_ui

poetry install
```
- Fix the ngrok link in .env and run the project (support for other apis coming soon)
```bash
poetry run python src/rag_ui/ui/app.py
```

