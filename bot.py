import os
import threading
import telebot
from flask import Flask
from telebot import types

TOKEN = '8845810892:AAG8-L2XNFkbd177tw9i1GwIsfSjd-S5GQQ'
bot = telebot.TeleBot(TOKEN)

# Render o'chirib qo'ymasligi uchun kichik veb-server
app = Flask(__name__)


@app.route('/')
def home():
  return 'Bot ishlayapti va faol!'


def run_flask():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


# /start buyrug'i
@bot.message_handler(commands=['start'])
def send_welcome(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn_fanlar = types.KeyboardButton('📚 Fanlar')
  btn_sertifikat = types.KeyboardButton('🏅 Milliy Sertifikatlar')
  btn_cefr_ielts = types.KeyboardButton('🇬🇧 CEFR & IELTS')
  btn_about = types.KeyboardButton('ℹ️ Biz haqimizda')

  markup.add(btn_fanlar, btn_sertifikat)
  markup.add(btn_cefr_ielts, btn_about)

  welcome_text = (
      f"Assalomu alaykum, {message.from_user.first_name}!\n\n"
      "🎓 **Talim.Uz** ta'limiy botiga xush kelibsiz.\n"
      "Kerakli bo'limni tanlang:"
  )
  bot.send_message(
      message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown'
  )


# Matnli xabarlar
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
  if message.text == '📚 Fanlar':
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_math = types.InlineKeyboardButton(
        '📐 Matematika', callback_data='math'
    )
    btn_fizika = types.InlineKeyboardButton('⚡ Fizika', callback_data='physics')
    btn_tarix = types.InlineKeyboardButton('🏛 Tarix', callback_data='history')
    btn_ona_tili = types.InlineKeyboardButton(
        '🇺🇿 Ona tili', callback_data='native'
    )
    markup.add(btn_math, btn_fizika, btn_tarix, btn_ona_tili)
    bot.send_message(
        message.chat.id,
        '📚 **Fanlarni tanlang:**',
        reply_markup=markup,
        parse_mode='Markdown',
    )
  elif message.text == '🏅 Milliy Sertifikatlar':
    bot.send_message(
        message.chat.id,
        '🏅 **Milliy Sertifikatlar boʻlimi**\n\nTayyorgarlik materiallari va'
        ' testlar.',
    )
  elif message.text == '🇬🇧 CEFR & IELTS':
    bot.send_message(
        message.chat.id,
        '🇬🇧 **CEFR & IELTS boʻlimi**\n\nIngliz tili imtihonlari uchun'
        ' materiallar.',
    )
  elif message.text == 'ℹ️ Biz haqimizda':
    bot.send_message(
        message.chat.id,
        'ℹ️ **Talim.Uz haqida**\n\nSifatli taʼlim materiallari platformasi.',
    )


# Inline tugmalar
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  bot.answer_callback_query(call.id)
  if call.data == 'math':
    bot.send_message(call.message.chat.id, '📐 **Matematika boʻlimi**')
  elif call.data == 'physics':
    bot.send_message(call.message.chat.id, '⚡ **Fizika boʻlimi**')
  elif call.data == 'history':
    bot.send_message(call.message.chat.id, '🏛 **Tarix boʻlimi**')
  elif call.data == 'native':
    bot.send_message(call.message.chat.id, '🇺🇿 **Ona tili boʻlimi**')


if __name__ == '__main__':
  # Veb-serverni alohida oqimda ishga tushiramiz
  t = threading.Thread(target=run_flask)
  t.start()

  print('Bot va Server ishga tushdi!')
  bot.infinity_polling()
