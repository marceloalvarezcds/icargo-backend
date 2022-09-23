from app import logger


def send_sms(phone_number: str, message: str):
    logger.info(f"Enviando sms a {phone_number} con mensaje = {message}")
