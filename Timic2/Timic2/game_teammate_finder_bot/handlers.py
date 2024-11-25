import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, \
    filters, ContextTypes

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Константи для етапів реєстрації
CHOOSE_LANGUAGE, REGISTER, CHOOSE_PLATFORM, FIND_TEAMMATES, VIEW_USERS = range(5)

# Вибір мов
LANGUAGES = {
    "English": "en",
    "Українська": "uk",
    "Deutsch": "de",
    "Français": "fr",
    "Italiano": "it",
    "Español": "es",
    "中文 (Chinese)": "zh",
    "한국어 (Korean)": "ko",
    "Polski": "pl"
}

# Текстові повідомлення на різних мовах
MESSAGES = {
    "en": {
        "choose_language": "Please choose your language:",
        "register_username": "Please enter your username:",
        "choose_platform": "Please choose your platform:",
        "thank_you": "Thank you, {}! Now select a game to find teammates.",
        "choose_game": "Choose a game:",
        "teammates_found": "Teammates found:\n{}",
        "no_teammates": "No teammates found at the moment.",
        "language_selected": "Language selected: {}. Please register with /register.",
        "platform_selected": "Platform selected: {}.",
        "view_users": "Registered users filtered by platform: {}",
        "choose_platform_filter": "Select a platform to filter users:"
    },
    "uk": {
        "choose_language": "Будь ласка, оберіть мову:",
        "register_username": "Будь ласка, введіть ваше ім'я користувача:",
        "choose_platform": "Будь ласка, оберіть платформу:",
        "thank_you": "Дякуємо, {}! Тепер виберіть гру, щоб знайти товаришів по команді.",
        "choose_game": "Оберіть гру:",
        "teammates_found": "Знайдені товариші по команді:\n{}",
        "no_teammates": "Зараз немає товаришів по команді.",
        "language_selected": "Мова обрана: {}. Будь ласка, зареєструйтесь за допомогою /register.",
        "platform_selected": "Платформа обрана: {}.",
        "view_users": "Зареєстровані користувачі, відфільтровані за платформою: {}",
        "choose_platform_filter": "Оберіть платформу для фільтрації користувачів:"
    },
    "de": {
        "choose_language": "Bitte wählen Sie Ihre Sprache:",
        "register_username": "Bitte geben Sie Ihren Benutzernamen ein:",
        "choose_platform": "Bitte wählen Sie Ihre Plattform:",
        "thank_you": "Danke, {}! Wählen Sie jetzt ein Spiel, um Mitspieler zu finden.",
        "choose_game": "Wählen Sie ein Spiel:",
        "teammates_found": "Gefundene Mitspieler:\n{}",
        "no_teammates": "Momentan keine Mitspieler gefunden.",
        "language_selected": "Sprache ausgewählt: {}. Bitte registrieren Sie sich mit /register.",
        "platform_selected": "Plattform ausgewählt: {}.",
        "view_users": "Registrierte Benutzer nach Plattform gefiltert: {}",
        "choose_platform_filter": "Wählen Sie eine Plattform, um Benutzer zu filtern:"
    },
    "fr": {
        "choose_language": "Veuillez choisir votre langue :",
        "register_username": "Veuillez entrer votre nom d'utilisateur :",
        "choose_platform": "Veuillez choisir votre plateforme :",
        "thank_you": "Merci, {}! Sélectionnez maintenant un jeu pour trouver des coéquipiers.",
        "choose_game": "Choisissez un jeu :",
        "teammates_found": "Coéquipiers trouvés :\n{}",
        "no_teammates": "Aucun coéquipier trouvé pour le moment.",
        "language_selected": "Langue sélectionnée : {}. Veuillez vous inscrire avec /register.",
        "platform_selected": "Plateforme sélectionnée : {}.",
        "view_users": "Utilisateurs inscrits filtrés par plateforme : {}",
        "choose_platform_filter": "Sélectionnez une plateforme pour filtrer les utilisateurs :"
    },
    "it": {
        "choose_language": "Per favore scegli la tua lingua:",
        "register_username": "Inserisci il tuo nome utente:",
        "choose_platform": "Scegli la tua piattaforma:",""
        "thank_you": "Grazie, {}! Ora seleziona un gioco per trovare compagni di squadra.",
        "choose_game": "Scegli un gioco:",
        "teammates_found": "Compagni di squadra trovati:\n{}",
        "no_teammates": "Nessun compagno di squadra trovato al momento.",
        "language_selected": "Lingua selezionata: {}. Registrati con /register.",
        "platform_selected": "Piattaforma selezionata: {}.",
        "view_users": "Utenti registrati filtrati per piattaforma: {}",
        "choose_platform_filter": "Seleziona una piattaforma per filtrare gli utenti:"
    },
    "es": {
        "choose_language": "Por favor, elige tu idioma:",
        "register_username": "Por favor, ingresa tu nombre de usuario:",
        "choose_platform": "Por favor, elige tu plataforma:",
        "thank_you": "Gracias, {}! Ahora selecciona un juego para encontrar compañeros de equipo.",
        "choose_game": "Elige un juego:",
        "teammates_found": "Compañeros encontrados:\n{}",
        "no_teammates": "No se encontraron compañeros en este momento.",
        "language_selected": "Idioma seleccionado: {}. Regístrate con /register.",
        "platform_selected": "Plataforma seleccionada: {}.",
        "view_users": "Usuarios registrados filtrados por plataforma: {}",
        "choose_platform_filter": "Selecciona una plataforma para filtrar usuarios:"
    },
    "zh": {
        "choose_language": "请选择您的语言：",
        "register_username": "请输入您的用户名：",
        "choose_platform": "请选择您的平台：",
        "thank_you": "谢谢，{}！现在选择一个游戏来找到队友。",
        "choose_game": "选择一个游戏：",
        "teammates_found": "找到的队友：\n{}",
        "no_teammates": "目前没有找到队友。",
        "language_selected": "选择的语言：{}。请通过 /register 注册。",
        "platform_selected": "选择的平台：{}。",
        "view_users": "按平台筛选的已注册用户：{}",
        "choose_platform_filter": "选择一个平台来筛选用户："
    },
    "ko": {
        "choose_language": "언어를 선택해주세요:",
        "register_username": "사용자 이름을 입력해주세요:",
        "choose_platform": "플랫폼을 선택해주세요:",
        "thank_you": "{}님, 감사합니다! 이제 팀원을 찾을 게임을 선택하세요.",
        "choose_game": "게임을 선택하세요:",
        "teammates_found": "찾은 팀원:\n{}",
        "no_teammates": "현재 팀원이 없습니다.",
        "language_selected": "선택된 언어: {}. /register로 등록하세요.",
        "platform_selected": "선택된 플랫폼: {}.",
        "view_users": "플랫폼별 등록된 사용자 목록: {}",
        "choose_platform_filter": "사용자를 필터링할 플랫폼을 선택하세요:"
    },
    "pl": {
        "choose_language": "Proszę wybierz swój język:",
        "register_username": "Wpisz swoją nazwę użytkownika:",
        "choose_platform": "Wybierz swoją platformę:",
        "thank_you": "Dziękujemy, {}! Teraz wybierz grę, aby znaleźć drużynowych.",
        "choose_game": "Wybierz grę:",
        "teammates_found": "Znalezieni drużynowi:\n{}",
        "no_teammates": "Nie znaleziono drużynowych.",
        "language_selected": "Wybrany język: {}. Zarejestruj się za pomocą /register.",
        "platform_selected": "Wybrana platforma: {}.",
        "view_users": "Zarejestrowani użytkownicy filtrowani według platformy: {}",
        "choose_platform_filter": "Wybierz platformę do filtrowania użytkowników:"
    },
}

# Ігри для вибору, розсортовані за платформами
PLATFORMS_GAMES = {
    "Steam": ["CS 2", "Dota 2", "FC 25", "Valorant", "War Thunder"],
    "Epic Games": ["FC 25", "Fall Guys", "GTA V Online"],
    "Xbox": ["Battlefield 5", "Hell Let Loose", "Forza Horizon 5"]
}

# Структура для збереження інформації про користувачів
user_data = {}

# Функція для вибору мови
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton(lang, callback_data=code) for lang, code in LANGUAGES.items()]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(MESSAGES['en']['choose_language'],
                                    reply_markup=reply_markup)  # За замовчуванням англійською
    return CHOOSE_LANGUAGE


# Обробник вибору мови
async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_language_code = query.data
    context.user_data['language'] = selected_language_code
    context.user_data['messages'] = MESSAGES[selected_language_code]

    await query.edit_message_text(context.user_data['messages']['language_selected'].format(selected_language_code))

    return REGISTER


# Команда реєстрації
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(context.user_data['messages']['register_username'])
    return REGISTER


# Обробник введення імені користувача
async def register_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_username = update.message.from_user.username or "No username"
    context.user_data['username'] = user_username
    user_id = update.message.from_user.id

    await update.message.reply_text(context.user_data['messages']['thank_you'].format(user_username))

    keyboard = [[InlineKeyboardButton(platform, callback_data=platform) for platform in PLATFORMS_GAMES.keys()]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(context.user_data['messages']['choose_platform'], reply_markup=reply_markup)

    return CHOOSE_PLATFORM


# Обробник вибору платформи
async def choose_platform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    selected_platform = query.data
    context.user_data['platform'] = selected_platform

    await query.edit_message_text(context.user_data['messages']['platform_selected'].format(selected_platform))

    keyboard = [[InlineKeyboardButton(game, callback_data=game) for game in PLATFORMS_GAMES[selected_platform]]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(context.user_data['messages']['choose_game'], reply_markup=reply_markup)
    return FIND_TEAMMATES


# Обробник пошуку тімейтів
async def find_teammates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    selected_game = query.data
    username = context.user_data.get('username', 'Unknown')
    platform = context.user_data.get('platform', 'Unknown')

    context.user_data['game'] = selected_game

    user_data[query.from_user.id] = {
        'username': username,
        'platform': platform,
        'game': selected_game
    }

    await query.edit_message_text(f"{username}, you are looking for teammates in {selected_game} on {platform}!")

    teammates = [user for user in user_data.values() if
                 user.get('game') == selected_game and user.get('platform') == platform and user[
                     'username'] != username]

    if teammates:
        teammates_list = "\n".join([f"@{user['username']} - {user['game']}" for user in teammates])
        await query.message.reply_text(context.user_data['messages']['teammates_found'].format(teammates_list))
    else:
        await query.message.reply_text(context.user_data['messages']['no_teammates'])

    return ConversationHandler.END


# Обробник перегляду зареєстрованих користувачів
async def find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 1:
        platform_filter = context.args[0]
        users_list = "\n".join([f"@{user['username']} - {user['game']}" for user in user_data.values() if
                                user['platform'].lower() == platform_filter.lower()])
        await update.message.reply_text(f"Registered users for {platform_filter}:\n{users_list}")
    else:
        await update.message.reply_text("Please specify a platform to filter by. For example, /find Steam.")


def main() -> None:
    application = Application.builder().token("7704301408:AAEfqd_jE9YKGwyW-Jm0kibRsQJtd0NCj2M").build()
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_LANGUAGE: [CallbackQueryHandler(choose_language)],
            REGISTER: [MessageHandler(filters.TEXT, register_username)],
            CHOOSE_PLATFORM: [CallbackQueryHandler(choose_platform)],
            FIND_TEAMMATES: [CallbackQueryHandler(find_teammates)],
            VIEW_USERS: [CommandHandler("find", find)],
        },
        fallbacks=[],
    )

    application.add_handler(conversation_handler)
    application.run_polling()


# Запуск програми
if __name__ == '__main__':
    main()