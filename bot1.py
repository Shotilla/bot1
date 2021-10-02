from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from covid import Covid

buttons = ReplyKeyboardMarkup([['Uzbekiston statistikasi'],['Dunyo statistikasi'],['Admin']], resize_keyboard=True)

covit = Covid(source='worldometers')


def start(update,context):
    update.message.reply_text('Salom 😎 {} \nXush kelibsiz! \nBu mening birinchi botim kamchiliklar bulsa oldindan uzur.'.format(update.message.from_user.first_name),
                              reply_markup=buttons)
    return 1

def stats(update,context):
    data = covit.get_status_by_country_name('Uzbekistan')
    update.message.reply_html(
        "<i>🇺🇿 O'zbekiston sitatistikasi:</i>\n\n<b>Yuqtirganlar :</b> {}\n<b>Sog'ayganlar :</b> {}\n<b>Vafot etganlar :</b> {}".format(
            data['confirmed'],data['recovered'],data['deaths']),reply_markup=buttons)

def world(update,context):
    data1 = covit.get_total_confirmed_cases()
    data2 = covit.get_total_recovered()
    data3 = covit.get_total_deaths()
    update.message.reply_html(
        "<i>Dunyo sitatistikasi:</i>\n\n<b>Yuqtirganlar :</b> {}\n<b>Sog'ayganlar :</b> {}\n<b>Vafot etganlar :</b> {}".format(
            data1,data2,data3),reply_markup=buttons)

def admin(update,context):
    update.message.reply_text('@realist_0606')

updater = Updater('API Token',use_context=True)
conv_hander = ConversationHandler(
    entry_points=[CommandHandler('start',start)],
    states={
        1:[
            MessageHandler(Filters.regex('^(Uzbekiston statistikasi)$'),stats),
            MessageHandler(Filters.regex('^(Dunyo statistikasi)$'),world),
            MessageHandler(Filters.regex('^(Admin)$'),admin),
        ]
            },
    fallbacks=[MessageHandler(Filters.text,start)]
                                )

updater.dispatcher.add_handler(conv_hander)

updater.start_polling()
updater.idle()
