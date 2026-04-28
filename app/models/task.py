import sqlite3
import os
from flask import current_app

def get_db_connection():
    """
    建立與資料庫的連線。
    預設連接到 current_app.config['DATABASE'] 或 instance/database.db。
    設定 row_factory = sqlite3.Row 以字典方式存取資料。
    """
    try:
        # 嘗試從 app.config 取得資料庫路徑，若無則使用預設值
        if current_app:
            db_path = current_app.config.get('DATABASE', 'instance/database.db')
        else:
            db_path = 'instance/database.db'
            
        # 確保資料夾存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"資料庫連線錯誤: {e}")
        return None
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")
        return None

def create(data):
    """
    新增一筆任務記錄。
    
    參數:
        data (dict): 包含 title, description, due_date 等資訊
        
    回傳:
        int: 新增的任務 ID，若失敗則回傳 None
    """
    conn = get_db_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)',
            (data.get('title'), data.get('description'), data.get('due_date'))
        )
        conn.commit()
        last_row_id = cursor.lastrowid
        return last_row_id
    except sqlite3.Error as e:
        print(f"新增任務錯誤: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_all():
    """
    取得所有任務記錄，依據建立時間降序排序（越新的在越前面）。
    
    回傳:
        list[sqlite3.Row]: 任務列表
    """
    conn = get_db_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"取得任務列表錯誤: {e}")
        return []
    finally:
        conn.close()

def get_by_id(task_id):
    """
    取得單筆任務記錄。
    
    參數:
        task_id (int): 任務 ID
        
    回傳:
        sqlite3.Row: 任務物件，若找不到或錯誤則回傳 None
    """
    conn = get_db_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"取得單筆任務錯誤: {e}")
        return None
    finally:
        conn.close()

def update(task_id, data):
    """
    更新任務記錄。
    
    參數:
        task_id (int): 任務 ID
        data (dict): 包含欲更新的欄位與值，可包含 title, description, is_completed, due_date
        
    回傳:
        bool: 是否更新成功
    """
    conn = get_db_connection()
    if not conn:
        return False
        
    # 動態產生 UPDATE 語句
    set_clause = []
    values = []
    
    for key in ['title', 'description', 'is_completed', 'due_date']:
        if key in data:
            set_clause.append(f"{key} = ?")
            values.append(data[key])
            
    if not set_clause:
        return False
        
    values.append(task_id)
    query = f"UPDATE tasks SET {', '.join(set_clause)} WHERE id = ?"
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"更新任務錯誤: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def delete(task_id):
    """
    刪除任務記錄。
    
    參數:
        task_id (int): 任務 ID
        
    回傳:
        bool: 是否刪除成功
    """
    conn = get_db_connection()
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"刪除任務錯誤: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
