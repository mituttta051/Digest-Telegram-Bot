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
        "✅Approve": "✅Подтверить",
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
      -  Бот автоматически создаст подборку постов выбранного периода. Вы можете изменить генерированный текст до публикации.""",
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
      -  The bot will automatically create and send a summary of posts for the selected period. You can change or confirm the generated text before publishing."""
    }
}


def localis(text, lang='en'):
    return translations.get(lang, translations["en"]).get(text, text)


async def localise(text, state):
    return localis(text, await get_bot_language(state))
