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
      "Bu yerda siz o'zingizga kerakli fanlar va imtihonlarga"
      " tayyorgarlik ko'rishingiz mumkin.\n\nKerakli bo'limni tanlang:"
  )
  bot.send_message(
      message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown'
  )


# Asosiy matnli xabarlar va bo'limlar
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
        '📚 **Fanlarni tanlang:**\nQuyidagi fanlardan birini tanlang:',
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif message.text == '🏅 Milliy Sertifikatlar':
    sertifikat_text = (
        '🏅 **Milliy Sertifikatlar boʻlimi**\n\n'
        "Bu bo'limda fanlar bo'yicha milliy sertifikat imtihonlariga"
        " tayyorgarlik ko'rishingiz mumkin:\n\n"
        '• 📐 **Matematika** (Tahlillar va testlar)\n'
        '• ⚡ **Fizika** (Qonun-qoidalar)\n'
        '• 🧪 **Kimyo & Biologiya** (Asosiy formulalar)\n\n'
        '📌 *Eslatma: Tez orada har bir fan boʻyicha test variantlari'
        ' yuklanadi!*'
    )
    bot.send_message(
        message.chat.id, sertifikat_text, parse_mode='Markdown'
    )

  elif message.text == '🇬🇧 CEFR & IELTS':
    cefr_text = (
        '🇬🇧 **CEFR & IELTS tayyorgarlik boʻlimi**\n\n'
        'Ingliz tilini oʻrganish uchun foydali yoʻnalishlar:\n\n'
        '📚 **Vocabulary (Lugʻat):** Eng koʻp ishlatiladigan 3000 ta'
        ' soʻz.\n'
        '✍️ **Grammar (Grammatika):** B1/B2 darajasidagi qoidalar.\n'
        '🎧 **Listening & Reading:** Amaliy matnlar va audial'
        ' materiallar.\n\n'
        '🎯 *Maqsadingiz yuqori ball olish boʻlsa, har kuni lugʻat yodlang!*'
    )
    bot.send_message(message.chat.id, cefr_text, parse_mode='Markdown')

  elif message.text == 'ℹ️ Biz haqimizda':
    about_text = (
        'ℹ️ **Talim.Uz haqida**\n\n'
        "Maqsadimiz — yoshlarga sifatli ta'lim materiallarini yetkazish,"
        " milliy sertifikat va xalqaro imtihonlarga (IELTS/CEFR)"
        " mustaqil tayyorgarlik ko'rishda ko'maklashish.\n\n"
        '💡 Botingiz boʻyicha takliflar va savollar uchun: @admin_username'
    )
    bot.send_message(message.chat.id, about_text, parse_mode='Markdown')


# Fanlar ichidagi tugmalar bosilganda chiqadigan ma'lumotlar
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  bot.answer_callback_query(call.id)

  if call.data == 'math':
    math_info = (
        '📐 **Matematika boʻlimi:**\n\n'
        '• **Algebra:** Kvadrat tenglamalar, logarifmlar, trigonometriya'
        ' formulalari.\n'
        '• **Geometriya:** Pifagor teoremasi, yuzlar va hajm topish'
        ' qoidalari.\n\n'
        '📌 *Tez kunda mavzuli testlar va yechimlari bilan misollar'
        ' qoʻshiladi!*'
    )
    bot.send_message(
        call.message.chat.id, math_info, parse_mode='Markdown'
    )

  elif call.data == 'physics':
    physics_info = (
        '⚡ **Fizika boʻlimi:**\n\n'
        '• **Mexanika:** Kinematika va dinamika qonunlari.\n'
        '• **Termodinamika:** Gaz qonunlari va issiqlik miqdori.\n'
        '• **Elektr:** Oks, Koulon qonunlari va formulalar.\n\n'
        '📌 *Masalalar yechish usullari va qisqacha qoʻllanmalar joylanmoqda.*'
    )
    bot.send_message(
        call.message.chat.id, physics_info, parse_mode='Markdown'
    )

  elif call.data == 'history':
    history_info = (
        '🏛 **Tarix boʻlimi:**\n\n'
        "• **O'zbekiston tarixi:** Qadimgi sivilizatsiyalar, xonliklar va"
        ' jadidlar davri.\n'
        '• **Jahon tarixi:** Buyuk geografik kashfiyotlar va XX asr'
        ' voqealari.\n\n'
        '📌 *Xronologiya va muhim sanalar roʻyxati tayyorlanmoqda.*'
    )
    bot.send_message(
        call.message.chat.id, history_info, parse_mode='Markdown'
    )

  elif call.data == 'native':
    native_info = (
        '🇺🇿 **Ona tili boʻlimi:**\n\n'
        '• **Fonetika:** Tovushlar turlari va urgʻu qoidalari.\n'
        '• **Morfologiya:** Soʻz turkumlari (ot, sifat, feʼl va h.k.).\n'
        '• **Sintaksis:** Qoʻshma gaplar va tinish belgilari.\n\n'
        '📌 *Imlo qoidalari va testlar tez kunda qoʻshiladi!*'
    )
    bot.send_message(
        call.message.chat.id, native_info, parse_mode='Markdown'
    )


if __name__ == '__main__':
  # Veb-serverni alohida oqimda ishga tushiramiz
  t = threading.Thread(target=run_flask)
  t.start()

  print('Bot va Server ishga tushdi!')
  bot.infinity_polling()
