
def list_inactive_habits(user_id):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    # Выбираем все привычки, которые не активны или не были добавлены пользователем
    cur.execute("""
        SELECT habit.id, habit.name 
        FROM habit 
        LEFT JOIN user_habit ON habit.id = user_habit.habit_id AND user_habit.user_id = ?
        WHERE user_habit.active IS NULL OR user_habit.active = 0
        """, (user_id,))
    habits = cur.fetchall()

    if habits:
        # Создаем словарь с названиями привычек в качестве ключей и их ID в качестве значений
        habits_dict = {habit[1]: habit[0] for habit in habits}
        conn.close()
        return habits_dict
    else:
        conn.close()
        return None