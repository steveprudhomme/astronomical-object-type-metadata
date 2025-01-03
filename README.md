# astronomical-object-type-metadata
Take astronomical object type dans subtype and convert them to exploitable metadata for photo
# Instructions pour exécuter le script :
Installer les bibliothèques nécessaires :

pip install pandas transformers torch openpyxl
Exécuter le script :

Assurez-vous que le fichier updated_table.xlsx est dans le même répertoire que le script.
Exécutez le script Python.
# Explications :
Chargement du fichier Excel : Utilisation de pandas pour lire le fichier Excel.
Initialisation de GPT-2 : Chargement du modèle GPT-2 et du tokenizer à partir de la bibliothèque transformers.
Fonction generate_text : Cette fonction génère du texte en utilisant GPT-2 basé sur un prompt donné.
Boucle sur les lignes du DataFrame : Pour chaque ligne, le script utilise GPT-2 pour générer les définitions des types, sous-types et exemples, puis les insère dans les colonnes appropriées.
Sauvegarde du fichier Excel mis à jour : Le fichier Excel est sauvegardé avec les nouvelles informations générées par GPT-2.
Ce script devrait vous permettre de générer les définitions et notes explicatives directement à l'aide de GPT-2 en mode local. Si vous avez des questions ou des ajustements à faire, n'hésitez pas à me le faire savoir !

