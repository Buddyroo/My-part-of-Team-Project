import sqlite3
def add_info():
    conn = sqlite3.connect('easy_habit.db')
    cur = conn.cursor()
    #cur.execute("INSERT INTO user (id, creation_date) VALUES (?,?)",
               # (1111111111, '2024-04-22'))

    #cur.execute("INSERT INTO habit (name, description) VALUES (?,?)",
                  #('Память','Необходимо петь'))
    #
    #cur.execute("INSERT INTO user_habit (user_id, habit_id, active, frequency_name, frequency_count) "
                  #"VALUES (?,?, ?, ?, ?)", (1111111111, 5, 1, 'ежемесячно', 4))
    # #
    #cur.execute("INSERT INTO user_habit_history "
                 # "(user_id, habit_id, mark_date, mark_count)"
                # "VALUES (?, ?, ?, ?)", (1111111111, 5, '2024-04-22', 1))
    #
    #cur.execute("INSERT INTO user_habit_history "
     #             "(user_id, habit_id, mark_date, mark_count)"
      #            "VALUES (?, ?, ?, ?)", (1111111111,5, '2024-04-17',3))

    cur.execute("DELETE FROM user_habit_history "
                "WHERE user_id= ? AND habit_id = ?",
                 (1111111111, 3))
    # #
    # cur.execute("INSERT INTO user_habit_history "
    #             "(user_id, habit_id, mark_date, mark_count)"
    #              "VALUES (?, ?, ?, ?)", (1111111111, 3, '2024-04-18', 3))

    #cur.execute("UPDATE user_habit_history SET mark_count = ? WHERE user_id = ? AND habit_id = ? AND mark_date = ?",

               # (7, 1111111111, 2, '2024-04-25'))

    #cur.execute("UPDATE user_habit SET frequency_name = ? WHERE user_id = ? AND habit_id = ?",

     #            ('ежедневно', 1111111111, 3))

    #cur.execute("UPDATE user_habit_history SET mark_count = ? WHERE user_id = ? AND habit_id = ? AND mark_date = ?",
#
             #   (6, 1111111111, 2, '2024-04-24'))

    conn.commit()
    conn.close()

add_info()