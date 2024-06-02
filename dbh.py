import sqlite3

db = sqlite3.connect("data.db")
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS data (key TEXT, value TEXT)""")
db.commit()

# ссылка_на_канал @fletpentest
# ссылка_на_владельца @fletwix502
# ссылка_на_отзывы @fletpentest
# ссылка_на_вопросы_и_ответы @fletpentest

cursor.execute(f'INSERT INTO data (key, value) VALUES ("ссылка_на_канал", "fletpentest")')
cursor.execute(f'INSERT INTO data (key, value) VALUES ("ссылка_на_владельца", "fletwix502")')
cursor.execute(f'INSERT INTO data (key, value) VALUES ("ссылка_на_отзывы", "fletpentest")')
cursor.execute(f'INSERT INTO data (key, value) VALUES ("ссылка_на_вопросы_и_ответы", "fletpentest")')

cursor.execute(f'INSERT INTO data (key, value) VALUES ("kross", "3")')
cursor.execute(f'INSERT INTO data (key, value) VALUES ("winterkros", "4")')
cursor.execute(f'INSERT INTO data (key, value) VALUES ("hood", "3")')
cursor.execute(f'INSERT INTO data (key, value) VALUES ("futbolk", "1.5")')
cursor.execute(f'INSERT INTO data (key, value) VALUES ("puhoviki", "6.5")')
cursor.execute(f'INSERT INTO data (key, value) VALUES ("summal", "4")')
cursor.execute(f'INSERT INTO data (key, value) VALUES ("sumbol", "5.5")')
cursor.execute('INSERT INTO data (key, value) VALUES ("курс_юаня", "14")')
cursor.execute('INSERT INTO data (key, value) VALUES ("цена_за_килограмм", "540")')
cursor.execute('INSERT INTO data (key, value) VALUES ("цена_СДЭК_Москва", "250")')
cursor.execute('INSERT INTO data (key, value) VALUES ("цена_центральный_регион", "350")')
cursor.execute('INSERT INTO data (key, value) VALUES ("цена_другие_регионы", "450")')
cursor.execute('INSERT INTO data (key, value) VALUES ("цена_самовывоз", "0")')
cursor.execute('INSERT INTO data (key, value) VALUES ("город_самовывоза", "Махачкала")')
cursor.execute('INSERT INTO data (key, value) VALUES ("доставка_по_китаю", "0")')
cursor.execute('INSERT INTO data (key, value) VALUES ("доставка_до_москвы", "1599")')
cursor.execute('INSERT INTO data (key, value) VALUES ("процент_страховки", "4")')
cursor.execute('INSERT INTO data (key, value) VALUES ("комиссия_сервиса", "790")')
cursor.execute('INSERT INTO data (key, value) VALUES ("процент_предоплаты", "50")')
db.commit()