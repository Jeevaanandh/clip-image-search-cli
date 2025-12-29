import clip
import torch
from PIL import Image
import faiss
import os
import numpy as np
from tqdm import tqdm

import sqlite3

os.environ['KMP_DUPLICATE_LIB_OK']='True'

conn= sqlite3.connect("embeddings.db")
cursor= conn.cursor()

def getEmbeddings():

    path= os.getcwd()
    listOfTables=cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Embeddings'; ").fetchall()
    if(listOfTables):
        print("Embeddings for the Current Folder is already done. Use 'sync' to update ")
        return


    cursor.execute("CREATE TABLE IF NOT EXISTS Embeddings(" \
    "path TEXT PRIMARY KEY," \
    "name TEXT," \
    "embeddings BLOB);")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-L/14", device=device)

    Image.MAX_IMAGE_PIXELS = None

    image_folder = path
    valid_exts = (".jpg", ".jpeg", ".png", "webp")

    image_files = sorted([
        f for f in os.listdir(image_folder)
        if f.lower().endswith(valid_exts)
    ])
    
    BATCH_SIZE = 16
    embeddings = []
    valid_files = []
    valid_paths=[]

    batch_images = []
    batch_names = []
    batch_paths=[]

    

    with torch.no_grad():
        for filename in tqdm(image_files):
            try:
                image_path = os.path.join(image_folder, filename)
                image = Image.open(image_path).convert("RGB")

                image_input = preprocess(image)
                batch_images.append(image_input)
                batch_names.append(filename)
                batch_paths.append(image_path)

                if len(batch_images) == BATCH_SIZE:
                    image_tensor = torch.stack(batch_images).to(device)
                    batch_embeddings = model.encode_image(image_tensor).cpu().numpy()  # Move to CPU and convert to numpy
                    embeddings.extend(batch_embeddings)
                    valid_files.extend(batch_names)
                    valid_paths.extend(batch_paths)
                    batch_images, batch_names, batch_paths = [], [], []
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
        
        if batch_images:
            image_tensor = torch.stack(batch_images).to(device)
            batch_embeddings = model.encode_image(image_tensor).cpu().numpy()  # Move to CPU and convert to numpy
            embeddings.extend(batch_embeddings)
            valid_files.extend(batch_names)
            valid_paths.extend(batch_paths)

    # Convert to numpy array
    embeddings = np.array(embeddings)

    


    for i in range(0, len(valid_paths)):
        embedding_blob= embeddings[i].astype(np.float32).tobytes()
        cursor.execute("INSERT INTO Embeddings VALUES(?,?,?)", (valid_paths[i], valid_files[i], embedding_blob))
        
    conn.commit()

    print("Embeddings saved successfully")


def Search(prompt):

    listOfTables=cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Embeddings'; ").fetchall()
    
    if(listOfTables==[]):
        print("No embeddings found. Run embed first.")
        return
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-L/14", device=device)

    
    
    embeddings=[]
    cursor.execute("SELECT * FROM Embeddings;")
    rows= cursor.fetchall()

    valid_names=[]

    for path, name, emb in rows:
        embedding = np.frombuffer(emb, dtype=np.float32)
        embeddings.append(embedding)
        valid_names.append(name)


    embeddings = np.vstack(embeddings).astype(np.float32)

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
          # Safety check
        top_results.append(valid_names[idx])

    return top_results


      



def updateFolder():
    path= os.getcwd()
    
    
    cur_files=[]
    lst = conn.execute("SELECT name FROM Embeddings;").fetchall()

    for f in lst:
        cur_files.append(f[0])


    
    image_folder = path
    valid_exts = (".jpg", ".jpeg", ".png", "webp")

    
    image_files = []

    for f in os.listdir():
        if(f.lower().endswith(valid_exts) and f not in cur_files):
            image_files.append(f)


    
    count= len(image_files)
    if(count==0):
        return 0
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-L/14", device=device)

    BATCH_SIZE= 16

    
    

    embeddings=[]
    valid_files=[]
    valid_paths=[]

    batch_images = []
    batch_names = []
    batch_paths=[]

    
    with torch.no_grad():
        for filename in tqdm(image_files):
            try:
                image_path = os.path.join(image_folder, filename)
                image = Image.open(image_path).convert("RGB")

                image_input = preprocess(image)
                batch_images.append(image_input)
                batch_names.append(filename)
                batch_paths.append(image_path)

                if len(batch_images) == BATCH_SIZE:
                    image_tensor = torch.stack(batch_images).to(device)
                    batch_embeddings = model.encode_image(image_tensor).cpu().numpy()  # Move to CPU and convert to numpy
                    embeddings.extend(batch_embeddings)
                    valid_files.extend(batch_names)
                    valid_paths.extend(batch_paths)
                    batch_images, batch_names, batch_paths = [], [], []
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
        
        if batch_images:
            image_tensor = torch.stack(batch_images).to(device)
            batch_embeddings = model.encode_image(image_tensor).cpu().numpy()  # Move to CPU and convert to numpy
            embeddings.extend(batch_embeddings)
            valid_files.extend(batch_names)
            valid_paths.extend(batch_paths)

    # Convert to numpy array
    embeddings = np.array(embeddings)

    


    for i in range(0, len(valid_paths)):
        embedding_blob= embeddings[i].astype(np.float32).tobytes()
        cursor.execute("INSERT INTO Embeddings VALUES(?,?,?)", (valid_paths[i], valid_files[i], embedding_blob))
        
    conn.commit()

    return count



    
