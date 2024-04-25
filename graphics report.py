
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def fetch_data():
    # Подключаемся к базе данных
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()

    # Определяем текущий день и начало недели (понедельник)
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Понедельник этой недели

    # Выборка активных ежедневных привычек
    cur.execute('''
        SELECT uh.id, uh.frequency_count, h.name
        FROM user_habit uh JOIN habit h ON uh.habit_id = h.id
        WHERE uh.active = 1 AND uh.frequency_name = 'ежедневно'
    ''')
    habits = cur.fetchall()

    # Словарь для данных
    data = {habit[0]: {'name': habit[2], 'goal': habit[1], 'actuals': [0]*((today - start_of_week).days + 1), 'dates': [(start_of_week + timedelta(days=i)).isoformat() for i in range((today - start_of_week).days + 1)]} for habit in habits}

    # Получаем историю выполнения для каждой привычки
    for habit_id in data:
        cur.execute('''
            SELECT mark_date, SUM(mark_count)
            FROM user_habit_history
            WHERE habit_id = ? AND mark_date BETWEEN ? AND ?
            GROUP BY mark_date
            ORDER BY mark_date
        ''', (habit_id, start_of_week, today))
        results = cur.fetchall()
        for result in results:
            index = (datetime.strptime(result[0], '%Y-%m-%d').date() - start_of_week).days
            data[habit_id]['actuals'][index] = result[1]

    conn.close()
    return data

def plot_data(data):
    for habit_id, info in data.items():
        fig, ax = plt.subplots()
        x = range(len(info['dates']))
        width = 0.35

        # Создаем столбцы для графика
        ax.bar(x, [info['goal']] * len(info['dates']), width, label='Цель', color='silver', align='center')
        ax.bar([p + width for p in x], info['actuals'], width, label='Выполнено', color='darksalmon', align='center')

        # Устанавливаем метки и заголовки
        ax.set_xlabel('Дата')
        ax.set_ylabel('Количество выполнений')
        ax.set_title(f'Выполнение привычки: {info["name"]} за эту неделю')
        ax.set_xticks([p + width / 2 for p in x])
        ax.set_xticklabels(info['dates'], rotation=45)  # Поворачиваем даты для лучшей читаемости
        ax.set_ylim(0, 10)  # Максимальное значение Y

        # Добавляем легенду
        ax.legend()

        # Показываем график
        plt.show()

# Запускаем функции
data = fetch_data()
plot_data(data)