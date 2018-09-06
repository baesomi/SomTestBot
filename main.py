#import modules
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging


from credentials import *

from modules.naver_weather import weather
from modules.melon_rank import get_music_chart

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Global vars:
MENU, MOVIE, CURWEATHER, MUSIC = range(4)
STATE = MENU

#The Function of bot
MOVIE_CHART = "영화 순위"
TODAY_WEATHER = "오늘 날씨"
MUSIC_CHART = "실시간 음원 차트"
SEARCH_CHART = "실시간 검색어"

cash = ''


# define command handlers
def start(bot, update):
    """
        Start function. Displayed whenever the /start command is called.
        This function sets the language of the bot.
        """
    # Create buttons to slect language:
    keyboard = [[TODAY_WEATHER, MOVIE_CHART],
                [MUSIC_CHART, SEARCH_CHART]]

    # Create initial message:
    message = "소미 맘대로하는 봇입니다. 시작할 때는 /satrt 끝낼때는 /end 를 기억하세요!"

    chat_id = update.message.chat_id

    bot.sendChatAction(chat_id, "TYPING")
    update.message.reply_text(message,
                              reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return MENU


# 정해진 커맨드가 아닌 다른 명령을 받았을 때 출력할 메시지
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="뭔말인지 모르겠는데요;;")


def menu(bot, update):
    logger.info("function call menu")
    chat_id = update.message.chat_id

    if update.message.text == MOVIE:
        bot.sendChatAction(chat_id, "TYPING")
        register_text = MOVIE_CHART + "를 선택했습니다."
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        get_movie_chart(bot, update)

    elif update.message.text == TODAY_WEATHER:
        bot.sendChatAction(chat_id, "TYPING")
        register_text = TODAY_WEATHER + "를 선택했습니다.  /날씨 서울 이런식으로 물어보세여ㅎㅎ"
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        return CURWEATHER

    elif update.message.text == MUSIC_CHART:
        bot.sendChatAction(chat_id, "TYPING")
        register_text = MUSIC_CHART + "를 선택했습니다."
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        get_music_chart(bot, update);

    elif update.message.text == SEARCH_CHART:
        bot.sendChatAction(chat_id, "TYPING")
        register_text = SEARCH_CHART + "를 선택했습니다."
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        get_search_chart(bot, update)

    else:
        bot.sendChatAction(chat_id, "TYPING")
        unknown(bot, update)


def cancel(bot, update):
    """
    User cancelation function.
    Cancel conersation by user.
    """
    user = update.message.from_user
    logger.info("User {} canceled the conversation.".format(user.first_name))
    update.message.reply_text("종료합니다.",reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def get_movie_chart(bot, update):
    update.message.reply_text("영화 순위 기능")
    return ConversationHandler.END


def get_search_chart(bot, update):
    update.message.reply_text("실시간 검색어 기능")
    return ConversationHandler.END

# main문을 정의하고
def main():

    # Create Updater object and attach dispatcher to it
    updater = Updater(telegram_token)
    dp = updater.dispatcher
    print("Bot started")

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MENU: [MessageHandler(Filters.text, menu)],
            CURWEATHER: [CommandHandler("날씨", weather, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('end', cancel)]
    )

    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()
    updater.stop()


if __name__ == '__main__':
    main()