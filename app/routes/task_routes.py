from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models import task as task_model

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
    tasks = task_model.get_all()
    return render_template('index.html', tasks=tasks)

@task_bp.route('/task/new', methods=['GET'])
def new_task():
    """
    新增任務頁面
    輸入: 無
    處理邏輯: 準備空資料供表單使用。
    輸出: 渲染 form.html 模板。
    """
    return render_template('form.html', task={}, action='新增任務')

@task_bp.route('/task/new', methods=['POST'])
def create_task():
    """
    建立任務
    輸入: 表單資料 (title, description, due_date)
    處理邏輯: 驗證資料後呼叫 Model 執行新增操作。
    輸出: 成功後重導向至 /
    """
    title = request.form.get('title')
    description = request.form.get('description')
    due_date = request.form.get('due_date')

    if not title or not title.strip():
        flash('任務標題為必填欄位！', 'error')
        return render_template('form.html', task={
            'title': title,
            'description': description,
            'due_date': due_date
        }, action='新增任務')

    task_data = {
        'title': title.strip(),
        'description': description.strip() if description else '',
        'due_date': due_date.strip() if due_date else ''
    }

    new_id = task_model.create(task_data)
    if new_id:
        flash('任務新增成功！', 'success')
        return redirect(url_for('task.index'))
    else:
        flash('任務新增失敗，請稍後再試。', 'error')
        return render_template('form.html', task=task_data, action='新增任務')

@task_bp.route('/task/<int:id>/edit', methods=['GET'])
def edit_task(id):
    """
    編輯任務頁面
    輸入: URL 參數 id
    處理邏輯: 呼叫 Model 查詢指定任務資料。
    輸出: 若任務存在，渲染 form.html 模板，並預填任務資料。若不存在回傳 404。
    """
    task = task_model.get_by_id(id)
    if not task:
        abort(404)
        
    return render_template('form.html', task=dict(task), action='編輯任務')

@task_bp.route('/task/<int:id>/edit', methods=['POST'])
def update_task(id):
    """
    更新任務
    輸入: URL 參數 id，表單資料 (title, description, due_date)
    處理邏輯: 驗證資料後呼叫 Model 執行更新操作。
    輸出: 成功後重導向至 /
    """
    task = task_model.get_by_id(id)
    if not task:
        abort(404)

    title = request.form.get('title')
    description = request.form.get('description')
    due_date = request.form.get('due_date')

    if not title or not title.strip():
        flash('任務標題為必填欄位！', 'error')
        return render_template('form.html', task={
            'id': id,
            'title': title,
            'description': description,
            'due_date': due_date
        }, action='編輯任務')

    task_data = {
        'title': title.strip(),
        'description': description.strip() if description else '',
        'due_date': due_date.strip() if due_date else ''
    }

    success = task_model.update(id, task_data)
    if success:
        flash('任務更新成功！', 'success')
        return redirect(url_for('task.index'))
    else:
        flash('任務更新失敗，請稍後再試。', 'error')
        # 把 id 加回去，否則表單可能壞掉
        task_data['id'] = id
        return render_template('form.html', task=task_data, action='編輯任務')

@task_bp.route('/task/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除任務
    輸入: URL 參數 id
    處理邏輯: 呼叫 Model 執行刪除操作。
    輸出: 成功後重導向至 /
    """
    task = task_model.get_by_id(id)
    if not task:
        abort(404)
        
    success = task_model.delete(id)
    if success:
        flash('任務刪除成功！', 'success')
    else:
        flash('任務刪除失敗，請稍後再試。', 'error')
        
    return redirect(url_for('task.index'))

@task_bp.route('/task/<int:id>/toggle', methods=['POST'])
def toggle_task(id):
    """
    標記完成狀態
    輸入: URL 參數 id
    處理邏輯: 呼叫 Model 切換該任務的 is_completed 狀態。
    輸出: 成功後重導向至 /
    """
    task = task_model.get_by_id(id)
    if not task:
        abort(404)
        
    new_status = 1 if task['is_completed'] == 0 else 0
    success = task_model.update(id, {'is_completed': new_status})
    
    if success:
        status_text = '已完成' if new_status == 1 else '未完成'
        flash(f'任務已標記為{status_text}！', 'success')
    else:
        flash('狀態切換失敗，請稍後再試。', 'error')
        
    return redirect(url_for('task.index'))
