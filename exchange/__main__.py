import requests
import telebot

from .configs import config
from .entities import ExratesRates, User
from .logger import Log
from .modules import DBConnector, UserLog


log = Log()
bot = telebot.TeleBot(config.TELEBOT_TOKEN, parse_mode=None)
session = DBConnector().get_connection()
user_log = UserLog()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Please, enter you currency like => USD, EUR, ...")


@bot.message_handler(func=lambda message: True)
def current_exrates_rates(message) -> telebot.types.Message:
    user = User(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        html_text=message.html_text,
        date=message.date,
    )
    user_log.insert(user)
    log.warn(user_log.select_all())

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
