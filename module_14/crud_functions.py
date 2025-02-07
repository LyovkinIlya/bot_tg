import sqlite3

connection = sqlite3.connect("products.db")
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
        );
    ''')
    connection.commit()

# Добавление продуктов в таблицу:
# for i in range(1, 5):
#     prod = [product1, product2, product3, product4]
#     p_p_p = [pieces_per_pack1, pieces_per_pack2, pieces_per_pack3, pieces_per_pack4]
#     cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
#                    (prod[i-1], p_p_p[i-1], f'{i * 100}'))

def get_all_products():
    cursor.execute("SELECT * FROM Products")
    return cursor.fetchall()

if __name__ == '__main__':
    initiate_db()
    connection.close()