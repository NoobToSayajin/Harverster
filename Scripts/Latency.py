# Python included libraries
import subprocess
import logging
from logging.handlers import TimedRotatingFileHandler

# PIP libraries

# Custom libraries
from Debug.Log import Timer

class Latency:
    # ---------- log ----------
    logger_latency: logging.Logger = logging.getLogger(__name__)
    logger_latency.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:ligne_%(lineno)d -> %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger_latency.addHandler(stream_handler)
    
    def __init__(self, host: str, timeout: int = 1):
        """
        Initialise la classe Latency.
        :param host: L'hôte à pinger (par exemple, "google.com" ou "192.168.1.1").
        :param timeout: Le temps d'attente maximal pour une réponse (en secondes).
        """
        self.__host = host
        self.__timeout = timeout

    def ping(self) -> float:
        """
        Envoie un ping à l'hôte et retourne la latence en millisecondes.
        Retourne -1 si le ping échoue.
        """
        try:
            # Utiliser la commande système ping
            output = subprocess.run(
                ["ping", "-c", "1", "-W", str(self.__timeout), self.__host],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Vérifier si le ping a réussi
            if output.returncode == 0:
                # Extraire le temps de réponse du ping
                time_line = [line for line in output.stdout.splitlines() if "time=" in line][0]
                latency = float(time_line.split("time=")[1].split(" ms")[0])
                return latency
            else:
                # Retourner -1 si le ping échoue
                return -1
        except Exception as e:
            # En cas d'erreur, afficher un message et retourner -1
            Latency.logger_latency.error(f"Erreur lors de l'exécution de ping: {e}")
            return -1