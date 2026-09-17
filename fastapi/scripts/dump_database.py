import sqlite3
import security.hash as hs
import os

if os.path.exists("database.db"):
    os.remove("database.db")

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")
cursor.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL UNIQUE,  name TEXT NOT NULL UNIQUE, email TEXT NOT NULL, hash_password TEXT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS predict (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, intent TEXT NOT NULL, owner_id INTEGER NOT NULL, FOREIGN KEY (owner_id) REFERENCES user(id))")

cursor.execute(f"INSERT INTO user (login, name, email, hash_password) VALUES ('admin', 'Administrador', 'admin@admin.com.br', '{hs.hash_password('admin')}')")
cursor.execute(f"INSERT INTO user (login, name, email, hash_password) VALUES ('teste01', 'Teste 01', 'teste01@email.com.br', '{hs.hash_password('123')}')")
cursor.execute(f"INSERT INTO user (login, name, email, hash_password) VALUES ('teste02', 'Teste 02', 'teste02@email.com.br', '{hs.hash_password('123')}')")

cursor.execute("INSERT INTO predict (text, intent, owner_id) VALUES ('Meu pedido não chegou', 'reclamacao', 1)")
cursor.execute("INSERT INTO predict (text, intent, owner_id) VALUES ('Quero cancelar minha compra', 'cancelamento', 1)")
cursor.execute("INSERT INTO predict (text, intent, owner_id) VALUES ('Qual o prazo de entrega?', 'informacao', 2)")
cursor.execute("INSERT INTO predict (text, intent, owner_id) VALUES ('Quanto ficará o valor da entrega?', 'informacao', 2)")

conn.commit()
conn.close()