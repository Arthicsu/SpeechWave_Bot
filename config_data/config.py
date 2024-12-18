from dataclasses import dataclass  # Используется для создания простых классов данных
from environs import Env  # Библиотека для удобной работы с переменными окружения

# Определяем класс для хранения параметров Telegram-бота
@dataclass
class TgBot:
    token: str  # Токен для взаимодействия с Telegram Bot API
    admin_ids: list[int]  # Список ID администраторов (целые числа)

# Определяем класс для хранения параметров модуля SaluteSpeech
@dataclass
class SaluteSpeech:
    credentials: str  # Данные авторизации для SaluteSpeech

# Определяем класс для хранения параметров Яндекс Переводчика
@dataclass
class YandexTranslate:
    iam_token: str  # IAM-токен для доступа к API Яндекса
    folder_id: str  # ID папки для использования сервисов Яндекса

# Главный класс конфигурации, объединяющий все остальные настройки
@dataclass
class Config:
    tg_bot: TgBot  # Настройки Telegram-бота
    salute_speech: SaluteSpeech  # Настройки SaluteSpeech
    yandex_translate: YandexTranslate  # Настройки Яндекс Переводчика

# Функция загрузки конфигурации из файла окружения
def load_config(path: str | None = None) -> Config:
    """
    Загружает конфигурацию из файла .env.

    :param path: Путь до файла .env. Если None, используется файл по умолчанию.
    :return: Объект Config, содержащий все настройки.
    """
    env = Env()  # Создаем экземпляр для работы с переменными окружения
    env.read_env(path)  # Читаем переменные окружения из файла .env

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),  # Считываем токен бота
            admin_ids=[int(admin_id.strip()) for admin_id in env.list('ADMIN_IDS')]
            # Считываем список ID администраторов и преобразуем их в целые числа
        ),
        salute_speech=SaluteSpeech(
            credentials=env('SALUTE_CREDENTIALS')  # Считываем данные авторизации SaluteSpeech
        ),
        yandex_translate=YandexTranslate(
            iam_token=env('YANDEX_IAM_TOKEN'),  # Считываем IAM-токен для Яндекса
            folder_id=env('YANDEX_FOLDER_ID')  # Считываем ID папки Яндекса
        )
    )