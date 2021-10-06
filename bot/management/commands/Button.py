import random

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup
from bot.models import *

def answer_button(id = 1):
    question = Test.objects.get(id = id)
    test = Answer.objects.filter(test=question)
    variants = []
    for i in test:
        variants.append([i.var, i.id])
    button =[]
    random.shuffle(variants)
    for i in range(4):
        button.append([InlineKeyboardButton(f'{variants[i][0]}', callback_data=f'{variants[i][1]}')])
    return InlineKeyboardMarkup(button)
