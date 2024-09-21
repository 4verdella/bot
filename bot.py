from telebot import TeleBot
from telebot.types import LabeledPrice
from parsing.parsing_laptop import *
from parsing.parsing_tv import *
from parsing.parsing_pc import *
from keyboards import *
from localization.lang_bot import *
from localization.lang_key import *
from config.config import Bot_config


cfg_token = Bot_config().token
token = cfg_token
bot = TeleBot(token)

cfg_clicktoken = Bot_config().click_token
click_token = cfg_clicktoken

user_langs = {}

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    chat_first_name = message.from_user.first_name
    bot.send_message(chat_id,f"️salom {chat_first_name}\n\nsiz ushbu botda o'zingizga kerakli mahsulotni topa olasiz")
    localization(message)


def localization(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "tilni tanlang:\n\nselect a language:\n\nвыберите язык:",
                     reply_markup=generate_localization())
    bot.register_next_step_handler(message, main_menu)


def main_menu(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id)

    if message.text == "🇺🇿UZB":
        lang = "uz"

    if message.text == "🇺🇸ENG":
        lang = "en"

    if message.text == "🇷🇺RUS":
        lang = "ru"


    bot.send_message(chat_id,select_catalog[lang],reply_markup=generate_catalog(lang))

    user_langs[chat_id] = lang
    bot.register_next_step_handler(message,main_catalogs)


def main_catalogs(message, product_id=0, products=None):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id)

    if message.text == back_main_menu[lang]:
        return start(message)

    if message.text == catalogs_laptop[lang]:
        products = PostgreSql_laptop().select_data()

    if message.text == catalogs_pc[lang]:
        products = PostgreSql_pc().select_data()

    if message.text == catalogs_tv[lang]:
        products = PostgreSql_tv().select_data()

    if message.text == go_to_next[lang] and product_id < len(products):
        product_id += 1

    if message.text == go_to_back[lang] and product_id > 0:
        product_id -= 1

    product = products[product_id]

    product_title = product[0]
    product_url = product[1]
    product_img = product[2]
    product_price = product[3]
    product_description = product[4]
    bot.send_photo(chat_id, product_img, caption=f'{"Brand_name"}: {product_title}\n\n'
                                                    f'{"Description"}: {product_description}'
                                                    f'\n\n{"Price"}: {product_price}',
                                         reply_markup=generate_inline_url(product_url,lang))

    user_message = bot.send_message(chat_id, f"{leen_products[lang]} : {len(products) - (product_id + 1)}", reply_markup=generate_pagination(lang))

    if message.text == go_to_next[lang] and len(products) - (product_id + 1) == 0:
        bot.delete_message(chat_id,message.id + 2)
        bot.send_message(chat_id,no_product[lang], reply_markup=generate_pagination(lang))
        product_id = product_id - len(products)
    bot.register_next_step_handler(user_message, main_catalogs, product_id, products)

@bot.callback_query_handler(func=lambda call: True)
def get_callback_data(call):
    chat_id = call.message.chat.id
    if call.data == "buy":
        product_info = call.message.caption.split(": ")
        product_price = ""
        price = product_info[-1].replace('UZS', "")
        for x in price:
            if x.isdigit():
                product_price += x

        INVOICE = {
            "title": product_info[1],
            "description": product_info[3],
            "invoice_payload": "bot-defined invoice payload",
            "provider_token": click_token,
            "start_parameter": "pay",
            "currency": "UZS",
            "prices": [LabeledPrice(label=product_info[1], amount=int(product_price + "00"))],
        }

        bot.send_invoice(chat_id, **INVOICE)

@bot.pre_checkout_query_handler(func=lambda query: True)
def invoice_checkout(query):
    """ Проверка чека """
    bot.answer_pre_checkout_query(query.id, ok=True, error_message="Ошибка оплаты !")





bot.polling()


