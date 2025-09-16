# Система учета финансов

Веб-приложение для учета финансовых операций с возможностью категоризации и фильтрации.

## Функциональность

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление финансовых операций
- Категоризация операций (статусы, типы, категории, подкатегории)
- Фильтрация операций по различным параметрам
- Управление профилем пользователя

## Технологии

- **Backend**: Django REST Framework
- **Frontend**: React
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker

## Требования

- Docker
- Docker Compose

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/finance-system.git
cd finance-system
```

2. Создайте файл .env в директории infra/:
```bash
# PostgreSQL
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432

# Django
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

3. Запустите проект через Docker Compose:
```bash
cd infra
docker-compose up -d --build
```

4. Выполните миграции:
```bash
docker-compose exec backend python manage.py migrate
```

5. Соберите статические файлы:
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```

6. Создайте суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```

После этого приложение будет доступно:
- Frontend: http://localhost:8000
- API: http://localhost:8000/api/
- Admin панель: http://localhost:8000/admin/

## Структура проекта

```
foodgram/
├── backend/
│   ├── api/              # Основное приложение
│   ├── users/            # Приложение для пользователей
│   └── backend/          # Настройки Django
├── frontend/
│   ├── src/
│   │   ├── components/   # React компоненты
│   │   ├── pages/        # Страницы приложения
│   │   └── utils/        # Вспомогательные функции
│   └── package.json
└── infra/               # Docker конфигурация
```

## API Endpoints

### Авторизация
- `POST /api/auth/token/login/` - получение токена
- `POST /api/auth/token/logout/` - выход
- `POST /api/users/` - регистрация пользователя

### Пользователи
- `GET /api/users/me/` - текущий пользователь
- `PUT /api/users/me/avatar/` - обновление аватара

### Финансовые операции
- `GET /api/money-flows/` - список операций
- `POST /api/money-flows/` - создание операции
- `GET /api/money-flows/{id}/` - детали операции
- `PATCH /api/money-flows/{id}/` - обновление операции
- `DELETE /api/money-flows/{id}/` - удаление операции

### Справочники
- `GET /api/statuses/` - статусы операций
- `GET /api/types/` - типы операций
- `GET /api/categories/` - категории
- `GET /api/subcategories/` - подкатегории

## Работа с системой

1. **Регистрация**: Создайте аккаунт через форму регистрации

2. **Авторизация**: Войдите в систему, используя email и пароль

3. **Создание операции**: 
   - Нажмите "Создать запись"
   - Заполните форму (дата, тип, категория и т.д.)
   - Нажмите "Сохранить"

4. **Фильтрация**:
   - Используйте фильтры на главной странице
   - Можно фильтровать по дате, статусу, типу и категориям

5. **Управление справочниками**:
   - Доступно в выпадающем меню "Справочники"
   - Можно создавать, редактировать и удалять записи


