import os
import threading
import telebot
from flask import Flask
from telebot import types

TOKEN = '8845810892:AAG8-L2XNFkbd177tw9i1GwIsfSjd-S5GQQ'
bot = telebot.TeleBot(TOKEN)

# Sizning Admin ID raqamingiz kiritildi:
ADMIN_ID = 6042443325

# Flask server
app = Flask(__name__)


@app.route('/')
def home():
  return 'Talim.Uz Boti Ishlayapti!'


def run_flask():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


# Foydalanuvchini faylga saqlash funksiyasi
def save_user(user_id):
  if not os.path.exists('users.txt'):
    open('users.txt', 'w').close()

  with open('users.txt', 'r+') as f:
    users = f.read().splitlines()
    if str(user_id) not in users:
      f.write(f'{user_id}\n')


# Jami foydalanuvchilar sonini olish
def get_users_count():
  if not os.path.exists('users.txt'):
    return 0
  with open('users.txt', 'r') as f:
    users = f.read().splitlines()
    return len(users)


# /start buyrug'i
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  try:
    save_user(message.from_user.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_fanlar = types.KeyboardButton('📚 Fanlar')
    btn_sertifikat = types.KeyboardButton('🏅 Milliy Sertifikatlar')
    btn_cefr_ielts = types.KeyboardButton('🇬🇧 CEFR & IELTS')
    btn_about = types.KeyboardButton('ℹ️ Biz haqimizda')

    markup.add(btn_fanlar, btn_sertifikat, btn_cefr_ielts, btn_about)

    welcome_text = (
        f"Assalomu alaykum, {message.from_user.first_name}!\n\n"
        "🎓 **Talim.Uz** ta'limiy botiga xush kelibsiz.\n\n"
        "Quyidagi tugmalardan birini tanlang:"
    )
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=markup,
        parse_mode='Markdown',
    )
  except Exception as e:
    print(f'Xatolik /start da: {e}')


# /stat buyrug'i - Faqat Admin uchun statistika
@bot.message_handler(commands=['stat', 'stats'])
def show_stats(message):
  if message.from_user.id == ADMIN_ID:
    count = get_users_count()
    bot.send_message(
        message.chat.id,
        f'📊 **Bot Statistikasi:**\n\n👤 Jami foydalanuvchilar soni: **{count}**'
        ' ta',
        parse_mode='Markdown',
    )
  else:
    bot.send_message(
        message.chat.id, 'Siz ushbu buyruqdan foydalana olmaysiz.'
    )


# Matnli xabarlarga javob
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
  try:
    save_user(message.from_user.id)
    text = message.text

    if text == '📚 Fanlar':
      markup = types.InlineKeyboardMarkup(row_width=2)
      btn_math = types.InlineKeyboardButton(
          '📐 Matematika', callback_data='math'
      )
      btn_fizika = types.InlineKeyboardButton(
          '⚡ Fizika', callback_data='physics'
      )
      btn_tarix = types.InlineKeyboardButton('🏛 Tarix', callback_data='history')
      btn_ona_tili = types.InlineKeyboardButton(
          '🇺🇿 Ona tili', callback_data='native'
      )
      markup.add(btn_math, btn_fizika, btn_tarix, btn_ona_tili)

      bot.send_message(
          message.chat.id,
          '📚 **Fanlardan birini tanlang:**',
          reply_markup=markup,
          parse_mode='Markdown',
      )

    elif text == '🏅 Milliy Sertifikatlar':
      bot.send_message(
          message.chat.id,
          '🏅 **Milliy Sertifikatlar boʻlimi**\n\n'
          "Bu yerda Matematika, Fizika va ona tili fanlaridan milliy"
          " sertifikat imtihoni topshiruvchilar uchun testlar va"
          ' qoʻllanmalar joylab boriladi.',
      )

    elif text == '🇬🇧 CEFR & IELTS':
      bot.send_message(
          message.chat.id,
          '🇬🇧 **CEFR & IELTS boʻlimi**\n\n'
          'Ingliz tilidan B2 va C1 darajalarini olish uchun kerakli lugʻatlar'
          ' hamda grammatik qoidalar toʻplami.',
      )

    elif text == 'ℹ️ Biz haqimizda':
      bot.send_message(
          message.chat.id,
          "ℹ️ **Talim.Uz** — oʻquvchilarga bepul ta'limiy resurslar yetkazib"
          ' beruvchi platforma.',
      )

    else:
      bot.send_message(
          message.chat.id,
          'Tushunmadim. Iltimos, pastdagi tugmalardan birini bosing.',
      )

  except Exception as e:
    print(f'Xatolik matnda: {e}')


# Inline tugmalar
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  try:
    bot.answer_callback_query(call.id)

    if call.data == 'math':
      bot.send_message(
          call.message.chat.id,
          '📐 **Matematika:**\n\n- Algebra formulalari\n- Geometriya'
          ' amaliyotlari\n- Testlar toʻplami',
      )
    elif call.data == 'physics':
      bot.send_message(
          call.message.chat.id,
          '⚡ **Fizika:**\n\n- Mexanika va dinamika\n- Elektr va magnetizm',
      )
    elif call.data == 'history':
      bot.send_message(
          call.message.chat.id,
          '🏛 **Tarix:**\n\n- Oʻzbekiston tarixi\n- Jahon tarixi sanalari',
      )
    elif call.data == 'native':
      bot.send_message(
          call.message.chat.id,
          '🇺🇿 **Ona tili:**\n\n- Grammatika qoidalari\n- Imlo lugʻati',
      )
  except Exception as e:
    print(f'Xatolik callback da: {e}')


if __name__ == '__main__':
  t = threading.Thread(target=run_flask)
  t.daemon = True
  t.start()

  print('Bot ishga tushdi...')
  bot.infinity_polling(timeout=10, long_polling_timeout=5)
