import sqlite3

connection = sqlite3.connect("products_5.db")
cursor = connection.cursor()

# Название и описание товара:
product1 = "Аскорбинка с глюкозой"
pieces_per_pack1 = "10"
product2 = "Аскорбиновая кислота"
pieces_per_pack2 = "200"
product3 = "Аскорбинка детская"
pieces_per_pack3 = "10"
product4 = "Витамин С"
pieces_per_pack4 = "20"

def initiate_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
        )
    ''')
    connection.commit()

def get_all_products():
    cursor.execute("SELECT * FROM Products")
    return cursor.fetchall()

def add_user(username, email, age, balance=1000):
    cursor.execute(
       'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
        (username, email, age, balance)
       )
    connection.commit()

def is_included(username):
    check_user = cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if check_user.fetchone() is None:
        return False
    else:
        return True



if __name__ == '__main__':
    initiate_db()
    connection.close()