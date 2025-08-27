import torch

# Load the file
all_data = torch.load("all_embeddings.pt")

# Print all folder keys
print("Folders stored:", all_data.keys())

# Pick a folder key
folder_path = list(all_data.keys())[0]  # just take the first one
folder_data = all_data[folder_path]

# List of image filenames
print("Files:", folder_data["files"])

# Shape of embeddings
print("Embeddings shape:", folder_data["embeddings"].shape)
