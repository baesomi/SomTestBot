#import modules
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from telegram import InlineKeyboardButton,ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
import logging


from credentials import *

from modules.naver_weather import weather
from modules.melon_rank import get_music_chart
from modules.movie_chart import get_movie_chart
from modules.search_rank import get_search_rank
from modules.restaurant_recommend import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Global vars:
MENU, MOVIE, CURWEATHER, MUSIC, RESTAURANT,SETWHERE, SETWHEN, SETHOWMANY = range(8)
STATE = MENU

#The Function of bot
MOVIE_CHART = "영화 순위"
TODAY_WEATHER = "오늘 날씨"
MUSIC_CHART = "실시간 음원 차트"
SEARCH_CHART = "실시간 검색어"
RECOMM_FOOD = "맛집 추천"

cash = ''


# define command handlers
def start(bot, update):

    # Create initial message:
    message = "소미 맘대로하는 봇입니다. 시작할 때는 /satrt 끝낼때는 /end 를 기억하세요!"

    functions = [MOVIE_CHART, TODAY_WEATHER, MUSIC_CHART, SEARCH_CHART, RECOMM_FOOD]
    function_list = []

    for func in functions:
        function_list.append(InlineKeyboardButton(func, callback_data=func))

    show_functions = InlineKeyboardMarkup(build_keyboard(function_list, (int)(len(function_list)/2)))  # make markup
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id, "TYPING")
    update.message.reply_text(message, reply_markup=show_functions)

    return MENU


# 정해진 커맨드가 아닌 다른 명령을 받았을 때 출력할 메시지
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="뭔말인지 모르겠는데요;;")


def menu(bot, update):
    logger.info("function call menu")
    chat_id = update.callback_query.message.chat_id

    if update.callback_query.data == MOVIE_CHART:
        bot.sendChatAction(chat_id, "TYPING")
        register_text = MOVIE_CHART + "를 선택했습니다."
        update.message.reply_text(register_text)
        get_movie_chart(bot, update)

    elif update.callback_query.data == TODAY_WEATHER:
        bot.sendChatAction(chat_id, "TYPING")
        register_text = TODAY_WEATHER + "를 선택했습니다. 원하는 지역을 선택하세요."
        areas = ["서울", "성남", "수원", "용인", "제주", "독도", "이전"]
        area_list = []

        for area in areas:
            area_list.append(InlineKeyboardButton(area, callback_data=area))

        show_areas = InlineKeyboardMarkup(
            build_keyboard(area_list, (int)(len(area_list)/3)))  # make markup

        bot.sendChatAction(chat_id, "TYPING")
        update.callback_query.message.reply_text(register_text, reply_markup=show_areas)
        return CURWEATHER

    elif update.callback_query.data == MUSIC_CHART:
        bot.sendChatAction(chat_id, "TYPING")
        register_text = MUSIC_CHART + "를 선택했습니다."
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        get_music_chart(bot, update)

    elif update.callback_query.data == SEARCH_CHART:
        bot.sendChatAction(chat_id, "TYPING")
        register_text = SEARCH_CHART + "를 선택했습니다."
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        get_search_rank(bot, update)

    elif update.callback_query.data == RECOMM_FOOD:
        bot.sendChatAction(chat_id, "TYPING")
        register_text = RECOMM_FOOD + "를 선택했습니다. 지역을 선택하세요."
        where = ["강남", "판교", "서현", "서초", "야탑", "정자"]
        where_list = []

        for item in where:
            where_list.append(InlineKeyboardButton(item, callback_data=item))

        show_where = InlineKeyboardMarkup(
            build_keyboard(where_list, (int)(len(where_list) / 3)))  # make markup

        # 검색어 초기화
        search_keyword = []
        # 지역선택
        bot.sendChatAction(chat_id, "TYPING")
        update.callback_query.message.reply_text(register_text, reply_markup=show_where)
        search_keyword.append(SETWHERE)

        # 시간대 선택
        bot.sendChatAction(chat_id, "TYPING")
        when = ["점심", "저녁", "밤"]
        when_list = []

        for item in when:
            when_list.append(InlineKeyboardButton(item, callback_data=item))

        show_when = InlineKeyboardMarkup(
            build_keyboard(when_list, (int)(len(when_list) / 3)))  # make markup

        update.callback_query.message.reply_text("시간대를 선택하세요", reply_markup=show_when)
        search_keyword.append(SETWHEN)

        # 유형 선택
        bot.sendChatAction(chat_id, "TYPING")
        howmany = ["혼밥", "회식"]
        howmany_list = []

        for item in howmany:
            howmany_list.append(InlineKeyboardButton(item, callback_data=item))

        show_where = InlineKeyboardMarkup(build_keyboard(howmany_list, (int)(len(howmany_list) / 2)))  # make markup
        update.message.callback_query.reply_text("식사 유형을 선택하세요", reply_markup=show_where)
        search_keyword.append(SETHOWMANY)
        print(search_keyword)

        return RESTAURANT

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


# 개수에 따라서 메뉴 template 생성해주는 함수
def build_keyboard(buttons, n_cols, header_buttons=None, footer_buttons=None):
    keyboard = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        keyboard.insert(0, header_buttons)
    if footer_buttons:
        keyboard.append(footer_buttons)
    return keyboard


# main문을 정의하고
def main():

    # Create Updater object and attach dispatcher to it
    updater = Updater(telegram_token)
    dp = updater.dispatcher
    print("Bot started")

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MENU: [CallbackQueryHandler(menu)],
            CURWEATHER: [CallbackQueryHandler(weather, pass_user_data=True)],
            RESTAURANT: [MessageHandler(Filters.text, get_restaurant)],
            SETWHEN : [CallbackQueryHandler(set_when)],
            SETWHERE : [CallbackQueryHandler(set_where)],
            SETHOWMANY : [CallbackQueryHandler(set_howmany)]
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