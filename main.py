from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
import logging

# Стани для ConversationHandler
(
    CHOOSING, SEEKING_COMPANION, CAR_OWNER, EVACUATION, PERSON_COUNT, DEPARTURE, DESTINATION, TRAVEL_DATE, COMMENT, PHONE_NUMBER, TELEGRAM_ID, PERSON_COUNT_EVACUATION, NAMES_EVACUATION, DEPARTURE_EVACUATION, COMMENT_EVACUATION, PHONE_NUMBER_EVACUATION, TELEGRAM_ID_EVACUATION
) = range(17)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainCommands:
    @staticmethod
    def start(update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            '👋 Привіт! Я чат бот для створення постів для пошуку попутників в Україні. 🔍🚌\n\n'
            '🚨Також наш бот допомагає створювати пости для пошуку волонтерів для евакуації людей з окупованих та прикордонних територій.📢🚑\n\n'
            'Шукаєш попутників? Чи маєш декілька вільних місць у салоні? 🧳🚙 Або можливо потребуєш допомоги в евакуації? 🚨\n'
            'Створи свій пост про це у наш Телеграм канал прямо зараз! \n\n Натисніть /choose для вибору опцій. 🔍✨'
        )
        return ConversationHandler.END

    @staticmethod
    def choose(update: Update, context: CallbackContext) -> int:
        keyboard = [
            [InlineKeyboardButton("🔍ШУКАЮ ПОПУТНИКА🚗", callback_data='option_1')],
            [InlineKeyboardButton("🔍ВІЗЬМУ ПОПУТНИКА. Я ВЛАСНИК АВТО🚗", callback_data='option_2')],
            [InlineKeyboardButton("🚨ПОТРІБНО ЕВАКУЮВАТИСЯ. Терміново!📢", callback_data='option_3')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Яка ситуація відноситься до тебе? Будь ласка, оберіть опцію:', reply_markup=reply_markup)
        return CHOOSING

    @staticmethod
    def button(update: Update, context: CallbackContext) -> int:
        query = update.callback_query
        query.answer()

        follow_up_map = {
            'option_1': SEEKING_COMPANION,
            'option_2': CAR_OWNER,
            'option_3': EVACUATION
        }

        state = follow_up_map.get(query.data)
        if state is not None:
            query.message.reply_text(
                'Ви впевнені що ви хочете створити пост? 🤔\n\n'
                'Введіть БУДЬ-ЩО для підтвердження. НАПРИКЛАД: 1. ✅ \n'
                'Якщо хочете відмінити створення посту, натисніть - /cancel ❌'
            )
            return state
        return CHOOSING

    @staticmethod
    def cancel(update: Update, context: CallbackContext) -> int:
        update.message.reply_text(
            '... \n\n'
            'Щоб відразу повернутися у головне МЕНЮ - натисніть /choose 🔄\n'
            'Щоб почати бот з самого початку - натисніть /start 🚀'
        )
        return ConversationHandler.END

class CompanionSearch:
    @staticmethod
    def seeking_companion(update: Update, context: CallbackContext) -> int:
        context.user_data['choice'] = '🔍ШУКАЮ ПОПУТНИКА🚗'
        update.message.reply_text(
            "Добре!✨Я тобі допоможу створити пост про пошук попутника.🚗\n\n"
            "❗️❗️❗️Усі пости перевіряються, тому заповнюйте лише у правильній формі. Якщо форма заповнення буде хибною - пост буде видалено❗️❗️❗️\n\n"
            "👩‍👦 Скільки їде осіб? 👨‍👩‍👧‍👦👨‍👦",
            reply_markup=ReplyKeyboardMarkup([[str(i)] for i in range(1, 11)], one_time_keyboard=True)
        )
        return PERSON_COUNT

    @staticmethod
    def car_owner(update: Update, context: CallbackContext) -> int:
        context.user_data['choice'] = '🔍ВІЗЬМУ ПОПУТНИКА. Я ВЛАСНИК АВТО🚗'
        update.message.reply_text(
            "Добре! Я тобі допоможу створити пост про пошук попутника для власників авто.\n\n"
            "!!Усі пости перевіряються, тому заповнюйте лише у правильній формі. Якщо форма заповнення буде хибною - пост буде видалено!!!\n\n"
            "Скільки можете взяти осіб до себе в авто?",
            reply_markup=ReplyKeyboardMarkup([[str(i)] for i in range(1, 11)], one_time_keyboard=True)
        )
        return PERSON_COUNT

    @staticmethod
    def person_count(update: Update, context: CallbackContext) -> int:
        context.user_data['person_count'] = update.message.text
        update.message.reply_text(
            "Звідки їдете?🏬\n\n Зазначте бажане місце відправлення у форматі: Київ, Вокзальна 4 🏫\n"
            "Якщо це село/смт - додайте область, у форматі: Київська область, Калинівка 🏡\n\n"
            "Ваша адреса:"
            )
        return DEPARTURE

    @staticmethod
    def departure(update: Update, context: CallbackContext) -> int:
        context.user_data['departure'] = update.message.text
        update.message.reply_text(
            "Куди їдете?🚘\n\n Зазначте бажане місце прибуття у форматі: Львів, Центр 🏦\n"
            "Якщо це село/смт - додайте область, у форматі: Київська область, Калинівка 🏡\n\n"
            "Ваша відповідь:"
        )
        return DESTINATION

    @staticmethod
    def destination(update: Update, context: CallbackContext) -> int:
        context.user_data['destination'] = update.message.text
        update.message.reply_text("Бажана дата поїздки?📅\n\n Зазначте бажану дату поїздки у форматі: 30.09.2023")
        return TRAVEL_DATE

    @staticmethod
    def travel_date(update: Update, context: CallbackContext) -> int:
        context.user_data['travel_date'] = update.message.text
        update.message.reply_text(
            "Надайте коментар до вашого посту, який будуть бачити інші користувачі чат-боту. 💬\n\n"
            "Тут ви можете вказати марку машини, грошову винагороду, алергію на тварин тощо.💸🐕👩‍👧\n\n"
            "Коментар:"
        )
        return COMMENT

    @staticmethod
    def comment(update: Update, context: CallbackContext) -> int:
        context.user_data['comment'] = update.message.text
        update.message.reply_text(
            "☎️Надайе ваш номер телефону за яким з вами можна буде зв'язатись:",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("Надати номер телефону📲", request_contact=True)]],
                one_time_keyboard=True
            )
        )
        return PHONE_NUMBER

    @staticmethod
    def phone_number(update: Update, context: CallbackContext) -> int:
        contact = update.message.contact
        if contact:
            context.user_data['phone_number'] = contact.phone_number
        else:
            context.user_data['phone_number'] = update.message.text
        
        update.message.reply_text("📱Надайе ваш Telegram ID, щоб попутники мали змогу зв'язатися з вами. У форматі: @vashe_id\nМоє Telegram ID:")
        return TELEGRAM_ID

    @staticmethod
    def telegram_id(update: Update, context: CallbackContext) -> int:
        context.user_data['telegram_id'] = update.message.text
        user_data = context.user_data
        post = (
            f"{user_data.get('choice', 'Невідомо')}\n"
            f"👥 Кількість осіб: {user_data.get('person_count', 'Невідомо')}\n"
            f"📍 Звідки: {user_data.get('departure', 'Невідомо')}\n"
            f"🏁 Куди: {user_data.get('destination', 'Невідомо')}\n"
            f"📅 Дата: {user_data.get('travel_date', 'Невідомо')}\n"
            f"💬 Коментар: {user_data.get('comment', 'Немає коментаря')}\n"
            f"☎️ Номер телефону: {user_data.get('phone_number', 'Невідомо')}\n"
            f"📱 Telegram ID: {user_data.get('telegram_id', 'Невідомо')}"
        )
        update.message.reply_text("Ваш пост успішно створено  та надіслано на головний канал 'https://t.me/poputnyky_ukraine' для пошуку попутників:\n\n" + post)
        # Відправка посту в загальний чат
        chat_id = '-1002009177529'
        context.bot.send_message(chat_id=chat_id, text=post)
        # Завершення
        update.message.reply_text(
            '... \n\n'
            'Щоб відразу повернутися у головне МЕНЮ - натисніть /choose \n'
            'Щоб почати бот з самого початку - натисніть /start'
        )
        return ConversationHandler.END

class EvacuationHelp:
    @staticmethod
    def evacuation(update: Update, context: CallbackContext) -> int:
        context.user_data['choice'] = '🚨ПОТРІБНО ЕВАКУЮВАТИСЯ📢'
        update.message.reply_text(
            "Добре!✨ Я тобі допоможу створити пост про пошук допомоги в евакуації: виїзду з окупованих місць та прикордонних територій з воєнними діями.🙏🚨\n\n"
            "Данний пост буде розісланий у певні волонтерські організації які займаються евакуацією людей з окупованих та прикордонних територій.🚑\n\n"
            "❗️❗️❗️Всі пости перевіряються на брехню! Пости заповнювати лише у правильній формі - або пост буде видалено❗️❗️❗️\n\n"
            "👩‍👦Скільки осіб потрібно евакуювати?👨‍👩‍👧‍👦👨‍👦",
            reply_markup=ReplyKeyboardMarkup([[str(i)] for i in range(1, 11)], one_time_keyboard=True)
        )
        return PERSON_COUNT_EVACUATION

    @staticmethod
    def person_count_evacuation(update: Update, context: CallbackContext) -> int:
        context.user_data['person_count_evacuation'] = update.message.text
        update.message.reply_text("👨‍👩‍👧 Як звати всіх людей, яким потрібно надати допомогу в евакуації? Скільки їм роів?\n\n Надайте повний список. (ПРИЗВІЩЕ ІМ'Я вік)")
        return NAMES_EVACUATION

    @staticmethod
    def names_evacuation(update: Update, context: CallbackContext) -> int:
        context.user_data['names_evacuation'] = update.message.text
        update.message.reply_text(
            "🏢Звідки вам потрібно евакуюватися?🏥\n\n Зазначте повний адрес у форматі: Київ, вул. Мечникова 17 кв. 5\n"
            "🏡Якщо це село/смт - додайте область, у форматі: Київська область, Калинівка\n\n"
            "Ваша адреса: "
        )
        return DEPARTURE_EVACUATION

    @staticmethod
    def departure_evacuation(update: Update, context: CallbackContext) -> int:
        context.user_data['departure_evacuation'] = update.message.text
        update.message.reply_text(
            "💬Надайте коментар до вашого посту.\n\n Вкажіть, наприклад, інформацію про наявність людей з інвалідністю, важко поранених людей, домашніх тварин та будь-яку іншу інформацію, яку вважаєте ВАЖЛИВОЮ для вашого подальшого евакуювання.🚨👨🏻‍🦽🤰🏼👨‍👧‍👦\n\n"
            "Ваш коментар:"
        )
        return COMMENT_EVACUATION

    @staticmethod
    def comment_evacuation(update: Update, context: CallbackContext) -> int:
        context.user_data['comment_evacuation'] = update.message.text
        update.message.reply_text(
            "☎️Надайе ваш номер телефону за яким з вами можна буде зв'язатись:",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("Надати номер телефону📲", request_contact=True)]],
                one_time_keyboard=True
            )
        )
        return PHONE_NUMBER_EVACUATION

    @staticmethod
    def phone_number_evacuation(update: Update, context: CallbackContext) -> int:
        contact = update.message.contact
        if contact:
            context.user_data['phone_number_evacuation'] = contact.phone_number
        else:
            context.user_data['phone_number_evacuation'] = update.message.text

        update.message.reply_text("📱Надайе ваш Telegram ID, щоб волонтери мали змогу зв'язатися з вами. У форматі: @vashe_id\nМоє Telegram ID:")
        return TELEGRAM_ID_EVACUATION

    @staticmethod
    def telegram_id_evacuation(update: Update, context: CallbackContext) -> int:
        context.user_data['telegram_id_evacuation'] = update.message.text
        user_data = context.user_data
        post1 = (
            f"{user_data.get('choice', 'Невідомо')}\n"
            f"👨‍👩‍👦‍👦 Кількість осіб: {user_data.get('person_count_evacuation', 'Невідомо')}\n"
            f"👥 Ім'я людей: {user_data.get('names_evacuation', 'Невідомо')}\n"
            f"📍 Звідки: {user_data.get('departure_evacuation', 'Невідомо')}\n"
            f"💬 Коментар: {user_data.get('comment_evacuation', 'Немає коментаря')}\n"
            f"📱 Номер телефону: {user_data.get('phone_number_evacuation', 'Невідомо')}\n"
            f"📱 Telegram ID: {user_data.get('telegram_id_evacuation', 'Невідомо')}"
        )
        update.message.reply_text("Ваш пост на евакуацію успішно створено:\n\n" + post1)
        update.message.reply_text("🙏Ваш пост надіслано на головний канал 'https://t.me/poputnyky_ukraine' для людей які потребують допомоги в евакуації, та надіслано в інші організації та волонтерам, що займаються евакуацією. Чекайте, поки з вами зв'яжуться по номеру телефону. Якщо ми не зможемо до вас додзвонитися - напишемо вам у Телеграм.📢\n\n")
        # Відправка посту в загальний чат та інши волонтерам які займаються допомогою в евакуації
        # Тут можуть бути айді інших волонтерів, яким можуть надсилатися пости від людей які потребують допомогу. Можна додати й інші групи для публікації постів про пошук допомоги.
        chat_id = '-1002009177529'
        context.bot.send_message(chat_id=chat_id, text=post1)
        # Завершення
        update.message.reply_text(
            '... \n\n'
            'Щоб відразу повернутися у головне МЕНЮ - натисніть /choose\n'
            'Щоб почати бот з самого початку - натисніть /start'
        )
        return ConversationHandler.END

class Bot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.add_handlers()

    def add_handlers(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', MainCommands.start), CommandHandler('choose', MainCommands.choose)],
            states={
                CHOOSING: [CallbackQueryHandler(MainCommands.button)],
                SEEKING_COMPANION: [MessageHandler(Filters.text & ~Filters.command, CompanionSearch.seeking_companion)],
                CAR_OWNER: [MessageHandler(Filters.text & ~Filters.command, CompanionSearch.car_owner)],
                EVACUATION: [MessageHandler(Filters.text & ~Filters.command, EvacuationHelp.evacuation)],
                PERSON_COUNT: [MessageHandler(Filters.regex('^\d+$'), CompanionSearch.person_count)],
                DEPARTURE: [MessageHandler(Filters.text & ~Filters.command, CompanionSearch.departure)],
                DESTINATION: [MessageHandler(Filters.text & ~Filters.command, CompanionSearch.destination)],
                TRAVEL_DATE: [MessageHandler(Filters.text & ~Filters.command, CompanionSearch.travel_date)],
                COMMENT: [MessageHandler(Filters.text & ~Filters.command, CompanionSearch.comment)],
                PHONE_NUMBER: [MessageHandler(Filters.contact | (Filters.text & ~Filters.command), CompanionSearch.phone_number)],
                TELEGRAM_ID: [MessageHandler(Filters.text & ~Filters.command, CompanionSearch.telegram_id)],
                PERSON_COUNT_EVACUATION: [MessageHandler(Filters.regex('^\d+$'), EvacuationHelp.person_count_evacuation)],
                NAMES_EVACUATION: [MessageHandler(Filters.text & ~Filters.command, EvacuationHelp.names_evacuation)],
                DEPARTURE_EVACUATION: [MessageHandler(Filters.text & ~Filters.command, EvacuationHelp.departure_evacuation)],
                COMMENT_EVACUATION: [MessageHandler(Filters.text & ~Filters.command, EvacuationHelp.comment_evacuation)],
                PHONE_NUMBER_EVACUATION: [MessageHandler(Filters.contact | (Filters.text & ~Filters.command), EvacuationHelp.phone_number_evacuation)],
                TELEGRAM_ID_EVACUATION: [MessageHandler(Filters.text & ~Filters.command, EvacuationHelp.telegram_id_evacuation)]
            },
            fallbacks=[CommandHandler('cancel', MainCommands.cancel)]
        )
        self.dispatcher.add_handler(conv_handler)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    bot = Bot("6843435565:AAGQ4dm9xaPsTd3eDo2ZtT7tRr8kPauZ99A")
    bot.start()
