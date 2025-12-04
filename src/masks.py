import logging

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""

    logger.debug(f"Вызов get_mask_card_number с аргументом: {card_number}")

    try:
        if not card_number:
            logger.error("Получена пустая строка или None")
            return None

        if not isinstance(card_number, str):
            logger.error(f"Ожидалась строка, получен {type(card_number)}: {card_number}")
            return None

        if len(card_number) != 16:
            logger.warning(f"Некорректная длина номера карты: {len(card_number)} вместо 16")
            return None

        if not card_number.isdigit():
            logger.error(f"Номер карты содержит нецифровые символы: {card_number}")
            return None

        # Логирование проверки
        logger.info(f"Проверка номера карты {card_number} пройдена успешно")

        masked_card = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

        # Логирование результата
        logger.info(f"Маскировка карты выполнена: {masked_card}")
        return masked_card

    except Exception as e:
        # Логирование ошибки
        logger.error(f"Неожиданная ошибка при маскировке карты {card_number}: {str(e)}", exc_info=True)
        return None


def get_mask_account(account_number: str) -> str:
    """Функция маскировки банковского счета"""
    logger.debug(f"Вызов get_mask_account с аргументом: {account_number}")

    try:
        if not account_number:
            logger.error("Получена пустая строка или None")
            return None

        if not isinstance(account_number, str):
            logger.error(f"Ожидалась строка, получен {type(account_number)}: {account_number}")
            return None

        if len(account_number) < 4:
            logger.warning(f"Слишком короткий номер счета: {len(account_number)} символов (минимум 4)")
            return None

        if not account_number.isdigit():
            logger.error(f"Номер счета содержит нецифровые символы: {account_number}")
            return None

        # Логирование проверки
        logger.info(f"Проверка номера счета {account_number} пройдена успешно")

        masked_account = f"**{account_number[-4:]}"

        # Логирование результата
        logger.info(f"Маскировка счета выполнена: {masked_account}")
        return masked_account

    except Exception as e:
        # Логирование ошибки
        logger.error(f"Неожиданная ошибка при маскировке счета {account_number}: {str(e)}", exc_info=True)
        return None
