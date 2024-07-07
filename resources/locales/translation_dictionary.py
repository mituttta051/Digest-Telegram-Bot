from content.FSMs.settings_FSMs import SettingsFSM
from utils.botUtils import get_bot_language

translations = {
    'ru': {
        "Choose a channel": "Выберите канал",
        "back": "назад",
        "Create digest": "Создать дайджест",
        "Choose a digest period": "Выберите период дайджеста",
        "Digest is preparing...": "Готовлю дайджест...",
        "Nothing has been posted since the bot was added": "Ничего не было опубликовано с добавления бота в канал",
        "Choose main language for digest": "Выберите главный язык для дайджеста",
        "Choose addition language for digest": "Выберите дополнительный язык дайджеста",
        "Welcome to the settings!": "Добро пожаловать в настройки!",
        "⬅️Back": "⬅️Назад",
        "❌Cancel editing": "❌Отмена редактирования",
        "🔄Regenerate": "🔄Регенерировать",
        "❌Cancel": "❌Отмена",
        "✏️Edit": "✏️Редактировать",
        "1 Month (30 days)": "1 Месяц (30 дней)",
        "2 weeks (14 days)": "2 недели (14 дней)",
        "Week (7 days)": "Неделя (7 дней)",
        "🌎Addition language": "🌎Дополнительный язык",
        "🌍Main language": "🌎Основной язык",
        "🌍Bot language": "🌍Язык бота",
        "⚙️Channel settings": "⚙️Настройки канала",
        "✍🏼Create digest": "✍🏼Создать дайджест",
        "⚙️Settings": "⚙️Настройки",
        "❓Help": "❓Помощь",
        'You chose channel': 'Вы выбрали канал',
        "You chose period": "Вы выбрали период",
        'You chose "✅Approve"': 'Вы выбрали "✅Подтвердить"',
        'You chose "❌Cancel"': 'Вы выбрали "❌Отмена"',
        "You chose ": "Вы выбрали ",
        "You chose the option language": "Выберите дополнительный язык",
        "You chose the main language": "Выберите основной язык дайджеста",
        "Choose one of the options": "Выберите один из вариантов",
        "Choose the main language for digest": "Выберите основной язык дайджеста",
        "Choose the addition language for digest": "Выберите дополнительный язык дайджеста",
        "🥳Digest posted successfully!": "🥳Дайджест успешно опубликован!",
        'You chose "Edit"': 'Вы выбрали "✏️Edit"',
        "Welcome":
            """
        🤖 <b>Добро пожаловать в Digest Bot!</b> Я помогу Вам суммаризировать посты в канале.

    Чтобы начать, нажмите кнопку <b>✍🏼Создать дайджест</b>.

    Для подробной информации нажмите кнопку <b>❓Помощь</b>.
        """,

        "Settings": """<b>Вы можете использовать Digest Bot следующим образом:</b>

    ⚙️ <b>Настройки</b>
      -  Изменить язык бота: Выберите язык бота для легкости использования.
      -  Настройки канала: Выберите нужный канал из списока своих каналов.

    📝 <b>Создать дайджест</b>
      -  Бот автоматически создаст подборку постов выбранного периода. Вы можете изменить сгенерированный текст до публикации.""",
        "✅Approve": "✅Подтвердить",
        "Write your own version and send it here": "Напишите и отправьте Вашу версию",
        'You return back': 'Вы возвращаетесь назад',
        "Current option": " — Текущий выбор",
        "❌Without language": "❌Без языка"
    },
    'en': {
        "Choose a channel": "Choose a channel",
        "back": "back",
        "Create digest": "Create digest",
        "Choose a digest period": "Choose a digest period",
        "Digest is preparing...": "Digest is preparing...",
        "Nothing has been posted since the bot was added": "Nothing has been posted since the bot was added",
        "Choose main language for digest": "Choose main language for digest",
        "Choose addition language for digest": "Choose addition language for digest",
        "Welcome to the settings!": "Welcome to the settings!",
        "⬅️Back": "⬅️Back",
        "❌Cancel editing": "❌Cancel editing",
        "🔄Regenerate": "🔄Regenerate",
        "❌Cancel": "❌Cancel",
        "✏️Edit": "✏️Edit",
        "✅Approve": "✅Approve",
        "1 Month (30 days)": "1 Month (30 days)",
        "2 weeks (14 days)": "2 weeks (14 days)",
        "Week (7 days)": "Week (7 days)",
        "🌎Addition language": "🌎Addition language",
        "🌍Main language": "🌍Main language",
        "⚙️Channel settings": "⚙️Channel settings",
        "🌍Bot language": "🌍Bot language",
        "✍🏼Create digest": "✍🏼Create digest",
        "⚙️Settings": "⚙️Settings",
        "❓Help": "❓Help",
        'You return back': 'You return back',
        'You chose channel': 'You chose channel',
        "You chose period": "You chose period",
        'You chose "✅Approve"': 'You chose "✅Approve"',
        "You chose ": "You chose ",
        "You chose the option language": "You chose option language",
        "You chose the main language": "You chose the main language",
        "Choose one of the options": "Choose one of the options",
        'You chose "Edit"': 'You chose "Edit"',
        "Welcome":
            """
        🤖 <b>Welcome to Digest Bot!</b> I will help you make up a summary of posts.

    To get started click <b>✍🏼Create digest</b> button.

    For more detailed information, click <b>❓Help</b> button.
        """,

        "Settings": """<b>Here's how you can use our Digest Bot:</b>

    ⚙️ <b>Settings</b>
      -  Change bot language: Select the bot interface language for ease of use.
      -  Channel settings: List of your channels that you can use for digests.

    📝 <b>Create Digest</b>
      -  The bot will automatically create and send a summary of posts for the selected period. You can change or confirm the generated text before publishing.""",
        "🥳Digest posted successfully!": "🥳Digest posted successfully!",
        "Write your own version": "Write your own version",
        'You chose "❌Cancel"': 'You chose "❌Cancel"',
        "Choose the main language for digest": "Choose the main language for digest",
        "Choose the addition language for digest": "Choose the addition language for digest",
        "Write your own version and send it here": "Write your own version and send it here",
        "Current option": " — Current option",
        "❌Without language": "❌Without language"
    },
}


def localis(text, lang='en'):
    return translations.get(lang, translations["en"]).get(text, text)


async def localise(text, state):
    return localis(text, await get_bot_language(state))
