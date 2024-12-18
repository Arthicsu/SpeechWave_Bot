LEXICON_RU: dict[str, str] = {
    '/start': 'Это Бот WaveSpeech 🦾. \nПросто отправьте/перешлите голосовое сообщение нашему боту.\n'
              'Используйте кнопку "Изменить язык", чтобы изменить язык.\nБесплатно для транскрибации доступны языки: русский, английский.\n'
              'Платные языки в премиум-подписке: казахский.\nПеревод транскрибации бесплатный. Спасибо, Яндекс ❤️',
    '/help': 'Это Бот WaveSpeech\n\nДоступные команды:\n\nКнопка "Изменить язык" - '
             'изменить язык перевода (доступны русский, английский, казахский)\n - проверить доступность платных языков ',
    '/lang_transcrib': 'Выберите язык для транскрибации!',
    'lang_cng': 'Вы изменили язык на русский! Привет!',
    'translate_on': 'Перевод на русский:',
    '/admin': 'Вы зашли в админ панель.',
}

LEXICON_KZ: dict[str, str] = {
    'lang_cng': 'сіз тілді қазақ тіліне өзгерттіңіз! Сәлем!',
    'translate_on': 'Қазақ тіліне аударылған:',
}

LEXICON_EN: dict[str, str] = {
    'lang_cng': 'You have changed the language to English! Hi!',
    'translate_on': 'Translate to English:',
}

LEXICON_FR: dict[str, str] = {
    'lang_cng': 'Vous avez changé la langue en français! Bonjour!',
    'translate_on': 'Traduction en français:',
}

LEXICON_DE: dict[str, str] = {
    'lang_cng': 'Sie haben die Sprache auf Deutsch geändert! Hallo!',
    'translate_on': 'Übersetzung ins Deutsche:',
}

LEXICON_ES: dict[str, str] = {
    'lang_cng': '¡Has cambiado el idioma a español! ¡Hola!',
    'translate_on': 'Traducción al español:',
}

LANG_LEXICON = {
    "ru": LEXICON_RU,
    "en": LEXICON_EN,
    "kz": LEXICON_KZ,
    "fr": LEXICON_FR,
    "de": LEXICON_DE,
    "es": LEXICON_ES,
}

LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Стартуем бота',
    '/admin': 'админ-панель',
}