# 🔍 CLIP Image Search CLI

A lightweight command-line tool that uses **OpenAI’s CLIP** to embed local images and perform **natural language search**.  
Images are indexed with **FAISS** for fast similarity search, making it easy to find what you need by simply typing a description.

---

## ✨ Features
- 📂 Generate and store embeddings for images in any folder.  
- 🔎 Search images using **natural language queries**.  
- ⚡ Powered by [FAISS](https://github.com/facebookresearch/faiss) for fast similarity search.  
- 💻 Simple and intuitive **CLI interface**.  

---

## 📦 Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/Jeevaanandh/clip-image-search-cli.git
```

---
## 🛠 Usage
1. Create embeddings for images in a folder:
(Make sure this is done before searching for an image)
```bash
gva embed /path/to/images
```
2. Search for a specific image in a path:
```bash
gva search /path/to/images "sunset over mountains"
```
3. Serach for images in all added paths:
```bash
gva search-all "sunset over mountains"
```
4. Add embeddings of newly added images to an already embedded folder:
```bash
gva update /path/to/images
```
5. To get all the embedded paths:
```bash
gva get-paths
```

---

## 📝 Example
```bash
# Index images
gva embed ~/Pictures/Wallpapers

# Search them by description
gva search-all "a futuristic city skyline at night"
```

---

## ⚡ Requirements
- Python 3.8+
- PyTorch
- FAISS
- OpenAI CLIP

---

## 📌 Notes
- The first run may take longer since the CLIP model needs to be downloaded.
- Embeddings are stored locally so future searches are instant.
