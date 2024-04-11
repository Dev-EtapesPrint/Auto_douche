import os
import datetime
import logging
import serial
import serial.tools.list_ports
import webbrowser
from urllib.parse import urlparse
from logging.handlers import TimedRotatingFileHandler

# Configuration du logger
logger = logging.getLogger("Logger")
logger.setLevel(logging.INFO)

# Définition du répertoire et du format des logs
log_dir = os.path.join(os.getcwd(), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

today = datetime.date.today()
handler = TimedRotatingFileHandler(
    os.path.join(log_dir, f"log-{today:%Y_%m_%d}.log"), when="midnight", interval=1
)
handler.suffix = "%Y-%m-%d"
logger.addHandler(handler)

formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)


def create_new_log_file(new_day):
    global handler
    handler.close()

    handler = TimedRotatingFileHandler(
        os.path.join(log_dir, f"log-{new_day:%Y_%m_%d}.log"),
        when="midnight",
        interval=1,
    )
    handler.suffix = "%Y-%m-%d"
    logger.addHandler(handler)


# Connexion au port série
try:
    print("Connexion série en cours...")
    ser = serial.Serial(port="COM6", baudrate=9600, timeout=1)
    print("Connexion série établie")
except serial.SerialException as e:
    logger.error(f"Erreur de connexion série : {e}")
    print(f"Erreur de connexion série : {e}")
    for port in serial.tools.list_ports.comports():
        print(f"{port}")
    input("Appuyez sur une touche pour quitter...")
    exit()

# Boucle principale
while True:
    data = ser.readline()

    if data:
        new_day = datetime.date.today()
        if new_day != today:
            today = new_day
            create_new_log_file(new_day)

        try:
            url = data.decode("utf-8").strip()

            # Vérification de la validité de l'URL
            if not url or not urlparse(url).scheme or not urlparse(url).netloc:
                raise ValueError("URL invalide")

            webbrowser.open(url)

        except ValueError as e:
            logger.error(f"Erreur de formatage de l'URL : {e}")
            print(f"Erreur de formatage de l'URL : {e}")
            continue

        except Exception as e:
            logger.error(f"Erreur inconnue : {e}")
            print(f"Erreur inconnue : {e}")
            continue

        logger.info(f"{url} - Ouvert dans le navigateur")
        print(f"{url} - Ouvert dans le navigateur")
