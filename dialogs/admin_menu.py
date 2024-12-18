from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Group, Back
from aiogram_dialog.widgets.text import Const, Format

from handlers.admin_handlers import show_users, show_stats
from states.states import AdminDialogStates

# Главное меню админ-панели
main_menu = Window(
    Const("🔧 Админ-панель"),
    Button(
        Const("📊 Статистика"),
        id="stats_btn",
        on_click=lambda c, widget, manager: manager.switch_to(AdminDialogStates.stats)  # Переход к окну статистики
    ),
    Button(
        Const("📋 Пользователи"),
        id="users_btn",
        on_click=lambda c, widget, manager: manager.switch_to(AdminDialogStates.users)  # Переход к окну пользователей
    ),

    state=AdminDialogStates.admin_menu,
)


# Окно статистики
stats = Window(
    Format("📊 Статистика бота:\n"
           "Всего пользователей: {total_users}\n"
           "Пользователей сегодня: {today_users}\n"
           "Всего запросов: {total_requests}\n"
           "Запросов сегодня: {today_requests}"),
    Back(Const("Назад")),
    state=AdminDialogStates.stats,
    getter=show_stats  # Связь с функцией получения данных
)


# Окно списка пользователей
users = Window(
    Format(
        "📋 Список пользователей:\n\n"
        "{users_text}"  # Место для динамического текста
    ),
    Back(Const("Назад")),
    state=AdminDialogStates.users,
    getter=show_users  # Связь с функцией получения данных
)

# Диалог
admin_dialog = Dialog(
    main_menu,
    stats,
    users
)
