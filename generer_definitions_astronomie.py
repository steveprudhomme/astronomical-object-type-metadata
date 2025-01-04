import pandas as pd
import requests
import json

# Charger le fichier Excel
df = pd.read_excel('updated_table.xlsx', engine='openpyxl')

# Fonction pour générer du texte avec l'API locale d'Ollama
def generate_text(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",  # Assurez-vous que l'API locale est accessible à cette adresse
        json={"model": "llama3.3:70b-instruct-q2_K", "prompt": prompt}
    )
    
    # Débogage : Afficher la réponse brute
    print("Réponse brute de l'API:", response.text)
    
    # Assembler les réponses fragmentées
    full_response = ""
    for line in response.text.splitlines():
        try:
            json_line = json.loads(line)
            full_response += json_line["response"]
            if json_line.get("done", False):
                break
        except json.JSONDecodeError as e:
            print("Erreur de décodage JSON:", e)
            return "Erreur de génération de texte"
    
    return full_response

# Parcourir les lignes du DataFrame et remplir les colonnes
for index, row in df.iterrows():
    type_query = row['Type']
    subtype_query = row['Sous-Type']
    example_query = row['Exemple']
    
    df.at[index, 'Définition du type'] = str(generate_text(f"Définition du type d'objet astronomique {type_query} en français:"))
    df.at[index, 'Définition du sous-type'] = str(generate_text(f"Définition du sous-type d'objet astronomique {subtype_query} de type {type_query} en français:"))
    df.at[index, 'Note explicative sur l\'exemple'] = str(generate_text(f"Note explicative sur l'exemple d'objet astronomique {type_query}, {subtype_query}, {example_query} en français:"))

# Sauvegarder le fichier Excel mis à jour
df.to_excel('updated_table_with_definitions.xlsx', index=False)

print("Le fichier Excel a été mis à jour avec des définitions générées par LLaMA en français.")