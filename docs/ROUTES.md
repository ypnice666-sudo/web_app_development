# 任務管理系統 - 路由設計文件 (ROUTES)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 瀏覽任務列表 | GET | / | templates/index.html | 顯示所有任務，包含狀態與即將到期提示 |
| 新增任務頁面 | GET | /task/new | templates/form.html | 顯示新增任務的表單 |
| 建立任務 | POST | /task/new | — | 接收表單，存入 DB，重導向至 / |
| 編輯任務頁面 | GET | /task/<int:id>/edit | templates/form.html | 顯示編輯任務的表單，預填現有資料 |
| 更新任務 | POST | /task/<int:id>/edit | — | 接收表單，更新 DB，重導向至 / |
| 刪除任務 | POST | /task/<int:id>/delete | — | 刪除指定任務後重導向至 / |
| 標記完成狀態 | POST | /task/<int:id>/toggle | — | 切換特定任務的完成/未完成狀態，重導向至 / |

## 2. 每個路由的詳細說明

### `GET /` (瀏覽任務列表)
- **輸入**: 無
- **處理邏輯**: 呼叫 Model 取得所有任務清單。
- **輸出**: 渲染 `index.html` 模板，傳遞任務資料。
- **錯誤處理**: 無特殊錯誤。

### `GET /task/new` (新增任務頁面)
- **輸入**: 無
- **處理邏輯**: 準備空的任務資料供表單使用。
- **輸出**: 渲染 `form.html` 模板。
- **錯誤處理**: 無特殊錯誤。

### `POST /task/new` (建立任務)
- **輸入**: 表單資料 (`title`, `description`, `due_date`)
- **處理邏輯**: 驗證資料後呼叫 Model 執行新增操作。
- **輸出**: 成功後重導向至 `/`。
- **錯誤處理**: 資料驗證失敗（如標題為空）則重新渲染 `form.html` 並顯示錯誤訊息。

### `GET /task/<int:id>/edit` (編輯任務頁面)
- **輸入**: URL 參數 `id`
- **處理邏輯**: 呼叫 Model 查詢指定任務資料。
- **輸出**: 若任務存在，渲染 `form.html` 模板，並預填任務資料。
- **錯誤處理**: 若 `id` 不存在，回傳 404 Not Found 或重導向並顯示錯誤訊息。

### `POST /task/<int:id>/edit` (更新任務)
- **輸入**: URL 參數 `id`，表單資料 (`title`, `description`, `due_date`)
- **處理邏輯**: 驗證資料後呼叫 Model 執行更新操作。
- **輸出**: 成功後重導向至 `/`。
- **錯誤處理**: 若 `id` 不存在回傳 404；驗證失敗則重新渲染 `form.html` 並顯示錯誤訊息。

### `POST /task/<int:id>/delete` (刪除任務)
- **輸入**: URL 參數 `id`
- **處理邏輯**: 呼叫 Model 執行刪除操作。
- **輸出**: 成功後重導向至 `/`。
- **錯誤處理**: 若 `id` 不存在，回傳 404 或忽略。

### `POST /task/<int:id>/toggle` (標記完成狀態)
- **輸入**: URL 參數 `id`
- **處理邏輯**: 呼叫 Model 切換該任務的 `is_completed` 狀態。
- **輸出**: 成功後重導向至 `/`。
- **錯誤處理**: 若 `id` 不存在，回傳 404 或忽略。

## 3. Jinja2 模板清單

- `templates/base.html`: 頁面共用架構（包含 HTML 骨架、導覽列、載入 CSS/JS）。
- `templates/index.html`: 首頁，繼承 `base.html`，用於顯示任務清單總覽與任務狀態切換。
- `templates/form.html`: 新增與編輯任務共用的表單視圖，繼承 `base.html`。

## 4. 路由骨架程式碼

路由的骨架程式碼將實作於 `app/routes/task_routes.py`，請參考該檔案的 docstring 與函式定義。
