import clip
import torch
from PIL import Image
import faiss
import os
import numpy as np
from tqdm import tqdm

import sqlite3

os.environ['KMP_DUPLICATE_LIB_OK']='True'

def getEmbeddings(path):
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-L/14", device=device)

    Image.MAX_IMAGE_PIXELS = None

    image_folder = path
    valid_exts = (".jpg", ".jpeg", ".png")

    image_files = sorted([
        f for f in os.listdir(image_folder)
        if f.lower().endswith(valid_exts)
    ])
    
    BATCH_SIZE = 16
    embeddings = []
    valid_files = []

    batch_images = []
    batch_names = []

    with torch.no_grad():
        for filename in tqdm(image_files):
            try:
                image_path = os.path.join(image_folder, filename)
                image = Image.open(image_path).convert("RGB")

                image_input = preprocess(image)
                batch_images.append(image_input)
                batch_names.append(filename)

                if len(batch_images) == BATCH_SIZE:
                    image_tensor = torch.stack(batch_images).to(device)
                    batch_embeddings = model.encode_image(image_tensor).cpu().numpy()  # Move to CPU and convert to numpy
                    embeddings.extend(batch_embeddings)
                    valid_files.extend(batch_names)
                    batch_images, batch_names = [], []
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
        
        if batch_images:
            image_tensor = torch.stack(batch_images).to(device)
            batch_embeddings = model.encode_image(image_tensor).cpu().numpy()  # Move to CPU and convert to numpy
            embeddings.extend(batch_embeddings)
            valid_files.extend(batch_names)

    # Convert to numpy array
    embeddings = np.array(embeddings)

    file_path = "all_embeddings.pt"
    if os.path.exists(file_path):
        all_data = torch.load(file_path, weights_only=False)
    else:
        all_data = {}

    # Use folder path as key
    all_data[path] = {
        "embeddings": embeddings,
        "files": valid_files
    }

    torch.save(all_data, file_path)
    print(f"Embeddings Saved Successfully for {len(valid_files)} images")


def Search(path, prompt):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-L/14", device=device)

    file_path = "all_embeddings.pt"
    if not os.path.exists(file_path):
        return []
    
    all_data = torch.load(file_path, weights_only=False)

    if path not in all_data:
        return []
    
    folder_data = all_data[path]
    embeddings = folder_data["embeddings"].astype('float32')
    files = folder_data["files"]

    d = embeddings.shape[1]  
    index = faiss.IndexFlatIP(d)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    text = clip.tokenize([prompt]).to(device)
    
    with torch.no_grad():
        text_features = model.encode_text(text)

    # Move text features to CPU and convert to numpy
    text_vector = text_features.cpu().numpy().astype('float32')
    faiss.normalize_L2(text_vector)

    k = 10
    distances, indices = index.search(text_vector, k)

    top_results = []
    for idx in indices[0]:
        if idx < len(files):  # Safety check
            top_results.append(files[idx])

    return top_results


def Search_All(prompt):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-L/14", device=device)

    file_path = "all_embeddings.pt"
    if not os.path.exists(file_path):
        return []
    
    all_data = torch.load(file_path, weights_only=False)

    all_embeddings=[]
    all_files=[]

    
    

    for path in tqdm(list(all_data.keys()), desc="Loading embeddings"):
        all_files.extend(all_data[path]["files"])
        all_embeddings.extend(all_data[path]["embeddings"])

    all_embeddings = np.array(all_embeddings)
    embeddings= all_embeddings.astype('float32')

    d = embeddings.shape[1]  
    index = faiss.IndexFlatIP(d)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    
    with torch.no_grad():
        text= clip.tokenize(prompt)
        text_features = model.encode_text(text)

    # Move text features to CPU and convert to numpy
    text_vector = text_features.cpu().numpy().astype('float32')
    faiss.normalize_L2(text_vector)

    k = 10
    distances, indices = index.search(text_vector, k)

    top_results = []
    for idx in indices[0]:
        if idx < len(all_files):  # Safety check
            top_results.append(all_files[idx])

    return top_results

      



def updateFolder(path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-L/14", device=device)

    BATCH_SIZE= 16

    file_path = "all_embeddings.pt"
    if not os.path.exists(file_path):
        return
    
    all_data = torch.load(file_path, weights_only=False)
    

    

    if(path not in list(all_data.keys())):
        return 
    

    cur_folder= all_data[path]
    cur_files= cur_folder["files"]

    image_folder = path
    valid_exts = (".jpg", ".jpeg", ".png")

    image_files = sorted([
        f for f in os.listdir(image_folder)
        if(f.lower().endswith(valid_exts) and f not in cur_files)
    ])

    embeddings=[]
    valid_files=[]

    batch_images = []
    batch_names = []


    with torch.no_grad():
        for filename in image_files:
            try:
                image_path = os.path.join(image_folder, filename)
                image = Image.open(image_path).convert("RGB")

                image_input = preprocess(image)
                batch_images.append(image_input)
                batch_names.append(filename)

                if len(batch_images) == BATCH_SIZE:
                    image_tensor = torch.stack(batch_images).to(device)
                    batch_embeddings = model.encode_image(image_tensor).cpu().numpy()  # Move to CPU and convert to numpy
                    embeddings.extend(batch_embeddings)
                    valid_files.extend(batch_names)
                    batch_images, batch_names = [], []
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
        
        if batch_images:
            image_tensor = torch.stack(batch_images).to(device)
            batch_embeddings = model.encode_image(image_tensor).cpu().numpy()  # Move to CPU and convert to numpy
            embeddings.extend(batch_embeddings)
            valid_files.extend(batch_names)
    

    embeddings = np.array(embeddings)

    cur_folder["files"].extend(valid_files)
    if embeddings.size > 0:
        cur_folder["embeddings"] = np.concatenate(
            (cur_folder["embeddings"], embeddings), axis=0
        )
    
    torch.save(all_data, file_path)

    return("Success")


def getPaths():
    file_path = "all_embeddings.pt"
    if not os.path.exists(file_path):
        return []
    
    all_data = torch.load(file_path, weights_only=False)

    paths=[]
    for path in list(all_data.keys()):
        paths.append(path)

    return paths

    
