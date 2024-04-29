def assign_habit(user_id, habit_id, frequency_name, frequency_count):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()

    # Проверяем существует ли уже такая запись и её статус
    cur.execute("""
        SELECT active FROM user_habit 
        WHERE user_id = ? AND habit_id = ?
        """, (user_id, habit_id))
    result = cur.fetchone()

    if result is None:
        # Добавляем новую запись, если она не существует
        cur.execute("""
            INSERT INTO user_habit (user_id, habit_id, frequency_name, frequency_count) 
            VALUES (?, ?, ?, ?)
            """, (user_id, habit_id, frequency_name, frequency_count))
    elif result[0] == 0:
        # Обновляем существующую неактивную запись
        cur.execute("""
            UPDATE user_habit 
            SET active = 1, frequency_name = ?, frequency_count = ?
            WHERE user_id = ? AND habit_id = ?
            """, (frequency_name, frequency_count, user_id, habit_id))

    # Получаем имя привычки для сообщения пользователю
    cur.execute("SELECT name FROM habit WHERE id = ?", (habit_id,))
    habit_name = cur.fetchone()[0]

    # Определение правильного склонения слова "раз"
    if frequency_count == 1:
        count_word = "раз"
    elif 2 <= frequency_count % 10 <= 4 and (frequency_count % 100 < 10 or frequency_count % 100 > 20):
        count_word = "раза"
    else:
        count_word = "раз"

    # Формирование текста в зависимости от периодичности
    frequency_text = {
        "ежедневно": "в день",
        "еженедельно": "в неделю",
        "ежемесячно": "в месяц"
    }.get(frequency_name, "в неопределённый период")

    message_text = f"Вы добавили себе привычку '{habit_name}', которую хотите выполнять {frequency_count} {count_word} {frequency_text}."

    conn.commit()
    conn.close()
    return message_text