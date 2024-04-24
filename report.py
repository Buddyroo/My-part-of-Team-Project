import sqlite3
from datetime import datetime, timedelta

def generate_report(conn, start_date, end_date, user_id):
    data = fetch_habit_data(conn, start_date, end_date, user_id)
    report = []
    for name, frequency_count, total_marks in data:
        status = "Achieved" if total_marks >= frequency_count else "Not Achieved"
        report.append(f"Habit: {name}, Target: {frequency_count}, Completed: {total_marks}, Status: {status}")
    return report

def weekly_report(user_id):
    conn = sqlite3.connect('easy_habit.db')
    today = datetime.now().date()
    start_date = today - timedelta(days=today.weekday(), weeks=1)  # Monday of the previous week
    end_date = start_date + timedelta(days=6)  # Sunday of the previous week
    print(f"Weekly Date Range: {start_date} to {end_date}")  # Debug: print date range
    report = generate_report(conn, start_date, end_date, user_id)
    conn.close()
    return report

def monthly_report(user_id):
    conn = sqlite3.connect('easy_habit.db')
    today = datetime.now().date()
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_last_month = today.replace(day=1) - timedelta(days=1)
    print(f"Monthly Date Range: {first_day_last_month} to {last_day_last_month}")  # Debug: print date range
    report = generate_report(conn, first_day_last_month, last_day_last_month, user_id)
    conn.close()
    return report

def fetch_habit_data(conn, user_id):
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT h.name, uh.frequency_count, SUM(uhh.mark_count) as total_marks
            FROM habit h
            JOIN user_habit uh ON h.id = uh.habit_id
            JOIN user_habit_history uhh ON uh.habit_id = uhh.habit_id AND uh.user_id = uhh.user_id
            WHERE uh.user_id = ?
            GROUP BY h.name, uh.frequency_count
        ''', (user_id,))
        results = cur.fetchall()
        print("Unfiltered Query Results:", results)
    except sqlite3.Error as e:
        print("An error occurred:", e)
        results = []
    return results

# Example usage
print("Data Check:")
print(fetch_habit_data(sqlite3.connect('easy_habit.db'), 1111111111))

# Example usage
user_id = 1111111111  # Assuming we have user with ID 1111111111
print("Weekly Report:")
print(weekly_report(user_id))
print("Monthly Report:")
print(monthly_report(user_id))

