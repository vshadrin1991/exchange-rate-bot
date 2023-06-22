import requests
import telebot

from .configs import config
from .entities import ExratesRates, User
from .logger import Log
from .modules import DBConnector, DBUserLog


log = Log()
bot = telebot.TeleBot(config.TELEBOT_TOKEN, parse_mode=None)
session = DBConnector().get_connection()
user_log = DBUserLog()


@bot.message_handler(commands=['start'])
def on_start(message: telebot.types.Message):
    bot.reply_to(
        message,
        "Hello there!\n"
        + "I can help you to know exchange rates for today according to the NBRB.\n"
        + "If you want to know about supported currencies, just use /help command"
        + "And if you know you currency, enter you currency like => USD, EUR, ...",
    )


@bot.message_handler(commands=['help'])
def on_help(message: telebot.types.Message):
    try:
        response = requests.get(
            f'{config.EXCHANGE_API}/exrates/rates', params={'periodicity': 0}
        )
    except requests.ConnectionError:
        bot.reply_to(message, "Opps... something went wrong. Please try later.")
    else:
        bot.reply_to(
            message,
            '\n'.join(
                [
                    f'{rate.Cur_Name} => {rate.Cur_Abbreviation}'
                    for rate in [ExratesRates(**rate) for rate in response.json()]
                ]
            ),
        )


@bot.message_handler(func=lambda message: True)
def current_exrates_rates(message: telebot.types.Message) -> telebot.types.Message:
    user = User(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        html_text=message.html_text,
        date=message.date,
    )
    user_log.insert(user)
    try:
        response = requests.get(
            f'{config.EXCHANGE_API}/exrates/rates', params={'periodicity': 0}
        )
    except requests.ConnectionError:
        return bot.reply_to(message, "Opps... something went wrong. Please try later.")
    else:
        if response.status_code != 200:
            return bot.reply_to(
                message, "Opps... something went wrong. Please try later."
            )
        rates: list[ExratesRates] = [
            rate
            for rate in [ExratesRates(**rate) for rate in response.json()]
            if rate.Cur_Abbreviation == str(message.html_text).upper()
        ]
        return (
            bot.reply_to(
                message,
                f'Exchange rate to the Belarusian ruble per {rates[0].Cur_Scale} units\n{rates[0].Cur_OfficialRate}',
            )
            if len(rates) == 1
            else bot.reply_to(
                message, f"Opps... i'am not found currency => {message.html_text}"
            )
        )


bot.infinity_polling()
