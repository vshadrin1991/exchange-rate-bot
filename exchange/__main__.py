import requests
import telebot

from .configs import config, localization
from .entities import ExratesRates, User
from .logger import Log
from .modules import DBConnector, DBUser, DBUserLog


log = Log()
local = localization.RUS
bot = telebot.TeleBot(config.TELEBOT_TOKEN, parse_mode=None)
session = DBConnector().get_connection()
user_db_log = DBUserLog()
user_db = DBUser()


@bot.message_handler(commands=['start'])
def on_start(message: telebot.types.Message):
    bot.reply_to(message, local['start'])


@bot.message_handler(commands=['help', 'list'])
def on_help(message: telebot.types.Message):
    try:
        response = requests.get(
            f'{config.EXCHANGE_API}/exrates/rates', params={'periodicity': 0}
        )
    except requests.ConnectionError:
        bot.reply_to(message, local['errors']['system'])
    else:
        rates: list[ExratesRates] = [ExratesRates(**rate) for rate in response.json()]
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
            chat_id=message.chat.id, text=local['select_country'], reply_markup=keyboard
        )


@bot.callback_query_handler(func=lambda message: True)
@bot.message_handler(func=lambda message: True)
def current_exrates_rates(message) -> telebot.types.Message:
    if isinstance(message, telebot.types.Message):
        message_handler: telebot.types.Message = message
        user = User(
            user_id=message_handler.from_user.id,
            first_name=message_handler.from_user.first_name,
            last_name=message_handler.from_user.last_name,
            html_text=message_handler.html_text,
            date=message_handler.date,
            chat_id=message_handler.chat.id,
        )
    else:
        callback_handler: telebot.types.CallbackQuery = message
        user = User(
            user_id=callback_handler.from_user.id,
            first_name=callback_handler.from_user.first_name,
            last_name=callback_handler.from_user.last_name,
            html_text=callback_handler.data,
            date=callback_handler.message.date,
            chat_id=callback_handler.message.chat.id,
        )
    log.info('Insert user data to DB...')
    user_db_log.insert(user)
    user_db.insert(user)
    try:
        response = requests.get(
            f'{config.EXCHANGE_API}/exrates/rates', params={'periodicity': 0}
        )
    except requests.ConnectionError:
        return bot.send_message(chat_id=user.chat_id, text=local['errors']['system'])
    else:
        if response.status_code != 200:
            return bot.send_message(
                chat_id=user.chat_id, text=local['errors']['system']
            )
        rates: list[ExratesRates] = [
            rate
            for rate in [ExratesRates(**rate) for rate in response.json()]
            if rate.Cur_Abbreviation == str(user.html_text).upper()
        ]
        return (
            bot.send_message(
                chat_id=user.chat_id,
                text=local['rate'].format(
                    rates[0].Cur_Name, rates[0].Cur_Scale, rates[0].Cur_OfficialRate
                ),
            )
            if len(rates) == 1
            else bot.send_message(
                chat_id=user.chat_id,
                text=local['errors']['not_found'].format(user.html_text),
            )
        )


bot.infinity_polling()
