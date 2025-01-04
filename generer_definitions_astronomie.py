# -*- coding: utf-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# Description:
# This script uses the local Ollama API to generate definitions and explanatory notes
# on astronomical objects from an Excel file. The script iterates over each row of the
# Excel file, sends requests to the API to obtain definitions in French, and saves the
# results in a new Excel file. If a type or subtype of object has already been processed,
# the script reuses the previously generated definition to avoid redundant API calls.
#
# Description :
# Ce script utilise l'API locale d'Ollama pour générer des définitions et des notes explicatives
# sur des objets astronomiques à partir d'un fichier Excel. Le script parcourt chaque ligne du
# fichier Excel, envoie des requêtes à l'API pour obtenir des définitions en français, et sauvegarde
# les résultats dans un nouveau fichier Excel. Si un type ou un sous-type d'objet a déjà été traité,
# le script réutilise la définition précédemment générée pour éviter des appels redondants à l'API.

# Origin of the Excel file:
# The Excel file used in this script comes from the Breakthrough Listen Exotica Catalog,
# a research project at the University of California, Berkeley. The Exotica Catalog is a
# collection of over 700 distinct celestial objects, aiming to include "one of everything"
# type of astronomical object known. It includes examples of each type in the Prototype sample,
# extreme objects with record properties in the Superlative sample, and enigmatic targets in the Anomaly sample.
#
# The Excel file was extracted from the source code of the scientific article "One of Everything:
# The Breakthrough Listen Exotica Catalog" available on arXiv. The conversion of the LaTeX table
# to an Excel file was done using the online converter available on TableConvert.
#
# Origine du fichier Excel :
# Le fichier Excel utilisé dans ce script provient du Catalogue Exotica de Breakthrough Listen,
# un projet de recherche de l'Université de Californie à Berkeley. Le Catalogue Exotica est une
# collection de plus de 700 objets célestes distincts, visant à inclure "un de chaque" type d'objet
# astronomique connu. Il comprend des exemples de chaque type dans l'échantillon Prototype, des objets
# extrêmes avec des propriétés record dans l'échantillon Superlative, et des cibles énigmatiques dans
# l'échantillon Anomaly.
#
# Le fichier Excel a été extrait du code source de l'article scientifique "One of Everything:
# The Breakthrough Listen Exotica Catalog" disponible sur arXiv. La conversion du tableau LaTeX
# en fichier Excel a été réalisée à l'aide du convertisseur en ligne disponible sur TableConvert.

# Import necessary libraries
# Importer les bibliothèques nécessaires
import pandas as pd
import requests
import json

# Load the Excel file
# Charger le fichier Excel
print("Loading the Excel file...")
print("Chargement du fichier Excel...")
df = pd.read_excel('updated_table.xlsx', engine='openpyxl')
print("Excel file loaded successfully.")
print("Fichier Excel chargé avec succès.")

# Dictionaries to store already generated definitions
# Dictionnaires pour stocker les définitions déjà générées
definitions_type = {}
definitions_subtype = {}
definitions_example = {}

# Function to generate text using the local Ollama API
# Fonction pour générer du texte avec l'API locale d'Ollama
def generate_text(prompt):
    print(f"Sending request to the API for the prompt: {prompt}")
    print(f"Envoi de la requête à l'API pour le prompt : {prompt}")
    response = requests.post(
        "http://localhost:11434/api/generate",  # Ensure the local API is accessible at this address
        # Assurez-vous que l'API locale est accessible à cette adresse
        json={"model": "llama3.3:70b-instruct-q2_K", "prompt": prompt}
    )
    
    # Debugging: Print the raw API response
    # Débogage : Afficher la réponse brute de l'API
    print("Raw API response:", response.text)
    print("Réponse brute de l'API:", response.text)
    
    # Assemble fragmented responses
    # Assembler les réponses fragmentées
    full_response = ""
    for line in response.text.splitlines():
        try:
            json_line = json.loads(line)
            full_response += json_line["response"]
            if json_line.get("done", False):
                break
        except json.JSONDecodeError as e:
            print("JSON decoding error:", e)
            print("Erreur de décodage JSON:", e)
            return "Text generation error"
            return "Erreur de génération de texte"
    
    print(f"Complete API response: {full_response}")
    print(f"Réponse complète de l'API : {full_response}")
    return full_response

# Iterate over the DataFrame rows and fill the columns
# Parcourir les lignes du DataFrame et remplir les colonnes
print("Starting to process DataFrame rows...")
print("Début du traitement des lignes du DataFrame...")
for index, row in df.iterrows():
    print(f"Processing row {index + 1}/{len(df)}")
    print(f"Traitement de la ligne {index + 1}/{len(df)}")
    type_query = row['Type']
    subtype_query = row['Sous-Type']
    example_query = row['Exemple']
    
    # Check if the type definition has already been generated
    # Vérifier si la définition du type a déjà été générée
    if type_query in definitions_type:
        df.at[index, 'Définition du type'] = definitions_type[type_query]
    else:
        definition_type = generate_text(f"Définition du type d'objet astronomique {type_query} en français:")
        definitions_type[type_query] = definition_type
        df.at[index, 'Définition du type'] = definition_type
    
    # Save the updated Excel file after each definition
    # Sauvegarder le fichier Excel mis à jour après chaque définition
    df.to_excel(f'updated_table_with_definitions_{index + 1}_type.xlsx', index=False)
    
    # Check if the subtype definition has already been generated
    # Vérifier si la définition du sous-type a déjà été générée
    subtype_key = (type_query, subtype_query)
    if subtype_key in definitions_subtype:
        df.at[index, 'Définition du sous-type'] = definitions_subtype[subtype_key]
    else:
        definition_subtype = generate_text(f"Définition du sous-type d'objet astronomique {subtype_query} de type {type_query} en français:")
        definitions_subtype[subtype_key] = definition_subtype
        df.at[index, 'Définition du sous-type'] = definition_subtype
    
    # Save the updated Excel file after each definition
    # Sauvegarder le fichier Excel mis à jour après chaque définition
    df.to_excel(f'updated_table_with_definitions_{index + 1}_subtype.xlsx', index=False)
    
    # Check if the explanatory note on the example has already been generated
    # Vérifier si la note explicative sur l'exemple a déjà été générée
    example_key = (type_query, subtype_query, example_query)
    if example_key in definitions_example:
        df.at[index, 'Note explicative sur l\'exemple'] = definitions_example[example_key]
    else:
        definition_example = generate_text(f"Note explicative sur l'exemple d'objet astronomique {type_query}, {subtype_query}, {example_query} en français:")
        definitions_example[example_key] = definition_example
        df.at[index, 'Note explicative sur l\'exemple'] = definition_example
    
    # Save the updated Excel file after each definition
    # Sauvegarder le fichier Excel mis à jour après chaque définition
    df.to_excel(f'updated_table_with_definitions_{index + 1}_example.xlsx', index=False)

print("Finished processing rows. Saving the final Excel file...")
print("Traitement des lignes terminé. Sauvegarde du fichier Excel final...")

# Save the final updated Excel file
# Sauvegarder le fichier Excel final mis à jour
df.to_excel('updated_table_with_definitions_final.xlsx', index=False)

print("The Excel file has been updated with definitions generated by LLaMA in French.")
print("Le fichier Excel a été mis à jour avec des définitions générées par LLaMA en français.")