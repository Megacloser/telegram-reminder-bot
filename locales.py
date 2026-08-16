DEFAULT_LANG = "en"
SUPPORTED_LANGS = {
    "en": "English",
    "ru": "Русский",
    "de": "Deutsch",
}

TRANSLATIONS = {
    "en": {
        "start": (
            "👋 Hi! I'm a reminder bot.\n\n"
            "Use the buttons below — no need to type commands:\n"
            "⏰ New reminder — set a reminder step by step\n"
            "📋 My reminders — view and delete your reminders\n"
            "❓ Help — detailed instructions\n"
            "🌐 Language — change interface language\n\n"
            "Power users can also type: /remind 10m call the client"
        ),
        "help": (
            "📖 Setting a reminder:\n\n"
            "Tap the ⏰ New reminder button, pick a time (or choose ✍️ Custom and type your own, "
            "e.g. 10m, 2h, 1d), then type what to remind you about.\n\n"
            "Shortcut for typing it directly:\n"
            "/remind <time><unit> <text>\n"
            "  s — seconds, m — minutes, h — hours, d — days\n"
            "Example: /remind 10m call the client\n\n"
            "I will send the reminder text back to this chat once the time is up.\n"
            "Tap 📋 My reminders (or /myreminders) to see all your pending reminders and delete any of them.\n"
            "Use the 🌐 Language button (or /language) to switch between English, Русский and Deutsch.\n"
            "Use /cancel to abort setting a reminder."
        ),
        "remind_usage": (
            "⚠️ Usage: /remind <time><unit> <text>\n"
            "Example: /remind 10m call the client\n"
            "Units: s (seconds), m (minutes), h (hours), d (days)"
        ),
        "remind_invalid_time": (
            "⚠️ Couldn't understand the time '{value}'.\n"
            "Use a number followed by s/m/h/d, e.g. 10m, 2h, 1d."
        ),
        "remind_too_long": "⚠️ The reminder time is too far in the future. Please use up to 30 days.",
        "remind_set": "✅ Got it! I'll remind you in {when} about: {text}",
        "reminder_fired": "⏰ Reminder: {text}",
        "language_choose": "🌐 Choose your language:",
        "language_set": "✅ Language set to English.",
        "unit_s": "second(s)",
        "unit_m": "minute(s)",
        "unit_h": "hour(s)",
        "unit_d": "day(s)",
        "menu_remind": "⏰ New reminder",
        "menu_list": "📋 My reminders",
        "menu_language": "🌐 Language",
        "menu_help": "❓ Help",
        "menu_prompt": "Choose an option below 👇",
        "remind_pick_time": "⏰ In how long should I remind you?",
        "remind_custom_prompt": "Type the time, e.g. 10m, 2h, 1d:",
        "remind_ask_text": "✍️ What should I remind you about?",
        "remind_cancelled": "❌ Cancelled.",
        "btn_custom": "✍️ Custom",
        "reminders_header": "📋 Your reminders (tap 🗑 to delete):",
        "reminders_empty": "You have no active reminders.",
        "reminder_deleted": "🗑 Reminder deleted.",
    },
    "ru": {
        "start": (
            "👋 Привет! Я бот-напоминалка.\n\n"
            "Пользуйтесь кнопками ниже — команды вводить не обязательно:\n"
            "⏰ Новое напоминание — пошаговая настройка\n"
            "📋 Мои напоминания — просмотр и удаление напоминаний\n"
            "❓ Помощь — подробная инструкция\n"
            "🌐 Язык — сменить язык интерфейса\n\n"
            "Для опытных: можно и командой — /remind 10m позвонить клиенту"
        ),
        "help": (
            "📖 Как поставить напоминание:\n\n"
            "Нажмите кнопку ⏰ Новое напоминание, выберите время (или ✍️ Своё время и введите его "
            "вручную, например 10m, 2h, 1d), затем напишите текст напоминания.\n\n"
            "Быстрый способ одной командой:\n"
            "/remind <время><единица> <текст>\n"
            "  s — секунды, m — минуты, h — часы, d — дни\n"
            "Пример: /remind 10m позвонить клиенту\n\n"
            "Когда время истечёт, я пришлю текст напоминания в этот же чат.\n"
            "Кнопка 📋 Мои напоминания (или /myreminders) показывает все ваши напоминания и позволяет удалить любое из них.\n"
            "Кнопка 🌐 Язык (или команда /language) переключает между English, Русский и Deutsch.\n"
            "Команда /cancel отменяет настройку напоминания."
        ),
        "remind_usage": (
            "⚠️ Использование: /remind <время><единица> <текст>\n"
            "Пример: /remind 10m позвонить клиенту\n"
            "Единицы: s (секунды), m (минуты), h (часы), d (дни)"
        ),
        "remind_invalid_time": (
            "⚠️ Не удалось распознать время '{value}'.\n"
            "Используйте число с буквой s/m/h/d, например 10m, 2h, 1d."
        ),
        "remind_too_long": "⚠️ Слишком большой срок. Максимум — 30 дней.",
        "remind_set": "✅ Хорошо! Напомню через {when} о: {text}",
        "reminder_fired": "⏰ Напоминание: {text}",
        "language_choose": "🌐 Выберите язык:",
        "language_set": "✅ Установлен русский язык.",
        "unit_s": "сек.",
        "unit_m": "мин.",
        "unit_h": "ч.",
        "unit_d": "дн.",
        "menu_remind": "⏰ Новое напоминание",
        "menu_list": "📋 Мои напоминания",
        "menu_language": "🌐 Язык",
        "menu_help": "❓ Помощь",
        "menu_prompt": "Выберите действие ниже 👇",
        "remind_pick_time": "⏰ Через сколько напомнить?",
        "remind_custom_prompt": "Введите время, например 10m, 2h, 1d:",
        "remind_ask_text": "✍️ О чём напомнить?",
        "remind_cancelled": "❌ Отменено.",
        "btn_custom": "✍️ Своё время",
        "reminders_header": "📋 Ваши напоминания (нажмите 🗑, чтобы удалить):",
        "reminders_empty": "У вас нет активных напоминаний.",
        "reminder_deleted": "🗑 Напоминание удалено.",
    },
    "de": {
        "start": (
            "👋 Hallo! Ich bin ein Erinnerungs-Bot.\n\n"
            "Nutze die Schaltflächen unten — Befehle sind nicht nötig:\n"
            "⏰ Neue Erinnerung — Schritt-für-Schritt einrichten\n"
            "📋 Meine Erinnerungen — Erinnerungen ansehen und löschen\n"
            "❓ Hilfe — ausführliche Anleitung\n"
            "🌐 Sprache — Sprache ändern\n\n"
            "Für Profis geht auch: /remind 10m Kunden anrufen"
        ),
        "help": (
            "📖 So stellst du eine Erinnerung ein:\n\n"
            "Tippe auf ⏰ Neue Erinnerung, wähle eine Zeit (oder ✍️ Eigene Zeit und gib sie selbst ein, "
            "z. B. 10m, 2h, 1d), und schreibe dann den Erinnerungstext.\n\n"
            "Abkürzung per Befehl:\n"
            "/remind <Zeit><Einheit> <Text>\n"
            "  s — Sekunden, m — Minuten, h — Stunden, d — Tage\n"
            "Beispiel: /remind 10m Kunden anrufen\n\n"
            "Sobald die Zeit abgelaufen ist, sende ich den Text zurück in diesen Chat.\n"
            "Mit 📋 Meine Erinnerungen (oder /myreminders) siehst du alle offenen Erinnerungen und kannst sie löschen.\n"
            "Mit der Schaltfläche 🌐 Sprache (oder /language) wechselst du zwischen English, Русский und Deutsch.\n"
            "Mit /cancel brichst du die Einrichtung ab."
        ),
        "remind_usage": (
            "⚠️ Verwendung: /remind <Zeit><Einheit> <Text>\n"
            "Beispiel: /remind 10m Kunden anrufen\n"
            "Einheiten: s (Sekunden), m (Minuten), h (Stunden), d (Tage)"
        ),
        "remind_invalid_time": (
            "⚠️ Zeit '{value}' konnte nicht erkannt werden.\n"
            "Bitte eine Zahl gefolgt von s/m/h/d verwenden, z. B. 10m, 2h, 1d."
        ),
        "remind_too_long": "⚠️ Der Zeitraum ist zu lang. Maximal 30 Tage sind erlaubt.",
        "remind_set": "✅ Alles klar! Ich erinnere dich in {when} an: {text}",
        "reminder_fired": "⏰ Erinnerung: {text}",
        "language_choose": "🌐 Sprache wählen:",
        "language_set": "✅ Sprache auf Deutsch eingestellt.",
        "unit_s": "Sekunde(n)",
        "unit_m": "Minute(n)",
        "unit_h": "Stunde(n)",
        "unit_d": "Tag(e)",
        "menu_remind": "⏰ Neue Erinnerung",
        "menu_list": "📋 Meine Erinnerungen",
        "menu_language": "🌐 Sprache",
        "menu_help": "❓ Hilfe",
        "menu_prompt": "Wähle unten eine Option 👇",
        "remind_pick_time": "⏰ In wie viel Zeit soll ich dich erinnern?",
        "remind_custom_prompt": "Gib die Zeit ein, z. B. 10m, 2h, 1d:",
        "remind_ask_text": "✍️ Woran soll ich dich erinnern?",
        "remind_cancelled": "❌ Abgebrochen.",
        "btn_custom": "✍️ Eigene Zeit",
        "reminders_header": "📋 Deine Erinnerungen (🗑 zum Löschen antippen):",
        "reminders_empty": "Du hast keine aktiven Erinnerungen.",
        "reminder_deleted": "🗑 Erinnerung gelöscht.",
    },
}


def all_translations(key: str) -> set[str]:
    return {TRANSLATIONS[lang][key] for lang in TRANSLATIONS if key in TRANSLATIONS[lang]}


def t(key: str, lang: str, **kwargs) -> str:
    lang = lang if lang in TRANSLATIONS else DEFAULT_LANG
    template = TRANSLATIONS[lang].get(key, TRANSLATIONS[DEFAULT_LANG][key])
    return template.format(**kwargs) if kwargs else template
