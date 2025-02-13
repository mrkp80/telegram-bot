from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# وضعیت‌ها برای ConversationHandler
CATEGORY, SUBCATEGORY, TASK_DETAILS, REPORT = range(4)

# تعریف چک‌لیست
CHECKLIST = {
    "طراحی پروژه": ["طراحی فاز 1 و تایید شهرداری", "طراحی کامل (فاز 2) و تایید شهرداری"],
    "اخذ پروانه": ["آزمایشگاه مکانیک خاک و نقشه‌برداری", "اخذ پروانه"],
    "انشعابات": ["انشعاب آب و فاضلاب", "انشعاب برق", "انشعاب گاز", "انشعاب تلفن"],
    # ادامه چک‌لیست به همین ترتیب...
}

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['progress'] = {"category": 0, "subcategory": 0, "details": []}
    categories = list(CHECKLIST.keys())
    await update.message.reply_text(f"سلام! لطفا دسته‌بندی زیر را انتخاب کنید:\n\n" + "\n".join(categories))
    return CATEGORY

# دریافت دسته‌بندی
async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    category_name = update.message.text
    if category_name not in CHECKLIST:
        await update.message.reply_text("لطفا یک دسته‌بندی معتبر انتخاب کنید.")
        return CATEGORY
    context.user_data['current_category'] = category_name
    subcategories = CHECKLIST[category_name]
    await update.message.reply_text(f"دسته '{category_name}' انتخاب شد.\nمرحله اول: {subcategories[0]}")
    return SUBCATEGORY

# دریافت زیرمرحله
async def subcategory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    subcategory_name = update.message.text
    current_category = context.user_data['current_category']
    subcategories = CHECKLIST[current_category]
    if subcategory_name not in subcategories:
        await update.message.reply_text("لطفا یک مرحله معتبر انتخاب کنید.")
        return SUBCATEGORY

    context.user_data['current_subcategory'] = subcategory_name
    await update.message.reply_text(f"برای '{subcategory_name}' لطفا نوع کار و هزینه را وارد کنید (مثال: نوع کار: بتن‌ریزی، هزینه: 5000000).")
    return TASK_DETAILS

# دریافت جزئیات کار
async def task_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    details = update.message.text
    category = context.user_data['current_category']
    subcategory = context.user_data['current_subcategory']
    context.user_data['progress']['details'].append({
        "category": category,
        "subcategory": subcategory,
        "details": details
    })

    await update.message.reply_text(f"اطلاعات '{subcategory}' ثبت شد. اگر می‌خواهید ادامه دهید، دسته‌بندی بعدی را وارد کنید یا دستور /report را بزنید.")
    return CATEGORY

# تولید گزارش
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    progress = context.user_data['progress']['details']
    if not progress:
        await update.message.reply_text("هیچ اطلاعاتی برای گزارش ثبت نشده است.")
        return

    report_text = "گزارش پروژه:\n\n"
    for item in progress:
        report_text += f"دسته‌بندی: {item['category']}\nمرحله: {item['subcategory']}\nجزئیات: {item['details']}\n\n"

    await update.message.reply_text(report_text)

# تنظیمات Webhook
if __name__ == "__main__":
    import os

    TOKEN = "7944939168:AAHol_MaUBGWwCUgQanKGj3hUbZjFV_cJWs"
    WEBHOOK_URL = "https://api.telegram.org/bot7944939168:AAHol_MaUBGWwCUgQanKGj3hUbZjFV_cJWs/getWebhookInfo"

    app = ApplicationBuilder().token(TOKEN).build()

    # اضافه کردن دستورها
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category)],
            SUBCATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, subcategory)],
            TASK_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, task_details)],
        },
        fallbacks=[],
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("report", report))

    # تنظیم Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://api.telegram.org/bot7944939168:AAHol_MaUBGWwCUgQanKGj3hUbZjFV_cJWs/getWebhookInfo",
    )
