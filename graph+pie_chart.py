
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from datetime import datetime, timedelta
import os
def fetch_data():
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Понедельник этой недели

    # Выборка активных ежедневных привычек
    cur.execute('''
        SELECT h.id, uh.frequency_count, h.name
        FROM user_habit uh
        JOIN habit h ON uh.habit_id = h.id
        WHERE uh.active = 1 AND uh.frequency_name = 'ежедневно'
    ''')
    habits = cur.fetchall()


    # Словарь для данных
    data = {habit[0]: {'name': habit[2], 'goal': habit[1], 'actuals': [0] * ((today - start_of_week).days + 1),
                       'dates': [(start_of_week + timedelta(days=i)).isoformat() for i in
                                 range((today - start_of_week).days + 1)]} for habit in habits}

    # Получаем историю выполнения для каждой привычки
    for habit_id in data:
        cur.execute('''
            SELECT mark_date, mark_count
            FROM user_habit_history
            WHERE habit_id = ? AND mark_date BETWEEN ? AND ?
            ORDER BY mark_date
        ''', (habit_id, start_of_week, today))
        results = cur.fetchall()
        for result in results:
            index = (datetime.strptime(result[0], '%Y-%m-%d').date() - start_of_week).days
            data[habit_id]['actuals'][index] = result[1]

    conn.close()
    return data


def plot_data(data):
    os.makedirs('saved_charts', exist_ok=True)  # Создаем папку для сохранения графиков, если ее нет

    for habit_id, info in data.items():
        fig, ax = plt.subplots()
        x = range(len(info['dates']))
        width = 0.35

        ax.bar(x, [info['goal']] * len(info['dates']), width, label='Цель', color='silver', align='center')
        ax.bar([p + width for p in x], info['actuals'], width, label='Выполнено', color='darksalmon', align='center')

        ax.set_xlabel('Дата')
        ax.set_ylabel('Количество выполнений')
        ax.set_title(f'Выполнение привычки: "{info["name"]}" за эту неделю')
        ax.set_xticks([p + width / 2 for p in x])
        ax.set_xticklabels(info['dates'], rotation=20)
        ax.set_ylim(0, info['goal'] + 3)
        fig.autofmt_xdate()
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.legend()

        # Сохраняем график в файл перед показом
        file_path = f'saved_charts/{habit_id}_{info["name"].replace(" ", "_")}.png'
        plt.savefig(file_path, format='png')
        plt.close(fig)  # Закрываем фигуру после сохранения

        # Затем отображаем график
        fig, ax = plt.subplots()
        ax.bar(x, [info['goal']] * len(info['dates']), width, label='Цель', color='silver', align='center')
        ax.bar([p + width for p in x], info['actuals'], width, label='Выполнено', color='darksalmon', align='center')
        ax.set_xlabel('Дата')
        ax.set_ylabel('Количество выполнений')
        ax.set_title(f'Выполнение привычки: "{info["name"]}" за эту неделю')
        ax.set_xticks([p + width / 2 for p in x])
        ax.set_xticklabels(info['dates'], rotation=20)
        ax.set_ylim(0, info['goal'] + 3)
        fig.autofmt_xdate()
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.legend()
        plt.show()  # Показываем график после сохранения


import matplotlib.pyplot as plt


def plot_pie_chart(data):
    fig, axs = plt.subplots(1, len(data), figsize=(15, 5))

    # Define the color palette for the charts
    colors = ['darksalmon', 'silver']  # You can choose your own colors

    for i, (habit_id, info) in enumerate(data.items()):
        total_goal = info['goal'] * len(info['dates'])  # Общая цель за весь период
        total_actuals = sum(info['actuals'])  # Считаем общее количество выполнений за период
        percentage = (total_actuals / total_goal) * 100  # Вычисляем процент выполнения цели

        # Строим круговую диаграмму
        axs[i].pie([percentage, 100 - percentage],
                   labels=[f'Выполнено: {total_actuals}', f'Осталось: {total_goal - total_actuals}'], autopct='%1.1f%%',
                   startangle=90, colors=colors)
        axs[i].set_title(info['name'])

    # Ensure the directory exists
    os.makedirs('saved_charts', exist_ok=True)

    # Save the figure
    plt.savefig('saved_charts/pie_charts.png')  # Saves the plot as a PNG file
    plt.show()  # Display the plot before closing
    plt.close(fig)  # Close the figure to free up memory

# Запускаем функции
data = fetch_data()
plot_data(data)
plot_pie_chart(data)