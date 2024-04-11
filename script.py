import serial
import serial.tools.list_ports
import logging
import datetime
import os
import requests
from urllib.parse import urlparse
from logging.handlers import TimedRotatingFileHandler

# Créer un logger
logger = logging.getLogger("Logger")
logger.setLevel(logging.INFO)

# Créer un répertoire pour les logs
log_dir = os.path.join(os.getcwd(), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Déterminer la date actuelle
today = datetime.date.today()

# Créer un gestionnaire de fichiers pour le jour actuel
handler = TimedRotatingFileHandler(
    os.path.join(log_dir, f"log-{today:%Y_%m_%d}"), when="midnight", interval=1
)
handler.suffix = "%Y-%m-%d"
logger.addHandler(handler)

# Créer un format de message de journalisation
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)

# Fonction pour créer un nouveau fichier de log si nécessaire
def create_new_log_file(new_day):
    global handler
    # Fermer le gestionnaire actuel
    handler.close()

    # Créer un nouveau gestionnaire pour le nouveau jour
    handler = TimedRotatingFileHandler(
        os.path.join(log_dir, f"log-{new_day:%Y_%m_%d}"), when="midnight", interval=1
    )
    handler.suffix = "%Y-%m-%d"
    logger.addHandler(handler)

# Lister les ports série disponibles
for port in serial.tools.list_ports.comports():
    print(f"{port}")

# Essayer de se connecter au port série
try:
    ser = serial.Serial(port="COM4", baudrate=9600, timeout=1)
except serial.SerialException as e:
    logger.error(f"Erreur de connexion série : {e}")
    print(f"Erreur de connexion série : {e}")
    exit()

# Boucle principale
while True:
    # Lire les données du port série
    data = ser.readline()

    # Si des données sont reçues
    if data:
        try:
            # Décoder les données et supprimer les caractères de fin de ligne
            url = data.decode("utf-8").strip()

            # Vérifier si l'URL est valide
            if not url or not urlparse(url).scheme or not urlparse(url).netloc:
                raise ValueError("URL invalide")

            # Effectuer une requête HTTP GET
            response = requests.request("GET", url)

        except ValueError as e:
            logger.error(f"Erreur de formatage de l'URL : {e}")
            continue

        except requests.RequestException as e:
            logger.error(f"Erreur de requête HTTP : {e}")
            continue

        # Vérifier la date et créer un nouveau fichier de log si nécessaire
        new_day = datetime.date.today()
        if new_day != today:
            today = new_day
            create_new_log_file(new_day)

        # Journaliser le code de retour HTTP
        logger.info(f"{url} - Reponse HTTP : {response.status_code}")

        # Afficher le code de retour HTTP
        print(f"Code de retour HTTP : {response.status_code}")

        if response.status_code == 200:
            logger.info(f"{url} - Reponse HTTP : {response.status_code}")
            # Si le code de retour HTTP est 200, on affiche le contenu de la réponse.
            print("Le serveur a répondu avec succès.")
        else:
            logger.error(f"{url} - Reponse HTTP : {response.status_code}")
            # Si le code de retour HTTP est différent de 200, on affiche une erreur.
            print(f"Le serveur a répondu avec une erreur : {response.status_code}")
