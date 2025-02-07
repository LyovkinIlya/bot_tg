import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

# Создание таблицы:
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# Заполнение таблицы 10 записями:
# for i in range(1, 11):
#     cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
#                    (f"User{i}", f"example{i}@gmail.com", i * 10, 1000))

# Обновление баланса у каждой 2-й записи начиная с 1-й на 500:
# for j in range(1, 11, 2):
#     cursor.execute("UPDATE Users SET balance = ? WHERE id = ?", (500, j))

# Удаление каждой 3-й записи, начиная с 1-й:
# for k in range(1, 11, 3):
#     cursor.execute("DELETE FROM Users WHERE id = ?", (k,))

# Выборка, где возраст не равен 60:
# cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
# users = cursor.fetchall()
# for user in users:
#     print(f"Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}")

# Удаление из бд запись с id = 6:
cursor.execute("DELETE FROM Users WHERE id = 6")

# Подсчёт общего кол-ва всех пользователей:
cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]

# Подсчёт суммы всех балансов:
cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]

#Средний баланс всех пользователей:
print(all_balances / total_users)
# Или через AVG:
cursor.execute("SELECT AVG(balance) FROM Users")
avg_balance = cursor.fetchone()[0]
print(avg_balance)

connection.commit()
connection.close()