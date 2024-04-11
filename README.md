# Auto_douche

## Description

Auto douche est un programme python qui permet d'écouter un port série USB à fin que grace à une douchette (scanner de code barre) on puisse récupérer l'url du code barre scanné et faire un appel API pour mettre à jour le statut de production du produit scanné.

## Installation

Installer les dépendances du fichier requirements.txt

```bash
pip install -r requirements.txt
```

## Utilisation

Metter un raccourci dans le dossier de démarrage de windows pour lancer le programme au démarrage de windows.
Grace au mini fichier `py.py` on détecte où est situer python.

Exemple de raccourci:

```text
C:\Users\*****\AppData\Local\Microsoft\WindowsApps\python.exe C:/Users/*****/Desktop/douchette/script.py
```
