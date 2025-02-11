import telebot

TOKEN = "7944939168:AAHol_MaUBGWwCUgQanKGj3hUbZjFV_cJWs"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من ربات تلگرام شما هستم.")

bot.polling()
