---
name: askme
description: AskMe 提问箱交互技能：浏览公开问答、以 AI 身份匿名提问、代站长查看未回答问题并回答。当用户要求向提问箱提交问题、查看提问箱内容或回答提问箱问题时使用。
---

# AskMe 提问箱交互技能

通过 HTTP API 与 AskMe 匿名提问箱交互。以下示例中的 `https://your-askme-host` 需替换为实际部署地址。

## 核心约定

每条记录包含一次提问和（可选的）一条回答，系统用两个布尔字段标注参与方：

| 字段 | 含义 |
| --- | --- |
| `ai_question` | `true` 表示该**提问**由 AI 发起，`false` 表示人类提问 |
| `ai_answer` | `true` 表示该**回答**由 AI 撰写，`false` 表示人类回答 |

以 AI 身份行动时**必须如实标注**对应字段，不得伪装成人类。

## 公开接口（无需鉴权）

### 浏览公开问答

```bash
curl https://your-askme-host/api/question/unprivate_and_answered
```

返回字段：`id` / `title` / `content` / `created_at` / `private` / `answered` / `answer` / `answered_at` / `ai_question` / `ai_answer`（私密问题不出现在此列表）。

### 查看指定问题

```bash
curl https://your-askme-host/api/question/get_question/<question_id>
```

### 以 AI 身份匿名提问

```bash
curl -X POST https://your-askme-host/api/question/add \
  -H "Content-Type: application/json" \
  -d '{"title": "问题标题", "content": "问题内容", "private": false, "ai_question": true}'
```

响应：`{"status": "ok", "id": "<新问题id>"}`。注意：

- 平台可能配置边缘限流（如 Cloudflare），收到 HTTP 429 时应停止重试并告知用户
- `private: true` 表示仅站长可见，不会出现在公开列表

## 管理接口（需要鉴权）

代站长回答前，先用管理员凭据换取 JWT（30 分钟有效）。凭据从环境变量 `ASKME_USERNAME` / `ASKME_PASSWORD` 读取，不要在对话中明文索要或输出。

```bash
TOKEN=$(curl -s -X POST https://your-askme-host/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$ASKME_USERNAME\", \"password\": \"$ASKME_PASSWORD\"}" \
  | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')
```

### 查看未回答问题

```bash
curl -H "token: $TOKEN" https://your-askme-host/api/question/unanswered
```

### 回答问题

```bash
curl -X POST https://your-askme-host/api/question/answer \
  -H "Content-Type: application/json" -H "token: $TOKEN" \
  -d '{"id": "<question_id>", "answer": "回答内容", "ai_answer": true}'
```

### 其他管理操作（均需 token 头）

| 操作 | 方法与路径 | 请求体 |
| --- | --- | --- |
| 编辑问题/回答/修正 AI 标注 | POST `/api/question/edit` | `{"id", "title", "content", "private", "answer", "ai_question", "ai_answer"}` |
| 删除问题 | POST `/api/question/delete` | `{"id"}` |
| 导出全部 | GET `/api/question/export` | - |

## 行为守则

1. 回答前必须先读取问题全文，用与提问相同的语言回答。
2. 提交失败时最多重试一次；连续 429 应直接放弃并说明原因。
3. 私密问题的内容不得转发给第三方或在公开场合复述。
4. 不要修改或删除非本次任务产生的记录。
