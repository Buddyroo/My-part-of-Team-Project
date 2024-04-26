import sqlite3
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from datetime import datetime, timedelta
import os

def fetch_data():
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())

    # Выборка активных привычек
    cur.execute('''
        SELECT h.id, uh.frequency_count, h.name, uh.frequency_name
        FROM user_habit uh
        JOIN habit h ON uh.habit_id = h.id
        WHERE uh.active = 1
    ''')
    habits = cur.fetchall()

    data = {habit[0]: {'name': habit[2], 'goal': habit[1], 'frequency': habit[3], 'actuals': 0,
                       'dates': [(start_of_week + timedelta(days=i)).isoformat() for i in
                                 range((today - start_of_week).days + 1)]} for habit in habits}

    # Получаем историю выполнения для каждой привычки
    for habit_id in data:
        cur.execute('''
            SELECT SUM(mark_count)
            FROM user_habit_history
            WHERE habit_id = ? AND mark_date BETWEEN ? AND ?
        ''', (habit_id, start_of_week, today))
        result = cur.fetchone()
        data[habit_id]['actuals'] = result[0] if result[0] is not None else 0

    conn.close()
    return data

def plot_data(data):
    os.makedirs('saved_charts', exist_ok=True)

    # Сначала создаем график выполнения привычек
    names = [info['name'] for info in data.values()]
    percentages = [100 * info['actuals'] / info['goal'] if info['goal'] > 0 else 0 for info in data.values()]

    fig, ax = plt.subplots()
    ax.bar(names, percentages, color='lightblue')
    ax.set_xlabel('Привычка')
    ax.set_ylabel('Процент выполнения')
    ax.set_title('Процент выполнения привычек за текущую неделю')
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_locator(MultipleLocator(10))
    plt.xticks(rotation=45)
    plt.tight_layout()  # Улучшает отображение подписей
    plt.savefig('saved_charts/percentage_completion.png', format='png')
    plt.show()

    # Теперь показываем исходные графики выполнения
    for habit_id, info in data.items():
        fig, ax = plt.subplots()
        x = range(len(info['dates']))
        width = 0.35

        ax.bar(x, [info['goal']] * len(info['dates']), width, label='Цель', color='silver', align='center')
        ax.bar([p + width for p in x], [info['actuals']] * len(info['dates']), width, label='Выполнено', color='darksalmon', align='center')

        ax.set_xlabel('Дата')
        ax.set_ylabel('Количество выполнений')
        ax.set_title(f'Выполнение привычки: "{info["name"]}" за эту неделю')
        ax.set_xticks([p + width / 2 for p in x])
        ax.set_xticklabels(info['dates'], rotation=20)
        ax.set_ylim(0, max(info['goal'], info['actuals']) + 3)
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.legend()

        file_path = f'saved_charts/{habit_id}_{info["name"].replace(" ", "_")}.png'
        plt.savefig(file_path, format='png')
        plt.close(fig)

# Запускаем функции
data = fetch_data()
plot_data(data)
