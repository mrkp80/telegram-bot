
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import CallbackContext

# پروژه‌ها و مراحل مختلف
projects = {}

# دستور /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('سلام! خوش آمدید به ربات مدیریت پروژه. لطفاً یک دستور را وارد کنید.')

# ایجاد پروژه جدید
def create_project(update: Update, context: CallbackContext) -> None:
    project_name = ' '.join(context.args)
    if project_name:
        projects[project_name] = {
            'phases': {},
            'total_cost': 0,
            'due_date': None
        }
        update.message.reply_text(f"پروژه '{project_name}' با موفقیت ایجاد شد.")
    else:
        update.message.reply_text("لطفاً نام پروژه را وارد کنید.")

# نمایش پروژه‌ها
def show_projects(update: Update, context: CallbackContext) -> None:
    if not projects:
        update.message.reply_text("هیچ پروژه‌ای وجود ندارد.")
    else:
        project_list = '\n'.join([f"- {project}" for project in projects])
        update.message.reply_text(f"پروژه‌ها:\n{project_list}")

# ایجاد مرحله جدید برای پروژه
def create_phase(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 3:
        update.message.reply_text("لطفاً نام پروژه، نام مرحله و تاریخ شروع را وارد کنید.")
        return
    
    project_name = context.args[0]
    phase_name = context.args[1]
    start_date = context.args[2]
    
    if project_name not in projects:
        update.message.reply_text(f"پروژه '{project_name}' وجود ندارد.")
        return

    projects[project_name]['phases'][phase_name] = {
        'start_date': start_date,
        'end_date': None,
        'cost': 0
    }

    update.message.reply_text(f"مرحله '{phase_name}' برای پروژه '{project_name}' با تاریخ شروع {start_date} ایجاد شد.")

# ثبت هزینه برای هر مرحله
def add_cost(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 3:
        update.message.reply_text("لطفاً نام پروژه، نام مرحله و هزینه را وارد کنید.")
        return
    
    project_name = context.args[0]
    phase_name = context.args[1]
    cost = float(context.args[2])
    
    if project_name not in projects:
        update.message.reply_text(f"پروژه '{project_name}' وجود ندارد.")
        return

    if phase_name not in projects[project_name]['phases']:
        update.message.reply_text(f"مرحله '{phase_name}' در پروژه '{project_name}' وجود ندارد.")
        return

    projects[project_name]['phases'][phase_name]['cost'] = cost
    projects[project_name]['total_cost'] += cost

    update.message.reply_text(f"هزینه مرحله '{phase_name}' برای پروژه '{project_name}' به {cost} ثبت شد.")

# نمایش اطلاعات پروژه
def project_info(update: Update, context: CallbackContext) -> None:
    project_name = ' '.join(context.args)
    
    if project_name not in projects:
        update.message.reply_text(f"پروژه '{project_name}' وجود ندارد.")
        return
    
    project = projects[project_name]
    phase_info = ""
    for phase, details in project['phases'].items():
        phase_info += f"\n- {phase} | تاریخ شروع: {details['start_date']} | هزینه: {details['cost']}"
    
    update.message.reply_text(f"پروژه '{project_name}':\nمجموع هزینه‌ها: {project['total_cost']}\nمراحل:{phase_info}")

# تنظیمات ربات و شروع
def main():
    updater = Updater("7944939168:AAHol_MaUBGWwCUgQanKGj3hUbZjFV_cJWs", use_context=True)
    
    # ثبت دستورات
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("createproject", create_project))
    dp.add_handler(CommandHandler("showprojects", show_projects))
    dp.add_handler(CommandHandler("createphase", create_phase))
    dp.add_handler(CommandHandler("addcost", add_cost))
    dp.add_handler(CommandHandler("projectinfo", project_info))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
