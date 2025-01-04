import tarfile
import os

blob_path = "C:/Users/steve/.ollama/models/blobs/sha256-<votre_hash>"  # Remplacez par le chemin correct vers le fichier blob
extract_path = "C:/Users/steve/.ollama/models/llama3"  # Chemin où vous souhaitez extraire les fichiers

# Assurez-vous que le répertoire de destination existe
os.makedirs(extract_path, exist_ok=True)

# Extraire les fichiers du blob
with tarfile.open(blob_path, "r:*") as tar:
    tar.extractall(path=extract_path)

print(f"Les fichiers ont été extraits dans {extract_path}")
Utiliser les fichiers extraits dans votre script : Une fois les fichiers extraits, vous pouvez les utiliser dans votre script Python avec transformers. Voici comment adapter votre script :

import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Charger le fichier Excel
df = pd.read_excel('updated_table.xlsx', engine='openpyxl')

# Initialiser le modèle LLaMA et le tokenizer à partir des fichiers locaux
model_path = "C:/Users/steve/.ollama/models/llama3"  # Chemin vers le répertoire contenant les fichiers extraits
tokenizer_path = "C:/Users/steve/.ollama/models/llama3"  # Chemin vers le répertoire contenant le tokenizer

tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16)

# Fonction pour générer du texte avec LLaMA en français
def generate_text(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = torch.ones(inputs.shape, dtype=torch.long)
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1, attention_mask=attention_mask, pad_token_id=tokenizer.eos_token_id)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

# Parcourir les lignes du DataFrame et remplir les colonnes
for index, row in df.iterrows():
    type_query = row['Type']
    subtype_query = row['Sous-Type']
    example_query = row['Exemple']
    
    df.at[index, 'Définition du type'] = generate_text(f"Définition du type {type_query} en français:")
    df.at[index, 'Définition du sous-type'] = generate_text(f"Définition du sous-type {subtype_query} en français:")
    df.at[index, 'Note explicative sur l'exemple'] = generate_text(f"Note explicative sur l'exemple {example_query} en français:")

# Sauvegarder le fichier Excel mis à jour
df.to_excel('updated_table_with_definitions.xlsx', index=False)

print("Le fichier Excel a été mis à jour avec des définitions générées par LLaMA en français.")