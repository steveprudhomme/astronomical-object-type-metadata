import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Charger le fichier Excel
df = pd.read_excel('updated_table.xlsx', engine='openpyxl')

# Initialiser le modèle LLaMA 3 et le tokenizer
model_name = "meta-llama/Meta-Llama-3-8B-Instruct"  # Remplacez par le chemin correct vers le modèle LLaMA 3
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, use_auth_token=True)

# Fonction pour générer du texte avec LLaMA 3 en français
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
    df.at[index, 'Note explicative sur l\'exemple'] = generate_text(f"Note explicative sur l'exemple {example_query} en français:")

# Sauvegarder le fichier Excel mis à jour
df.to_excel('updated_table_with_definitions.xlsx', index=False)

print("Le fichier Excel a été mis à jour avec des définitions générées par LLaMA 3 en français.")