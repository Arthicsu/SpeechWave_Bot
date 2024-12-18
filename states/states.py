from aiogram.fsm.state import State, StatesGroup

# Состояния для существующего функционала
class States(StatesGroup):
    waiting_for_language = State()
    waiting_for_voice_message = State()

# состояния для админ-панельки
class AdminDialogStates(StatesGroup):
    admin_menu = State()
    stats = State()
    users = State()