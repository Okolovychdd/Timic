import sqlite3

# Ініціалізація бази даних
def init_db():
    conn = sqlite3.connect('teammates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, user_id INTEGER, platform TEXT, game TEXT, language TEXT, skill_level INTEGER)''')
    conn.commit()
    conn.close()

# Збереження даних користувача
def save_user_data(user_id, platform, game, language, skill_level):
    conn = sqlite3.connect('teammates.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (user_id, platform, game, language, skill_level) VALUES (?, ?, ?, ?, ?)",
              (user_id, platform, game, language, skill_level))
    conn.commit()
    conn.close()

# Отримання товаришів для гри за параметрами
def get_teammates(platform, game, language, skill_level):
    conn = sqlite3.connect('teammates.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE platform=? AND game=? AND language=? AND skill_level=?",
              (platform, game, language, skill_level))
    teammates = c.fetchall()
    conn.close()
    return teammates

# Отримання товариша за ID
def get_teammate_by_id(teammate_id):
    conn = sqlite3.connect('teammates.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (teammate_id,))
    teammate = c.fetchone()
    conn.close()
    return teammate

import sqlite3

# Ініціалізація бази даних
def init_db():
    conn = sqlite3.connect('teammates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, user_id INTEGER, platform TEXT, game TEXT, language TEXT, skill_level INTEGER)''')
    conn.commit()
    conn.close()

# Збереження профілю користувача
def save_profile(user_id, platform, game, language, skill_level):
    conn = sqlite3.connect('teammates.db')
    c = conn.cursor()
    # Якщо профіль уже існує, оновимо його, інакше додамо новий
    c.execute('''INSERT OR REPLACE INTO users (user_id, platform, game, language, skill_level) 
                 VALUES (?, ?, ?, ?, ?)''', (user_id, platform, game, language, skill_level))
    conn.commit()
    conn.close()

# Отримання профілю користувача
def get_user_profile(user_id):
    conn = sqlite3.connect('teammates.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user_profile = c.fetchone()
    conn.close()
    return user_profile

# Пошук товаришів для гри
def find_teammates(platform, game, language, skill_level):
    conn = sqlite3.connect('teammates.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users 
                 WHERE platform=? AND game=? AND language=? AND skill_level=?''',
                 (platform, game, language, skill_level))
    teammates = c.fetchall()
    conn.close()
    return teammates
