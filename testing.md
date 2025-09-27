# API Test Cases

This document thoroughly documents all possible test scenarios—valid, invalid, authentication, and error handling for the API. Use these with Postman, curl, or automated tests.

---

## 1. User Registration (`POST /register`)

| Test Case                | Input (JSON)                                 | Expected Status | Description                                  |
|--------------------------|----------------------------------------------|-----------------|----------------------------------------------|
| Valid registration       | `{"username":"user1","password":"pass123"}`  | 201             | Registers a new user.                        |
| Missing username         | `{"password":"pass123"}`                     | 400             | Username required error.                     |
| Missing password         | `{"username":"user1"}`                       | 400             | Password required error.                     |
| Empty username           | `{"username":"","password":"pass123"}`       | 400/409         | Empty or duplicate username error.           |
| Username already exists  | (reuse existing username)                    | 409             | Conflict error for duplicates.               |
| Invalid JSON body        | `{` (malformed)                              | 400             | JSON parse error.                            |

---

## 2. User Login (`POST /login`)

| Test Case                | Input (JSON)                                 | Expected Status | Description                                  |
|--------------------------|----------------------------------------------|-----------------|----------------------------------------------|
| Valid login              | `{"username":"user1","password":"pass123"}`  | 200             | Returns JWT access_token.                    |
| Wrong password           | `{"username":"user1","password":"bad"}`      | 400             | Error for invalid login.                     |
| Non-existent user        | `{"username":"nouser","password":"test"}`    | 400             | Error for unknown username.                  |
| Missing fields           | `{"password":"pass123"}`                     | 400             | Username required error.                     |
| Empty username/password  | `{"username":"","password":""}`              | 400             | Empty credential error.                      |
| Invalid JSON             | `{` (malformed)                              | 400             | JSON parse error.                            |

---

## 3. Create Task (`POST /tasks`) [Authentication Required]

| Test Case                | Input (JSON)                                 | Expected Status | Description                                  |
|--------------------------|----------------------------------------------|-----------------|----------------------------------------------|
| Valid creation           | `{"title":"Task1","description":"Details"}`  | 201             | Task created for user.                       |
| Title missing            | `{"description":"Details"}`                  | 400             | Title required error.                        |
| Title empty              | `{"title":"","description":"Details"}`       | 400             | Empty title error.                           |
| Description optional     | `{"title":"OnlyTitle"}`                      | 201             | Allowed without description.                 |
| Unauthorized (no token)  | -                                            | 401             | Requires authentication.                     |
| Invalid JSON format      | `{` (malformed)                              | 400             | JSON parse error.                            |

---

## 4. Get All Tasks (`GET /tasks`) [Authentication Required]

| Test Case                | Query String               | Expected Status | Description                                  |
|--------------------------|----------------------------|-----------------|----------------------------------------------|
| All tasks                | None                       | 200             | List of user's tasks.                        |
| Filter completed true    | `?completed=true`          | 200             | Only completed tasks.                        |
| Filter completed false   | `?completed=false`         | 200             | Only incomplete tasks.                       |
| Invalid completed value  | `?completed=random`        | 400             | Bad value error.                             |
| Unauthorized             | -                          | 401             | Requires authentication.                     |

---

## 5. Get Task by ID (`GET /tasks/<id>`) [Authentication Required]

| Test Case                | URL Example          | Expected Status | Description                                  |
|--------------------------|----------------------|-----------------|----------------------------------------------|
| Valid, existing          | `/tasks/1`           | 200             | Returns requested task.                      |
| Task not found           | `/tasks/9999`        | 404             | Unknown or unauthorized task.                |
| Unauthorized             | `/tasks/1` (no token)| 401             | Requires authentication.                     |

---

## 6. Update Task (`PUT /tasks/<id>`) [Authentication Required]

| Test Case                | Input (JSON)                                 | Expected Status | Description                                  |
|--------------------------|----------------------------------------------|-----------------|----------------------------------------------|
| Valid update             | `{"title":"NewT","completed":true}`          | 200             | Task updated successfully.                   |
| Title only               | `{"title":"NewT"}`                           | 200             | Only title updated.                          |
| Completed only           | `{"completed":false}`                        | 200             | Only status updated.                         |
| No fields provided       | `{}`                                         | 400             | No updates supplied.                         |
| Invalid field types      | `{"title":123,"completed":"no"}`             | 400             | Input type error.                            |
| Task not found/not owned | Non-existent/foreign task                    | 404             | 404 if not user's task.                      |
| Unauthorized             | (no token)                                   | 401             | Requires authentication.                     |

---

## 7. Delete Task (`DELETE /tasks/<id>`) [Authentication Required]

| Test Case                | URL Example           | Expected Status | Description                                  |
|--------------------------|-----------------------|-----------------|----------------------------------------------|
| Valid delete             | `/tasks/1`            | 200             | Task deleted successfully.                   |
| Task not found/not owned | `/tasks/9999`         | 404             | 404 if not user's task.                      |
| Unauthorized             | `/tasks/1` (no token) | 401             | Requires authentication.                     |

---

## Testing & Usage Tips

- For all endpoints except `/register` and `/login`, set `Authorization: Bearer <access_token>` header.
- Use `Content-Type: raw - json` header for all requests with a body.
- Note: Replace URLs with your backend server address and port if not `localhost:5000`.

---

Feel free to modify, split, or extend these tests as your API grows!
