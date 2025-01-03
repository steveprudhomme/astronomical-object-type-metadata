import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Charger le fichier Excel
df = pd.read_excel('updated_table.xlsx', engine='openpyxl')

# Initialiser le modèle GPT-2 et le tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Fonction pour générer du texte avec GPT-2
def generate_text(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

# Parcourir les lignes du DataFrame et remplir les colonnes
for index, row in df.iterrows():
    type_query = row['Type']
    subtype_query = row['Sous-Type']
    example_query = row['Exemple']
    
    df.at[index, 'Définition du type'] = generate_text(f"Définition du type {type_query}:")
    df.at[index, 'Définition du sous-type'] = generate_text(f"Définition du sous-type {subtype_query}:")
    df.at[index, 'Note explicative sur l\'exemble'] = generate_text(f"Note explicative sur l'exemple {example_query}:")

# Sauvegarder le fichier Excel mis à jour
df.to_excel('updated_table_with_definitions.xlsx', index=False)

print("Le fichier Excel a été mis à jour avec des définitions générées par GPT-2.")