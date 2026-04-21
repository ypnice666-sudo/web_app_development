-- database/schema.sql
-- 任務管理系統的資料庫定義
-- 這個腳本可以透過 sqlite3 命令列或在 Python 起始化時執行以準備好環境。

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    is_completed INTEGER NOT NULL DEFAULT 0,
    due_date TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
