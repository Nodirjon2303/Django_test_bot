import random
from django.core.management.base import BaseCommand
from telegram.utils.request import Request
from telegram import Bot
from django.conf import settings
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler
from .Button import *
from bot.views import read

state_name = 1
state_question = 2
state_main = 3
state_last = 4
state_admin_main = 5
state_reklama = 6
state_admin_word = 7
state_add_admin = 8

def start(update, context):
    update.message.reply_text("Assalomu alaykum\n"
                              "Xush kelibsiz")
    id = update.effective_user.id
    username = update.effective_user.username

    try:
        Profile.objects.get_or_create(telegram_id=id, username=username)
        user = Profile.objects.get(telegram_id=id)
    except Exception as e:
        update.message.reply_text("error sodir buldi @ruzimurodov_nodir ga murojaat qiling\n"
                                  f"{e}")
    if user.status == 'admin':
        update.message.reply_text("Admin panel", reply_markup=admin_main())
        return state_admin_main
    update.message.reply_text("\nIsm familyangizni kiriting:")

    return state_name


def command_name(update, context):
    full_name = update.message.text
    user = Profile.objects.get(telegram_id=update.effective_user.id)
    user.full_name = full_name
    user.save()
    context.user_data['right']  =0
    soni = context.user_data['soni'] = 0
    context.user_data['savollar'] = []
    question = Test.objects.all()
    res = []
    l = []
    for i in question:
        res.append(i.id)
    l = random.sample(res, 10)
    context.user_data['savollar'] = l
    print("savollar", context.user_data['savollar'][soni])
    id = l[soni]
    test = Test.objects.get(id=id)
    try:
        update.message.reply_text(test.question, reply_markup=answer_button(id))
        context.user_data['soni'] += 1
    except Exception as e:
        update.message.reply_text(f'eror {e}')
    return state_question

def command_test(update, context):
    query = update.callback_query
    A = query.data
    query.message.delete()
    soni = context.user_data['soni']
    if A.isdigit():
        A = int(A)
        l =[]
        l = context.user_data['savollar']
        id = l[soni]
        question = Test.objects.get(id=l[soni-1])
        if A == question.right:
            context.user_data['right']+=1
        if soni<9:
            test = Test.objects.get(id=int(context.user_data['savollar'][soni]))
            query.message.reply_text(text=test.question, reply_markup=answer_button(id))
            context.user_data['soni'] += 1
            return state_question
        else:
            test = Test.objects.get(id=int(context.user_data['savollar'][soni]))
            query.message.reply_text(text=test.question, reply_markup=answer_button(int(context.user_data['savollar'][soni])))
            return state_last
    else:
        query.message.reply_text('main manu', reply_markup=ReplyKeyboardRemove())
        return state_main

def command_last(update, context):
    query = update.callback_query
    A = query.data
    query.message.delete()
    soni = context.user_data['soni']
    user = Profile.objects.get(telegram_id=update.effective_user.id)
    if A.isdigit():
        A = int(A)
        question = Test.objects.get(id=int(context.user_data['savollar'][soni]))
        if A == question.right:
            context.user_data['right'] += 1
        query.message.reply_text(f"Rahmat Sizning natijangiz: {context.user_data['right']}/10\n"
                                 f"Testni qayta boshlash uchun ixtiyoriy so'zni yuboring")
        xabar = f"username: @{user.username}\n" \
                f"Ismi: {user.full_name}\n" \
                f"Natija: {context.user_data['right']}/10"
        admin = Profile.objects.filter(status='admin')
        for i in admin:
            try:
                context.bot.send_message(chat_id=i.telegram_id, text=xabar)
            except:
                print("Admin eror")
        return state_main


    else:
        update.message.reply_text('main manu', reply_markup=ReplyKeyboardRemove())
        return state_main


def command_add(update, context):
    update.message.reply_text("Savollarni Word variantda yuboring\n"
                              "Yangi savollar yuborilganda eskilari o'chib ketadi  shu sababli fayl yuborishda ehtiyotkor bo'lishingizni so'rab qolardim")
    return state_admin_word
def command_adv(update, context):
    update.message.reply_html("Foydalanuvchilarga yubormoqchi bo'lgan xabaringizni menga yuboring",
                              reply_markup=ReplyKeyboardRemove())
    return state_reklama

def command_adv_send(update, context):
    id = update.message.message_id
    users = Profile.objects.all()
    admins = Profile.objects.filter(status='admin')
    soni = 0
    for i in users:
        try:
            context.bot.forward_message(chat_id=i.telegram_id,from_chat_id=update.effective_user.id, message_id=id)
            soni+=1
        except Exception as e:
            print(e)
    for i in admins:
        try:
            context.bot.send_message(chat_id=i.telegram_id, text=f"xabar {soni} ta kishiga muaffaqiyatli yuborildi", reply_markup=admin_main())
        except Exception as e:
            print(e)
    return state_admin_main
def command_test_update(update, context):
    print(update.message)
    id = update.message['document']['file_id']
    fileName = update.message['document']['file_name']
    doc = context.bot.get_file(id)
    print(fileName)
    doc.download(f'media\\{fileName}')
    read(fileName)
    update.message.reply_text("File muaffaqiyatli yangilandi" ,reply_markup=admin_main())
    return state_admin_main

def command_add_admin(update, context):
    update.message.reply_html("Yangi adminning <b>id</b> raqamini yuboring", reply_markup=ReplyKeyboardRemove())
    return state_add_admin

def command_admin(update, context):
    id  = update.message.text
    if id.isdigit():
        id = int(id)
        try:
            profile = Profile.objects.get(telegram_id=id)
            profile.status = 'admin'
            profile.save()
        except Exception as e:
            print(e)
        update.message.reply_text("yangi admin muaffaqiyatli qo'shildi", reply_markup=admin_main())
        return state_admin_main
    else:
        update.message.reply_text("siz noto'g'ri id yubordingiz", reply_markup=admin_main())
        return state_admin_main

class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=None,
            read_timeout=None
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )

        updater = Updater(
            bot=bot,
            use_context=True
        )

        conv_hand = ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text, start)
            ],
            states={
                state_main:[
                   MessageHandler(Filters.text, start)
                ],
                state_name: [
                    MessageHandler(Filters.text, command_name)
                ],
                state_question: [
                    CallbackQueryHandler(command_test)
                ],
                state_last: [
                    CallbackQueryHandler(command_last)
                ],
                state_admin_main: [
                    MessageHandler(Filters.regex('^(' + "Reklama yuborish" + ')$'), command_adv),
                    MessageHandler(Filters.regex('^(' + "savol qo'shish" + ')$'), command_add),
                    MessageHandler(Filters.regex('^(' + "add admin" + ')$'), command_add_admin),
                ],
                state_reklama: [
                    MessageHandler(Filters.text, command_adv_send),
                    MessageHandler(Filters.photo, command_adv_send),
                    MessageHandler(Filters.video, command_adv_send),
                    MessageHandler(Filters.audio, command_adv_send),
                    MessageHandler(Filters.invoice, command_adv_send),
                ],
                state_admin_word: [
                    MessageHandler(Filters.document, command_test_update)
                ],
                state_add_admin: [
                    MessageHandler(Filters.text, command_admin)
                ]
            },
            fallbacks=[
                CommandHandler('start', start)
            ]

        )
        updater.dispatcher.add_handler(conv_hand)

        updater.start_polling()
        updater.idle()

