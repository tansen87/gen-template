import logging
from colorama import Fore, Style, init

class Log:
    init(autoreset=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt="%H:%M:%S"
    )

    @staticmethod
    def info(message: str):
        logging.info(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    @staticmethod
    def warning(message: str):
        logging.warning(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

    @staticmethod
    def error(message: str):
        logging.error(f"{Fore.RED}{message}{Style.RESET_ALL}")
