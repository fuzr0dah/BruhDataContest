import logging

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from ai import classify_question


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text("""
Привет!
Я могу проконсультировать тебя по любому вопросу.
Например:
- *Существуют ли обязательные реквизиты письменных пояснений?*
и т.д.
Просто спроси!
    """, parse_mode=telegram.ParseMode.MARKDOWN)


def help(update, context):
    update.message.reply_text("""
Спрашивай меня о чём хочешь.
Например:
- *Существуют ли обязательные реквизиты письменных пояснений?*
и т.д.
Просто спроси!
    """, parse_mode=telegram.ParseMode.MARKDOWN)


def echo(update, context):
    answer = classify_question(update.message.text)
    dump_data(update.message.from_user, update.message.text, answer)
    update.message.reply_text(answer)


def dump_data(user, question, answer):
    username = user.username
    full_name = user.full_name
    id = user.id

    str = """{username}\t{full_name}\t{id}\t{question}\t{answer}\n""".format(username=username,
                                                                 full_name=full_name,
                                                                 id=id,
                                                                 question=question,
                                                                 answer=answer)

    with open("dump.tsv", "a") as myfile:
        myfile.write(str)


def main():
    updater = Updater("1488387888:AAG1ObCLMPexruvr6ZpK9LGYUhQMGvQh0ZA", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()