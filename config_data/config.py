from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]

@dataclass
class SaluteSpeech:
    credentials: str

@dataclass
class Config:
    tg_bot: TgBot
    salute_speech: SaluteSpeech

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        salute_speech=SaluteSpeech(
            credentials=env('SALUTE_CREDENTIALS')
        )
    )
