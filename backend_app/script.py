import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('backend_app.db')
cursor = conn.cursor()

# 准备数据
data_to_insert = [
    ('John', 'Doe', 30),
    ('Alice', 'Smith', 25),
    # 添加更多数据行
]

# 使用 executemany 方法插入数据
cursor.executemany('INSERT INTO Image (image, last_name, age) VALUES (?, ?, ?)', data_to_insert)

# 提交更改并关闭连接
conn.commit()
conn.close()
