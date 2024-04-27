import telebot

def send_chart(chat_id, period):
    file_path = plot_progress_chart(user_id=chat_id, period = period)
    if not file_path:
        bot.send_message(chat_id, "У Вас нет подключенных привычек")
    else:
        with open(file_path, 'rb') as photo:
            period_text = 'неделю' if period == 'week' else 'месяц'
            bot.send_photo(chat_id, photo, caption=f"Прогресс выполнения привычек за {period_text}")
    os.remove(file_path)

#@bot.message_handler(commands=['start'])
 #   def start(message):
  #      chat_id = message.chat.id
  #      send_chart(chat_id, 'week')
  #      send_chart(chat_id, 'month')