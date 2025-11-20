# **博客系统 - API接口文档**

**版本: 2.0**

**日期: 2025-06-16**

**修订人: System Architect**

## **1. 引言 (Introduction)**

### **1.1 概述**
本系统采用混合 API 策略：
1.  **REST API**: 用于通用数据检索（如搜索、Wagtail 内容）。
2.  **AJAX API**: 用于前端交互（如点赞、评论），通常返回 JSON 状态码或 HTML 片段。

### **1.2 基础 URL**
* **API Root**: `https://your_domain.com/`
* **Wagtail API**: `https://your_domain.com/api/v2/`

### **1.3 认证方式**
* **JWT (Json Web Token)**: 用于移动端或第三方集成。
* **Session/CSRF**: 用于浏览器端 AJAX 请求（需在 Header 中携带 `X-CSRFToken`）。

## **2. 搜索服务 API (Search Services)**

由 `apps.search` 模块提供，支持 Elasticsearch/MongoDB 混合后端。

### **2.1 全文搜索**
* **Endpoint**: `GET /api/search/`
* **视图函数**: `apps.search.api.search_api`
* **描述**: 执行高级全文搜索，支持日期过滤和排序。

| 参数名       | 类型   | 必选 | 默认值 | 描述                               |
| :----------- | :----- | :--- | :----- | :--------------------------------- |
| `q`          | string | 是   | -      | 搜索关键词                         |
| `type`       | string | 否   | `all`  | 搜索范围: `all`, `blog`, `pages`   |
| `page`       | int    | 否   | `1`    | 页码                               |
| `per_page`   | int    | 否   | `10`   | 每页数量                           |
| `start_date` | string | 否   | -      | 起始日期 (YYYY-MM-DD)              |
| `end_date`   | string | 否   | -      | 结束日期 (YYYY-MM-DD)              |
| `order_by`   | string | 否   | -      | 排序: `date`, `-date`, `relevance` |

* **响应示例 (200 OK)**:
```json
{
    "query": "wagtail",
    "total": 15,
    "page": 1,
    "per_page": 10,
    "start_date": "",
    "end_date": "",
    "order_by": "",
    "results": [
        {
            "id": 101,
            "title": "Wagtail 教程",
            "url": "/blog/wagtail-tutorial/",
            "type": "blog.BlogPage",
            "date": "2025-06-15",
            "intro": "文章简介...",
            "featured_image": {
                "id": 5,
                "title": "Cover",
                "url": "/media/images/cover.jpg"
            }
        }
    ]
}
```

### **2.2 搜索建议**

  * **Endpoint**: `GET /api/search/suggest/`
  * **视图函数**: `apps.search.api.search_suggestions_api`
  * **描述**: 根据用户输入提供热门搜索词补全。

| 参数名 | 类型 | 必选 | 描述 |
| :--- | :--- | :--- | :--- |
| `q` | string | 是 | 关键词前缀 |

  * **响应示例**:

```json
{
    "suggestions": [
        { "query": "django tutorial", "hits": 150 },
        { "query": "django models", "hits": 89 }
    ]
}
```

## **3. 博客互动 API (Blog Interactions)**

由 `apps.blog` 提供，主要用于处理文章的点赞、反应等轻量交互。

### **3.1 切换文章反应 (Toggle Reaction)**

  * **Endpoint**: `POST /blog/api/reactions/<int:page_id>/toggle/`
  * **认证**: Session (支持匿名，基于 IP/SessionKey)
  * **描述**: 用户点击点赞/鼓掌图标时调用。若已存在相同反应则取消，不同则更新。

| Body 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| `reaction_type` | int | 反应类型 ID (如 1=Like, 2=Heart) |

  * **响应示例**:



```json
{
    "success": true,
    "action": "added",  // 或 'removed', 'changed'
    "counts": {
        "1": 10,  // 反应类型ID: 数量
        "2": 5
    }
}
```

### **3.2 获取反应计数**

  * **Endpoint**: `GET /blog/api/reactions/<int:page_id>/counts/`

  * **描述**: 页面加载时获取最新的反应数据及当前用户的状态。

  * **响应示例**

```json
{
    "user_reaction": 1, // 当前用户选择的类型ID，无则null
    "reactions": [
        { "id": 1, "name": "点赞", "icon": "fa-thumbs-up", "count": 12 },
        { "id": 2, "name": "爱心", "icon": "fa-heart", "count": 5 }
    ]
}
```

## **4. 评论系统 API (Comments)**

由 `apps.comments` 提供，支持 AJAX 动态加载和提交。

### **4.1 提交评论**

  * **Endpoint**: `POST /comments/post/<int:page_id>/`
  * **认证**: `LoginRequired` (需登录)
  * **Headers**: `X-Requested-With: XMLHttpRequest`

| Body 参数 | 类型 | 必选 | 描述 |
| :--- | :--- | :--- | :--- |
| `content` | string | 是 | 评论内容 |
| `parent_id` | int | 否 | 父评论 ID (回复时使用) |
| `replied_to_user_id` | int | 否 | 被回复用户 ID |

  * **响应示例**:

```json
{
    "status": "success",
    "message": "评论已发布",
    "html": "<div class='comment'>...</div>", // 渲染好的评论 HTML 片段
    "comment_status": "approved"
}
```

### **4.2 加载评论列表**

  * **Endpoint**: `GET /comments/load/<int:page_id>/`
  * **描述**: 分页加载根评论。

| 参数 | 描述 |
| :--- | :--- |
| `page` | 页码 |
| `sort` | `hot` (热门) 或 `new` (最新) |

  * **响应**:

```json
{
    "status": "success",
    "html": "...", // 包含多条评论的 HTML
    "has_next": true,
    "total_comments": 100,
    "is_authenticated": true
}
```

### **4.3 评论点赞/踩**

  * **Endpoint**: `POST /comments/react/`
  * **认证**: `LoginRequired`

| Body 参数 | 描述 |
| :--- | :--- |
| `comment_id` | 评论 ID |
| `reaction_type` | `1` (赞) 或 `-1` (踩) |

  * **响应**:

```json
{
    "status": "success",
    "action": "added",
    "like_count": 10,
    "dislike_count": 2
}
```

### **4.4 删除/编辑评论**

  * **删除**: `POST /comments/delete/` (`comment_id`)
  * **编辑**: `POST /comments/edit/` (`comment_id`, `content`)

## **5. 认证 API (Authentication)**

基于 `djangorestframework_simplejwt`。

### **5.1 获取 Token**

  * **Endpoint**: `POST /api/token/`
  * **Body**: `{"username": "...", "password": "..."}`
  * **Response**: `{"refresh": "...", "access": "..."}`

### **5.2 刷新 Token**

  * **Endpoint**: `POST /api/token/refresh/`
  * **Body**: `{"refresh": "..."}`

## **6. 错误代码规范**

所有自定义 API 遵循以下 HTTP 状态码规范：

  * **200 OK**: 操作成功。
  * **400 Bad Request**: 参数错误（如缺少必填项、验证失败）。
  * **403 Forbidden**: 权限不足（如删除他人评论、未登录操作）。
  * **404 Not Found**: 资源不存在（如评论 ID 无效）。
  * **429 Too Many Requests**: 触发频率限制（如评论过快）。
  * **500 Internal Server Error**: 服务器内部异常。
