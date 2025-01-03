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
Échappement des guillemets simples : Dans la ligne où vous avez rencontré l'erreur, j'ai échappé le guillemet simple dans l'exemple en utilisant une barre oblique inversée (\). Cela permet d'éviter la confusion avec la fin de la chaîne de caractères.
Définition de attention_mask : Ajout d'un masque d'attention pour les entrées afin d'améliorer la fiabilité des résultats.
Définition de pad_token_id : Utilisation du token de fin de séquence (eos_token_id) comme pad_token_id pour éviter les comportements inattendus.
Ce script devrait maintenant fonctionner correctement et générer des définitions en français pour les types, sous-types et exemples dans votre fichier Excel. Si vous rencontrez d'autres problèmes ou avez besoin d'ajustements supplémentaires, n'hésitez pas à me le faire savoir !