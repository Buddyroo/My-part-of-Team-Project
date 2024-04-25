import matplotlib.pyplot as plt

# Данные: цели и фактические выполнения за каждый день недели
days = ['1', '2', '3', '4', '5', '6', '7']
goals = [7, 7, 7, 7, 7, 7, 7]  # Цели за каждый день (пример)
actuals = [5, 6, 7, 3, 5, 7, 6]  # Фактическое выполнение

# Создание фигуры и осей
fig, ax = plt.subplots()

# Определение положения столбцов на оси X
x = range(len(days))
width = 0.35  # Ширина столбцов

# Создание столбцов
ax.bar(x, goals, width, label='Цель', color='silver', align='center')
ax.bar([p + width for p in x], actuals, width, label='Выполнено', color='darksalmon', align='center')

# Добавление заголовка и меток
ax.set_xlabel('Дни недели')
ax.set_ylabel('Количество выполнений')
ax.set_title('Выполнение привычек за неделю')
ax.set_xticks([p + width / 2 for p in x])
ax.set_xticklabels(days)
ax.set_ylim(0, 10)  # Максимальное значение по оси Y

# Добавление легенды
ax.legend()

# Показать график
plt.show()