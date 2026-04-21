import sqlite3
import os

# 此處預設將資料庫存在頂層 instance 資料夾中
# 為了避免找不到路徑，這裡可以用相對絕對路徑抓取
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'database.db')

# 確保 instance 資料夾存在
os.makedirs(INSTANCE_DIR, exist_ok=True)

def get_db_connection():
    """建立資料庫連線並回傳 Row 格式的結果"""
    conn = sqlite3.connect(DB_PATH)
    # 將回傳結果設為 sqlite3.Row，讓資料可以用 dict 的方式取用 (ex: row['title'])
    conn.row_factory = sqlite3.Row
    return conn

class TaskModel:
    """負責處理 task 資料表 CRUD 的 Model 層"""

    @classmethod
    def get_all(cls):
        """讀取所有的任務，以狀態及時間排序 (未完成及近期優先)"""
        conn = get_db_connection()
        # 把未完成的 (is_completed=0) 擺前面
        # 再依照 due_date 排序（空值會被排到後面因為 ASC 特性，不過 SQLite 對空值排序比較不一定，可以後續改進，目前夠用）
        tasks = conn.execute(
            'SELECT * FROM tasks ORDER BY is_completed ASC, due_date ASC, created_at DESC'
        ).fetchall()
        conn.close()
        return [dict(task) for task in tasks]

    @classmethod
    def get_by_id(cls, task_id):
        """根據特定的 ID 取回單一一筆資料"""
        conn = get_db_connection()
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        if task:
            return dict(task)
        return None

    @classmethod
    def create(cls, title, description='', due_date=None):
        """新增一筆任務並回傳該筆資料的 ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)',
            (title, description, due_date)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @classmethod
    def update(cls, task_id, title, description, due_date):
        """依據 ID 編輯更新特定的任務細節"""
        conn = get_db_connection()
        conn.execute(
            'UPDATE tasks SET title = ?, description = ?, due_date = ? WHERE id = ?',
            (title, description, due_date, task_id)
        )
        conn.commit()
        conn.close()
        return True

    @classmethod
    def toggle_status(cls, task_id):
        """切換狀態: 若已完成則變未完成、若未完成則變完成"""
        task = cls.get_by_id(task_id)
        if not task:
            return False
            
        new_status = 1 if task['is_completed'] == 0 else 0
        
        conn = get_db_connection()
        conn.execute(
            'UPDATE tasks SET is_completed = ? WHERE id = ?',
            (new_status, task_id)
        )
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, task_id):
        """根據 ID 刪除任務"""
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        return True
