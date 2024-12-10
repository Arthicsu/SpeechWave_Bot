from aiogram.fsm.state import State, StatesGroup

class States(StatesGroup):
    waiting_for_language = State()
    waiting_for_voice_message = State()