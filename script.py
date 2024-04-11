import serial
import serial.tools.list_ports
import logging
import datetime
import os
import requests
from logging.handlers import TimedRotatingFileHandler
from urllib.parse import urlparse

# Créer un logger
logger = logging.getLogger("Logger")
logger.setLevel(logging.INFO)

# Créer un gestionnaire de fichiers qui écrit dans un nouveau fichier chaque jour à minuit.
log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
handler = TimedRotatingFileHandler(os.path.join(log_dir, "log"), when="midnight", interval=1)
handler.suffix = "%Y-%m-%d"
logger.addHandler(handler)

# Créer un format de message de journalisation.
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)


"""
On liste les ports série disponibles sur la machine.
"""
for port in serial.tools.list_ports.comports():
    print(f"{port}")

"""
On essaie de se connecter au port série COM6 à une vitesse de 9600 bauds.
"""
try:
    ser = serial.Serial(port="COM4", baudrate=9600, timeout=1)
except serial.SerialException as e:
    logger.error(f"Erreur de connexion série : {e}")
    print(f"Erreur de connexion série : {e}")
    exit()

"""
Tant que le programme est en cours d'exécution, on lit les données reçues sur le port série.
"""
while True:
    # On lit les données reçues sur le port série.
    data = ser.readline()
    # Si on a reçu des données.
    if data:
        try:
            # On décode les données reçues en UTF-8 et on supprime les caractères de fin de ligne.
            url = data.decode("utf-8").strip()
            parsed_url = urlparse(url)
            # On vérifie que l'URL est bien formée.
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("URL invalide")
        # Si une erreur de formatage de l'URL est levée.
        except ValueError as e:
            print(f"Erreur de formatage de l'URL : {e}")
            continue

        try:
            # On effectue une requête HTTP GET à l'URL reçue.
            response = requests.request("GET", url)
        except requests.RequestException as e:
            # Si une erreur de requête HTTP est levée.
            print(f"Erreur de requête HTTP : {e}")
            continue

        # On affiche le code de retour HTTP de la réponse.
        print(f"Code de retour HTTP : {response.status_code}")

        if response.status_code == 200:
            logger.info(f"{url} - Reponse HTTP : {response.status_code}")
            # Si le code de retour HTTP est 200, on affiche le contenu de la réponse.
            print("Le serveur a répondu avec succès.")
        else:
            logger.error(f"{url} - Reponse HTTP : {response.status_code}")
            # Si le code de retour HTTP est différent de 200, on affiche une erreur.
            print(f"Le serveur a répondu avec une erreur : {response.status_code}")
