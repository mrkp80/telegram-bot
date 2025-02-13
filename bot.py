from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# دستور شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"سلام {update.effective_user.first_name}!\nبه ربات مدیریت پروژه خوش آمدید.")

# دستور تست
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("دستورهای موجود:\n/start - شروع\n/help - راهنما")

if __name__ == "__main__":
    # توکن ربات خود را اینجا جایگزین کنید
    TOKEN = "7944939168:AAHol_MaUBGWwCUgQanKGj3hUbZjFV_cJWs"

    # ساخت اپلیکیشن
    app = ApplicationBuilder().token(TOKEN).build()

    # اضافه کردن دستورها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # اجرا
    print("ربات در حال اجراست...")
    app.run_polling()
