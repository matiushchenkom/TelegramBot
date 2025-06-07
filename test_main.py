import unittest
from unittest.mock import MagicMock
from telegram import Update, Message, CallbackQuery, User, Contact
from telegram.ext import CallbackContext

# Імпортуємо необхідні класи та константи з основного файлу бота
from main import MainCommands, CompanionSearch, CHOOSING, PERSON_COUNT, SEEKING_COMPANION, DEPARTURE, TELEGRAM_ID

# Клас для тестування функцій Telegram-бота
class TestTelegramBot(unittest.TestCase):
    def setUp(self):
        # Створюємо мок-об'єкти для Update та CallbackContext
        self.update = MagicMock(spec=Update)
        self.context = MagicMock(spec=CallbackContext)

        # Мокуємо повідомлення та callback-запит
        self.message = MagicMock(spec=Message)
        self.callback_query = MagicMock(spec=CallbackQuery)

        self.update.message = self.message
        self.update.callback_query = self.callback_query

        # Мокуємо користувача Telegram
        self.user = MagicMock(spec=User)
        self.user.id = 123456
        self.update.effective_user = self.user

    # Тест команди /start
    def test_start_command(self):
        self.message.reply_text = MagicMock()
        result = MainCommands.start(self.update, self.context)
        self.message.reply_text.assert_called_once()
        self.assertEqual(result, -1)  # ConversationHandler.END == -1

    # Тест вибору ролі користувача
    def test_choose_command(self):
        self.message.reply_text = MagicMock()
        result = MainCommands.choose(self.update, self.context)
        self.message.reply_text.assert_called_once()
        self.assertEqual(result, CHOOSING)

    # Тест натискання кнопки "🔍ШУКАЮ ПОПУТНИКА🚗"
    def test_button_option_1(self):
        self.callback_query.data = 'option_1'
        self.callback_query.answer = MagicMock()
        self.callback_query.message.reply_text = MagicMock()

        result = MainCommands.button(self.update, self.context)

        self.callback_query.answer.assert_called_once()
        self.callback_query.message.reply_text.assert_called_once()
        self.assertEqual(result, SEEKING_COMPANION)

    # Тест переходу до запиту кількості попутників
    def test_seeking_companion(self):
        self.message.reply_text = MagicMock()
        self.context.user_data = {}

        result = CompanionSearch.seeking_companion(self.update, self.context)

        self.message.reply_text.assert_called_once()
        self.assertEqual(self.context.user_data['choice'], '🔍ШУКАЮ ПОПУТНИКА🚗')
        self.assertEqual(result, PERSON_COUNT)

    # Тест зчитування кількості попутників
    def test_person_count(self):
        self.message.text = '3'
        self.message.reply_text = MagicMock()
        self.context.user_data = {}

        result = CompanionSearch.person_count(self.update, self.context)

        self.assertEqual(self.context.user_data['person_count'], '3')
        self.message.reply_text.assert_called_once()
        self.assertEqual(result, DEPARTURE)

    # Тест введення номера телефону через контакт
    def test_phone_number_with_contact(self):
        contact = Contact(phone_number='+380123456789', user_id=123456, first_name='Test')
        self.message.contact = contact
        self.message.reply_text = MagicMock()
        self.context.user_data = {}

        result = CompanionSearch.phone_number(self.update, self.context)

        self.assertEqual(self.context.user_data['phone_number'], '+380123456789')
        self.message.reply_text.assert_called_once()
        self.assertEqual(result, TELEGRAM_ID)

    # Тест введення номера телефону текстом, без контакту
    def test_phone_number_without_contact(self):
        self.message.contact = None
        self.message.text = '+380987654321'
        self.message.reply_text = MagicMock()
        self.context.user_data = {}

        result = CompanionSearch.phone_number(self.update, self.context)

        self.assertEqual(self.context.user_data['phone_number'], '+380987654321')
        self.message.reply_text.assert_called_once()

# Запуск усіх тестів
if __name__ == '__main__':
    unittest.main()
