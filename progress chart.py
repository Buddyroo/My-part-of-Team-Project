import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sqlite3
from datetime import datetime, timedelta
import numpy as np


def fetch_progress_data(period):
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    today = datetime.now().date()

    if period == 'week':
        start_date = today - timedelta(days=today.weekday())  # Понедельник текущей недели
        end_date = start_date + timedelta(days=6)
    elif period == 'month':
        start_date = today.replace(day=1)  # Первый день текущего месяца
        end_date = today

    cur.execute('''
        SELECT h.id, h.name, uh.frequency_name, uh.frequency_count, 
               IFNULL(SUM(uhh.mark_count), 0) as total_done
        FROM habit h
        JOIN user_habit uh ON h.id = uh.habit_id
        LEFT JOIN user_habit_history uhh ON h.id = uhh.habit_id AND uhh.mark_date BETWEEN ? AND ?
        WHERE uh.active = 1
        GROUP BY h.id
    ''', (start_date, end_date))

    habits = cur.fetchall()
    conn.close()

    results = {}
    for habit in habits:
        habit_id, name, freq_name, freq_count, total_done = habit
        if freq_name == 'ежедневно':
            target = (end_date - start_date).days * freq_count
        elif freq_name == 'еженедельно' and period == 'week':
            target = freq_count
        elif freq_name == 'еженедельно' and period == 'month':
            target = 4 * freq_count  # Предполагаем 4 полные недели в месяце
        elif freq_name == 'ежемесячно':
            target = freq_count

        percentage_done = (total_done / target) * 100 if target != 0 else 0
        results[name] = {'percentage_done': percentage_done, 'total_done': total_done, 'target': target}

    return results, start_date, end_date


def plot_progress_chart(period):
    data, start_date, end_date = fetch_progress_data(period)
    names = list(data.keys())
    percentages = [data[name]['percentage_done'] for name in names]

    fig, ax = plt.subplots(figsize=(10, max(5, len(names) * 0.8)))  # Увеличиваем высоту фигуры

    bar_height = 0.1  # Фиксированная ширина столбцов
    y_positions = np.arange(0.15, 0.15 + len(names) * 0.2, 0.2)

    print("Размеры массивов:")
    print("y_positions:", len(y_positions))
    print("[100] * len(names):", len([100] * len(names)))
    print("percentages:", len(percentages))

    goals = ax.barh(y_positions, [100] * len(names), color='silver', label='Цель', height=bar_height)
    progress_bars = ax.barh(y_positions, percentages, color='darksalmon', label='Фактический прогресс', height=bar_height)

    ax.set_yticks([y for y in y_positions])  # Центрируем названия привычек

    ax.invert_yaxis()  # Начинаем снизу
    ax.set_xlabel('Процент выполнения', color = "dimgray", fontweight='bold')
    ax.set_title(
        f'Прогресс выполнения привычек за {"неделю" if period == "week" else "месяц"} с {start_date} по {end_date}',pad =20, color = "dimgray", fontweight='bold', fontsize = 14)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
    legend = ax.legend(loc='upper right')  # Перемещаем легенду в правый верхний угол
    for text in legend.get_texts():
        text.set_color('dimgray')  # Change the color of legend text
        text.set_fontweight('bold')

    # Добавляем вертикальные линии и меняем цвет осей
    major_ticks = np.arange(0, 101, 20)
    for mtick in major_ticks:
        ax.axvline(x=mtick, color='silver', linestyle='--', linewidth=0.5)  # Линии на основных тиках

    # Изменение цветов осей и тиков
    ax.spines['bottom'].set_color('silver')
    ax.spines['top'].set_color('silver')
    ax.spines['right'].set_color('silver')
    ax.spines['left'].set_color('silver')
    ax.tick_params(axis='both', colors='silver')  # Меняем цвет тиков

    ax.set_yticklabels(names, color="dimgray", fontweight='bold')  # Устанавливаем названия привычек

    # Расширяем ось X для дополнительного пространства
    ax.set_xlim(0, 100)
    # Set Y-axis height to be 0.5 units above the last bar
    ax.set_ylim(0, y_positions[-1] + 0.5)

    # Adding text inside the progress bars
    for bar, percentage in zip(progress_bars, percentages):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{percentage:.1f}%', ha='right', va='center',
                color='dimgrey', fontweight='bold')
        # Adding text inside the bars
    for bar, goal in zip(goals, [100] * len(names)):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, '100%', ha='right', va='center', color='dimgrey', fontweight='bold')

        # Adjust the margins
        plt.subplots_adjust(top=0.85, bottom=0.15)  # Fine-tune the subplot margins

        # Сохраняем график
    fig.savefig(os.path.join(save_path, f'progress_chart_{period}.png'))

    plt.show()


# Пример вызова функции
plot_progress_chart('week')
plot_progress_chart('month')