import logging
import os

#Creamos carpeta de logs si no existe
os.makedirs("logs", exist_ok=True)

#Configuramos el logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s %(message)s]",
    handlers=[
        logging.FileHandler("logs/sistema.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SistemaFJ")

def registrar_info(mensaje):
    logger.info(mensaje)

def registrar_error(mensaje):
    logger.error(mensaje)

def registrar_advertencia(mensaje):
    logger.warning(mensaje)