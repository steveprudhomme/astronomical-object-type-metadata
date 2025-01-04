import pandas as pd
import requests
import json

# Charger le fichier Excel
print("Chargement du fichier Excel...")
df = pd.read_excel('updated_table.xlsx', engine='openpyxl')
print("Fichier Excel chargé avec succès.")

# Dictionnaires pour stocker les définitions déjà générées
definitions_type = {}
definitions_subtype = {}
definitions_example = {}

# Fonction pour générer du texte avec l'API locale d'Ollama
def generate_text(prompt):
    print(f"Envoi de la requête à l'API pour le prompt : {prompt}")
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
    
    print(f"Réponse complète de l'API : {full_response}")
    return full_response

# Parcourir les lignes du DataFrame et remplir les colonnes
print("Début du traitement des lignes du DataFrame...")
for index, row in df.iterrows():
    print(f"Traitement de la ligne {index + 1}/{len(df)}")
    type_query = row['Type']
    subtype_query = row['Sous-Type']
    example_query = row['Exemple']
    
    # Vérifier si la définition du type a déjà été générée
    if type_query in definitions_type:
        df.at[index, 'Définition du type'] = definitions_type[type_query]
    else:
        definition_type = generate_text(f"Définition du type d'objet astronomique {type_query} en français:")
        definitions_type[type_query] = definition_type
        df.at[index, 'Définition du type'] = definition_type
    
    # Sauvegarder le fichier Excel mis à jour après chaque définition
    df.to_excel(f'updated_table_with_definitions_{index + 1}_type.xlsx', index=False)
    
    # Vérifier si la définition du sous-type a déjà été générée
    subtype_key = (type_query, subtype_query)
    if subtype_key in definitions_subtype:
        df.at[index, 'Définition du sous-type'] = definitions_subtype[subtype_key]
    else:
        definition_subtype = generate_text(f"Définition du sous-type d'objet astronomique {subtype_query} de type {type_query} en français:")
        definitions_subtype[subtype_key] = definition_subtype
        df.at[index, 'Définition du sous-type'] = definition_subtype
    
    # Sauvegarder le fichier Excel mis à jour après chaque définition
    df.to_excel(f'updated_table_with_definitions_{index + 1}_subtype.xlsx', index=False)
    
    # Vérifier si la note explicative sur l'exemple a déjà été générée
    example_key = (type_query, subtype_query, example_query)
    if example_key in definitions_example:
        df.at[index, 'Note explicative sur l\'exemple'] = definitions_example[example_key]
    else:
        definition_example = generate_text(f"Note explicative sur l'exemple d'objet astronomique {type_query}, {subtype_query}, {example_query} en français:")
        definitions_example[example_key] = definition_example
        df.at[index, 'Note explicative sur l\'exemple'] = definition_example
    
    # Sauvegarder le fichier Excel mis à jour après chaque définition
    df.to_excel(f'updated_table_with_definitions_{index + 1}_example.xlsx', index=False)

print("Traitement des lignes terminé. Sauvegarde du fichier Excel...")

# Sauvegarder le fichier Excel final mis à jour
df.to_excel('updated_table_with_definitions_final.xlsx', index=False)

print("Le fichier Excel a été mis à jour avec des définitions générées par LLaMA en français.")