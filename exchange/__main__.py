import requests
import telebot
from sqlalchemy.exc import OperationalError

from .configs import config
from .entities import CurrencyRate, User
from .localizations import Localization
from .logger import Log
from .models import DBConnector, DBUser, DBUserLog


log = Log()
localization = Localization()
db_connection = DBConnector()
bot = telebot.TeleBot(config.TELEBOT_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def on_start(message: telebot.types.Message):
    bot.reply_to(message, localization.local['start'])


@bot.message_handler(commands=['help', 'list'])
def on_help(message: telebot.types.Message):
    try:
        response = requests.get(
            f'{config.EXCHANGE_API}/exrates/rates', params={'periodicity': 0}
        )
    except requests.ConnectionError:
        bot.reply_to(message, localization.local['errors']['system'])
    else:
        rates: list[CurrencyRate] = [CurrencyRate(**rate) for rate in response.json()]
        buttons = [
            [
                telebot.types.InlineKeyboardButton(
                    text=rate.Cur_Name, callback_data=rate.Cur_Abbreviation
                )
            ]
            for rate in rates
        ]
        keyboard = telebot.types.InlineKeyboardMarkup(buttons)
        bot.send_message(
            chat_id=message.chat.id,
            text=localization.local['select_country'],
            reply_markup=keyboard,
        )


@bot.callback_query_handler(func=lambda message: True)
def callback_query_exrates_rates(message: telebot.types.CallbackQuery):
    user = User(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        message=message.data,
        date=message.message.date,
        chat_id=message.message.chat.id,
    )
    exrates_rates(user)


@bot.message_handler(func=lambda message: True)
def message_handler_exrates_rates(message: telebot.types.Message):
    user = User(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        message=message.html_text,
        date=message.date,
        chat_id=message.chat.id,
    )
    exrates_rates(user)


def exrates_rates(user: User):
    try:
        log.info('insert user data to DB...')
        DBUserLog(db_connection).insert(user)
        DBUser(db_connection).insert(user)
    except OperationalError as err:
        log.error(err)
        bot.send_message(
            chat_id=user.chat_id, text=localization.local['errors']['system']
        )
        return
    try:
        response = requests.get(
            f'{config.EXCHANGE_API}/exrates/rates', params={'periodicity': 0}
        )
    except requests.ConnectionError as err:
        log.error(err)
        bot.send_message(
            chat_id=user.chat_id, text=localization.local['errors']['system']
        )
        return
    if response.status_code != 200:
        bot.send_message(
            chat_id=user.chat_id, text=localization.local['errors']['system']
        )
        return
    rates: list[CurrencyRate] = [
        rate
        for rate in [CurrencyRate(**rate) for rate in response.json()]
        if rate.Cur_Abbreviation == str(user.message).upper()
    ]
    if len(rates) != 1:
        bot.send_message(
            chat_id=user.chat_id,
            text=localization.local['errors']['not_found'].format(user.message),
        )
        return
    bot.send_message(
        chat_id=user.chat_id,
        text=localization.local['rate'].format(
            rates[0].Cur_Name, rates[0].Cur_Scale, rates[0].Cur_OfficialRate
        ),
    )


bot.infinity_polling()
