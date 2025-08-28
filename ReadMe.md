## CLIP Image Search CLI

A lightweight command-line tool that uses OpenAI’s CLIP to embed local images and search them with natural language. Images are indexed with FAISS for fast similarity search, making it easy to find what you need by simply typing a description.
---

## 🚀 Features
- Generate and store embeddings for images in a folder.
- Search images using natural language queries.
- Uses [FAISS](https://github.com/facebookresearch/faiss) for fast similarity search.
- CLI interface for easy use.

---

## 📦 Installation

You can install the tool directly from GitHub:

```bash
pip install git+https://github.com/Jeevaanandh/clip-image-search-cli.git
```

---
## 🛠 Usage
1. Create embeddings for images in a folder:
```bash
gva embed /path/to/images
```
2. Search for a specific image in a path:
```bash
gva search /path/to/images "sunset over mountains"
```
3. Add embeddings of new images added to an already added folder:
```bash
gva update /path/to/images
```
4. To get all the paths where images where embedded:
```bash
gva get-paths
```

