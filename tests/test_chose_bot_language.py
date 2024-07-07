from content.handlers.settings_handlers import chose_bot_language
import unittest

class TestChoseBotLanguage(unittest.TestCase):

    @unittest.mock.patch('content.handlers.settings_handlers.get_bot_language')
    @unittest.mock.patch('content.handlers.settings_handlers.update_bot_language')
    @unittest.mock.patch('content.handlers.settings_handlers.localise')
    @unittest.mock.patch('content.handlers.settings_handlers.sk.settings_inline_keyboard')
    @unittest.mock.patch('content.handlers.settings_handlers.bot_settings')
    async def test_successfully_change_bot_language(self, mock_bot_settings, mock_settings_inline_keyboard, mock_localise, mock_update_bot_language, mock_get_bot_language):
        state = unittest.mock.AsyncMock()
        callback = unittest.mock.AsyncMock()
        callback.data = 'en'
        callback.message.edit_text = unittest.mock.AsyncMock()
        callback.answer = unittest.mock.AsyncMock()
        mock_get_bot_language.return_value = 'fr'
        mock_localise.return_value = 'Choose language'
        await chose_bot_language(callback, state)
        state.update_data.assert_called_with(selected_bot_language='en')
        mock_update_bot_language.assert_called_with(None, 'en')
        callback.message.edit_text.assert_called_with('Choose language', reply_markup=mock_settings_inline_keyboard.return_value)
        callback.answer.assert_called_with('You chose en')
        mock_bot_settings.assert_called_with(callback.message, state)

    @unittest.mock.patch('content.handlers.settings_handlers.get_bot_language')
    @unittest.mock.patch('content.handlers.settings_handlers.update_bot_language')
    async def test_update_bot_language_in_database(self, mock_update_bot_language, mock_get_bot_language):
        state = unittest.mock.AsyncMock()
        callback = unittest.mock.AsyncMock()
        callback.data = 'es'
        mock_get_bot_language.return_value = 'en'
        await chose_bot_language(callback, state)
        state.update_data.assert_called_with(selected_bot_language='es')
        mock_update_bot_language.assert_called_with(None, 'es')

    @unittest.mock.patch('content.handlers.settings_handlers.get_bot_language')
    @unittest.mock.patch('content.handlers.settings_handlers.localise')
    @unittest.mock.patch('content.handlers.settings_handlers.bot_settings')
    async def test_same_selected_language(self, mock_bot_settings, mock_localise, mock_get_bot_language):
        state = unittest.mock.AsyncMock()
        callback = unittest.mock.AsyncMock()
        callback.data = 'en'
        callback.answer = unittest.mock.AsyncMock()
        mock_get_bot_language.return_value = 'en'
        await chose_bot_language(callback, state)
        state.update_data.assert_called_with(selected_bot_language='en')
        callback.answer.assert_called_with('You chose en')
        mock_bot_settings.assert_called_with(callback.message, state)

    @unittest.mock.patch('content.handlers.settings_handlers.get_bot_language')
    async def test_invalid_callback_data(self, mock_get_bot_language):
        state = unittest.mock.AsyncMock()
        callback = unittest.mock.AsyncMock()
        callback.data = ''
        await chose_bot_language(callback, state)
        state.update_data.assert_not_called()

    @unittest.mock.patch('content.handlers.settings_handlers.get_bot_language')
    @unittest.mock.patch('content.handlers.settings_handlers.update_bot_language')
    async def test_user_id_none(self, mock_update_bot_language, mock_get_bot_language):
        state = unittest.mock.AsyncMock()
        callback = unittest.mock.AsyncMock()
        callback.data = 'de'
        mock_get_bot_language.return_value = 'en'
        await chose_bot_language(callback, state)
        state.update_data.assert_called_with(selected_bot_language='de')
        mock_update_bot_language.assert_called_with(None, 'de')
