import coloredlogs
import requests
import telebot
from configs import config
from entity import ExratesRates, User
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    insert,
    select,
)


coloredlogs.install()

bot = telebot.TeleBot(config.TELEBOT_TOKEN)
log = coloredlogs.logging

engine = create_engine(url=config.DB_URL)
session = engine.connect()
metadata = MetaData()


def log_user(message):
    users = Table(
        'users',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer),
        Column('first_name', String),
        Column('last_name', String),
        Column('html_text', String),
        Column('date', String),
        extend_existing=True,
    )
    metadata.create_all(session)

    insert_log = insert(users).values(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        html_text=message.html_text,
        date=message.date,
    )
    session.execute(insert_log)
    stmt = select("*").select_from(users)
    results = session.execute(stmt).fetchall()

    session.commit()
    for result in results:
        log.info(result)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Please, enter you currency like => USD, EUR, ...")


@bot.message_handler(func=lambda message: True)
def current_exrates_rates(message) -> telebot.types.Message:
    log_user(message)
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
