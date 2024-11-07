# Task Manager Fast API

Task Manager Fast API - это простой API для управления задачами, созданный с использованием Fast API. Он обеспечивает базовые операции CRUD (создание, чтение, обновление, удаление) для задач и включает обновления в режиме реального времени при изменении статуса задачи через WebSocket.

# Функции
  
  - Регистрация и аутентификация пользователя.
  - Операции CRUD для задач (Создание, Чтение, Обновление, Удаление).
  - Обновления в реальном времени для изменения статуса задачи с помощью WebSocket.
  - Аутентификация OAuth2 для доступа к API.

# Структура проекта 
```
task_manager_fastapi/
├── app/
│   ├── alembic/
│   ├── api/
│   │   ├── endpoints/
│   │   ├── middleware/
│   │   ├── models/
│   ├── core/
│   ├── db/
├── tests/
├── .env
├── .gitignore
├── alembic.ini
├── README.md
├── main.py
├── requirements.txt
```


app: Содержит основной код приложения.
    alembic: файлы миграции базы данных (если используются).
    api: содержит конечные точки API для задач и пользователей.
        endpoints: конечные точки API задач и пользователей.
        middleware: Пользовательское промежуточное программное обеспечение (например, простое ведение журнала).
        models: Pydantic модели.
    core: Основные утилиты и конфигурации.
    db: Конфигурация и модели базы данных.
.env: Сохранение переменных среды (например, учетные данные базы данных).
.gitignore: список файлов и каталогов, которые будут игнорироваться системой контроля версий.
alembic.ini: Конфигурация перегонного куба (если используется).
README.md: Документация о проекте.

# Конечные точки API

 - API предоставляет следующие конечные точки:
 - POST /api/v1/users/register/: Зарегистрируйте нового пользователя.
 - POST /api/v1/users/login/: Аутентификация и получение токена JWT.
 - GET /api/v1/about_me/: Получить информацию о пользователе (защищенная конечная точка).
 - GET /api/v1/tasks/: Получить список задач (защищенная конечная точка).
 - POST /api/v1/tasks/: создать новую задачу (защищенную конечную точку).
 - GET /api/v1/tasks/{task_id}: получить конкретную задачу (защищенную конечную точку).
 - PUT /api/v1/tasks/{task_id}: обновить конкретную задачу (защищенную конечную точку).
 - DELETE /api/v1/tasks/{task_id}: удалить определенную задачу (защищенную конечную точку).

