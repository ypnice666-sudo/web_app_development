from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

# 建立 Blueprint，若應用程式簡單也可以直接掛在 app 上，這裡用 blueprint 較好管理
task_bp = Blueprint('task', __name__)

@task_bp.route('/')
def index():
    """
    瀏覽任務列表
    輸入: 無
    處理邏輯: 呼叫 Model 取得所有任務清單。
    輸出: 渲染 index.html 模板，傳遞任務資料。
    """
    pass

@task_bp.route('/task/new', methods=['GET'])
def new_task():
    """
    新增任務頁面
    輸入: 無
    處理邏輯: 準備空資料供表單使用。
    輸出: 渲染 form.html 模板。
    """
    pass

@task_bp.route('/task/new', methods=['POST'])
def create_task():
    """
    建立任務
    輸入: 表單資料 (title, description, due_date)
    處理邏輯: 驗證資料後呼叫 Model 執行新增操作。
    輸出: 成功後重導向至 /
    """
    pass

@task_bp.route('/task/<int:id>/edit', methods=['GET'])
def edit_task(id):
    """
    編輯任務頁面
    輸入: URL 參數 id
    處理邏輯: 呼叫 Model 查詢指定任務資料。
    輸出: 若任務存在，渲染 form.html 模板，並預填任務資料。若不存在回傳 404。
    """
    pass

@task_bp.route('/task/<int:id>/edit', methods=['POST'])
def update_task(id):
    """
    更新任務
    輸入: URL 參數 id，表單資料 (title, description, due_date)
    處理邏輯: 驗證資料後呼叫 Model 執行更新操作。
    輸出: 成功後重導向至 /
    """
    pass

@task_bp.route('/task/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除任務
    輸入: URL 參數 id
    處理邏輯: 呼叫 Model 執行刪除操作。
    輸出: 成功後重導向至 /
    """
    pass

@task_bp.route('/task/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """
    標記完成狀態
    輸入: URL 參數 id
    處理邏輯: 呼叫 Model 切換該任務的 is_completed 狀態。
    輸出: 成功後重導向至 /
    """
    pass
