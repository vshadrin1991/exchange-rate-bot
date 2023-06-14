import coloredlogs
import requests
import telebot

import configs.config as env_data
from entity.exrates_rates import ExratesRates
from entity.user import User


coloredlogs.install()

bot = telebot.TeleBot(env_data.TELEBOT_TOKEN)
log = coloredlogs.logging


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Please, enter you currency like => USD, EUR, ...")


@bot.message_handler(func=lambda message: True)
def current_exrates_rates(message) -> telebot.types.Message:
    log.info(
        User(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            html_text=message.html_text,
            date=message.date,
        )
    )
    try:
        response = requests.get(
            f'{env_data.EXCHANGE_API}/exrates/rates', params={'periodicity': 0}
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
