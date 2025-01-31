# IMEI Checker API & Telegram Bot

Этот проект представляет собой систему для проверки IMEI устройств. Включает **FastAPI** для API-запросов и **Telegram-бота** для удобной проверки.

## 🚀 Установка и запуск

### 1️⃣ Установить зависимости
```bash
pip install -r requirements.txt
```

### 2️⃣ Настроить `.env`
- Переименуйте `.env.example` в `.env` и укажите нужные параметры:
```ini
DATABASE_URL="your-database-url-sqlite"
TOKEN_BOT="your-telegram-bot-token"
SECRET_KEY="your-jwt-secret"
ALGORITHM="your-algorithm"
API_KEY_IMEI="your-api-key"
```

### 3️⃣ Запустить приложение
```bash
python start.py
```
- **Backend** запустится на [`http://localhost:8000`](http://localhost:8000)
- **Telegram-бот** будет использовать ваш `TOKEN_BOT`

---

## 📡 API Методы

### 🔹 Авторизация
**1. Регистрация**
```http
POST /api/auth/register
```
**2. Логин (получение токенов)**
```http
POST /api/token
```
**3. Обновление access токена**
```http
POST /api/auth/refresh
```
**4. Выход**
```http
POST /api/auth/logout
```

### 🔹 Проверка IMEI
**Метод:**  
```http
POST /api/check-imei
```
**Требуется авторизация Bearer <key>!**  
Пример запроса:
```json
{
  "imei": "354190023896443",
}
```

---

## 🤖 Команды Telegram-бота
| Команда      | Описание                                  |
|-------------|------------------------------------------|
| `/start`     | Приветственное сообщение               |
| `/imei <IMEI>` | Проверить устройство по IMEI           |
| `/add_wl <ID>` | Добавить пользователя в белый список для админа |

Админы добавляются в tg_bot/config.py

---

## 📂 Структура проекта
```
📂 backend/
 ┣ 📂 routers/           # Эндпоинты API
 ┣ 📂 database.py        # Подключение к базе данных
 ┣ 📄 main.py            # Запуск FastAPI
 ┣ 📄 utils.py           # Доп функции
 ┗ 📄 config.py          # Настройка FastAPI

📂 services/             # Логика работы с API IMEI Check

📂 tg_bot/
 ┣ 📂 handlers/          # Обработчики команд
 ┣ 📄 main.py            # Запуск бота
 ┗ 📄 config.py          # Настройки бота

📂 tests/                # Тесты
📄 start.py              # Главный файл запуска
📄 requirements.txt      # Зависимости
📄 .env.example          # Пример конфига
```

---

## 🛠 Поддержка и Контакты
Если у вас возникли вопросы, свяжитесь со мной в Telegram: `@red0core`.
