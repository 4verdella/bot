from telebot import types
from localization.lang_key import *


def generate_localization():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_uzb = types.KeyboardButton(text="🇺🇿UZB")
    key_eng = types.KeyboardButton(text="🇺🇸ENG")
    key_rus = types.KeyboardButton(text="🇷🇺RUS")
    keyboard.row(key_uzb,key_rus,key_eng)
    return keyboard



def generate_catalog(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_laptop = types.KeyboardButton(text=catalogs_laptop[lang])
    key_pc = types.KeyboardButton(text=catalogs_pc[lang])
    key_tv = types.KeyboardButton(text=catalogs_tv[lang])
    keyboard.row(key_laptop,key_pc,key_tv)
    return keyboard


def generate_inline_url(url,lang):
    keyboard = types.InlineKeyboardMarkup()
    btn_more_bay = types.InlineKeyboardButton(text=for_buy[lang], callback_data="buy")
    btn_url = types.InlineKeyboardButton(text=for_url[lang],url=url)
    keyboard.row(btn_more_bay,btn_url)
    return keyboard

def generate_pagination(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_next = types.KeyboardButton(text=go_to_next[lang])
    btn_back = types.KeyboardButton(text=go_to_back[lang])
    btn_menu = types.KeyboardButton(text=back_main_menu[lang])
    keyboard.row(btn_back, btn_next)
    keyboard.row(btn_menu)
    return keyboard


