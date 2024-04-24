import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def plot_results(results, title):
    if not results:
        print("Нет данных для отображения.")
        return

    user_ids = [result[0] for result in results]
    habit_ids = [result[1] for result in results]
    frequencies = [result[2] for result in results]
    required_counts = [result[3] for result in results]
    total_marks = [result[4] for result in results]

    completion_percentages = []
    for frequency, marks, required in zip(frequencies, total_marks, required_counts):
        if frequency == 'ежедневно':
            expected_count = 7 * required  # Assuming a full week
        elif frequency == 'еженедельно':
            expected_count = required
        else:  # ежемесячно
            expected_count = required
        completion_percentages.append(min(100, (marks / expected_count) * 100))

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(completion_percentages)), completion_percentages, color='skyblue')
    plt.xlabel('Процент выполнения')
    plt.title(title)
    plt.yticks(range(len(completion_percentages)), [f'User {uid}, Habit {hid}' for uid, hid in zip(user_ids, habit_ids)])
    plt.show()

# Подключение к базе данных
conn = sqlite3.connect('easy_habit.db')
cursor = conn.cursor()

# Определение дат для анализа
today = datetime.now()
start_last_week = (today - timedelta(days=today.weekday() + 7)).date()
end_last_week = start_last_week + timedelta(days=6)  # Removed .date() here

start_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1).date()
end_last_month = (today.replace(day=1) - timedelta(days=1))  # Removed .date() here

# Формирование и выполнение SQL-запросов для недели и месяца
queries = {
    'last_week': ('Прошлая неделя', start_last_week.strftime('%Y-%m-%d'), end_last_week.strftime('%Y-%m-%d')),
    'last_month': ('Прошлый месяц', start_last_month.strftime('%Y-%m-%d'), end_last_month.strftime('%Y-%m-%d'))
}

for key, (title, start_date, end_date) in queries.items():
    query = '''
    SELECT uh.user_id, uh.habit_id, uh.frequency_name, uh.frequency_count, SUM(hh.mark_count) as total_marks
    FROM user_habit uh
    JOIN habit h ON uh.habit_id = h.id
    JOIN user_habit_history hh ON uh.user_id = hh.user_id AND uh.habit_id = hh.habit_id
    WHERE hh.mark_date BETWEEN ? AND ? AND uh.active = 1
    GROUP BY uh.user_id, uh.habit_id
    '''
    cursor.execute(query, (start_date, end_date))
    results = cursor.fetchall()
    plot_results(results, f'Выполнение привычек за {title}')

# Закрытие соединения с базой данных
conn.close()
