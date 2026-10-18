# Matnli xabarlarga javob (Asosiy tugmalar bosilganda)
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
          'Bu yerda Milliy sertifikat imtihoni topshiruvchilar uchun testlar va'
          ' qoʻllanmalar joylab boriladi.',
      )

    elif text == '🇬🇧 CEFR & IELTS':
      markup = types.InlineKeyboardMarkup(row_width=1)
      btn_cefr = types.InlineKeyboardButton(
          '📘 CEFR Qoʻllanma va Testlar', url='https://t.me/talim_rasmiy_uz/8'
      )
      btn_ielts = types.InlineKeyboardButton(
          '📕 IELTS Oʻquv Materiallari', url='https://t.me/talim_rasmiy_uz/11'
      )
      markup.add(btn_cefr, btn_ielts)

      bot.send_message(
          message.chat.id,
          '🇬🇧 **CEFR & IELTS boʻlimi**\n\n'
          'Kerakli boʻlim boʻyicha materiallarni yuklab olish uchun quyidagi'
          ' tugmalardan birini tanlang:',
          reply_markup=markup,
          parse_mode='Markdown',
      )

    elif text == 'ℹ️ Biz haqimizda':
      bot.send_message(
          message.chat.id,
          "ℹ️ **Talim.Uz** — oʻquvchilarga bepul ta'limiy resurslar va"
          ' darsliklar yetkazib beruvchi rasmiy bot.',
      )

    else:
      bot.send_message(
          message.chat.id,
          'Tushunmadim. Iltimos, pastdagi tugmalardan birini bosing.',
      )

  except Exception as e:
    print(f'Xatolik matnda: {e}')


# Inline tugmalar (Fanlar ichi) bosilganda
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  try:
    bot.answer_callback_query(call.id)

    # 1. MATEMATIKA BOSILGANDA
    if call.data == 'math':
      text = (
          '📐 **Matematika fanidan oʻquv materiallari:**\n\n'
          'Quyidagi tugma orqali darslik va qoʻllanmalarni yuklab oling:'
      )
      markup = types.InlineKeyboardMarkup()
      btn = types.InlineKeyboardButton(
          '📂 Matematika materiallarini yuklash',
          url='https://t.me/talim_rasmiy_uz/4',
      )
      markup.add(btn)
      bot.send_message(
          call.message.chat.id, text, reply_markup=markup, parse_mode='Markdown'
      )

    # 2. TARIX BOSILGANDA
    elif call.data == 'history':
      text = (
          '🏛 **Tarix fanidan oʻquv materiallari:**\n\n'
          'Quyidagi tugma orqali darslik va manbalarni yuklab oling:'
      )
      markup = types.InlineKeyboardMarkup()
      btn = types.InlineKeyboardButton(
          '📂 Tarix materiallarini yuklash',
          url='https://t.me/talim_rasmiy_uz/9?single',
      )
      markup.add(btn)
      bot.send_message(
          call.message.chat.id, text, reply_markup=markup, parse_mode='Markdown'
      )

    # 3. ONA TILI BOSILGANDA
    elif call.data == 'native':
      text = (
          '🇺🇿 **Ona tili va Adabiyotdan oʻquv materiallari:**\n\n'
          'Quyidagi tugma orqali qoʻllanmalarni yuklab oling:'
      )
      markup = types.InlineKeyboardMarkup()
      btn = types.InlineKeyboardButton(
          '📂 Ona tili materiallarini yuklash',
          url='https://t.me/talim_rasmiy_uz/6',
      )
      markup.add(btn)
      bot.send_message(
          call.message.chat.id, text, reply_markup=markup, parse_mode='Markdown'
      )

    # 4. FIZIKA BOSILGANDA (Hozircha havola kiritilmagan bo'lsa)
    elif call.data == 'physics':
      text = (
          '⚡ **Fizika fanidan materiallar:**\n\n'
          'Hozircha materiallar yuklanmoqda...'
      )
      bot.send_message(
          call.message.chat.id, text, parse_mode='Markdown'
      )

  except Exception as e:
    print(f'Xatolik callback da: {e}')
