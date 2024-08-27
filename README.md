# PAWCONTROLL

## Описание проекта

Пётр и Антон решили открыть свой бизнес по выгулу собак в своем доме и разработали приложение PAWCONTROLL, через которое жильцы дома смогут направлять им заказы на выгул своих питомцев. Ваша задача как бэкенд разработчика — разработать структуру БД и реализовать REST-API для управления этими заказами.

## Требования

1. **Структура заказа:**

   - Номер квартиры
   - Кличка животного
   - Порода животного
   - Время и дата прогулки

2. **Правила прогулок:**

   - Прогулка может длиться не более получаса.
   - Прогулка может начинаться либо в начале часа, либо в половину (например, 11:00, 11:30, 12:00, 12:30 и т.д.).
   - Самая ранняя прогулка может начинаться не ранее 7:00 утра, а самая поздняя не позднее 23:00 вечера.

3. **Ограничение по прогулкам:**
   - Пётр и Антон могут гулять одновременно только с одним животным.

## API

### 1. Вывод заказов на указанную дату

- **URL:** `/orders/{date}`
- **Метод:** `GET`
- **Параметры:**
  - `date` (формат: `YYYY-MM-DD`)

**Пример запроса:**

GET /orders/2024-08-28

**Пример ответа:**

```json
[
	{
		"id": 1,
		"apartment_number": "12B",
		"pet_name": "Buddy",
		"pet_breed": "Labrador",
		"walk_date": "2024-08-28",
		"walk_time": "10:00:00",
		"created_at": "2024-08-27 16:00:39"
	}
]
```

### Сообщение об ошибке, если нет заказов:

```
No orders found for this date.
```

### 2. Оформление заказа

- URL: /orders/
- Метод: POST
- Тело запроса (формат: application/x-www-form-urlencoded):
  - apartment_number (строка, от 1 до 10 символов)
  - pet_name (строка, от 1 до 50 символов)
  - pet_breed (строка, от 1 до 50 символов)
  - walk_date (формат: YYYY-MM-DD)
  - walk_time (формат: HH:MM)

**Пример запроса:**

```
POST /orders/
Content-Type: application/x-www-form-urlencoded

apartment_number=12B&pet_name=Buddy&pet_breed=Labrador&walk_date=2024-08-28&walk_time=10:00
```

**Пример ответа:**

```json
[
	{
		"id": 1,
		"apartment_number": "12B",
		"pet_name": "Buddy",
		"pet_breed": "Labrador",
		"walk_date": "2024-08-28",
		"walk_time": "10:00:00",
		"created_at": "2024-08-27 16:00:39"
	}
]
```

**Сообщение об ошибке, если время уже занято:**

```json
[
	{
		"detail": "This time slot is fully booked."
	}
]
```

## Как запустить проект

**Первый метод : Запуск через Docker**

1. **Cоздайте файл .env в корневой директории проекта и укажите параметры подключения к базе данных PostgreSQL:**

`env`

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
```

2. **Создайте Docker образ для вашего приложения:**

- В корневой директории проекта создайте файл Dockerfile со следующим содержимым:

`Dockerfile`

```
# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY requirements.txt ./
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

3. **Создайте Docker образ:**

- В корневой директории проекта выполните команду:

`bash`

```
docker build -t pawcontroll .

```

4. **Запустите контейнер PostgreSQL:**

`bash`

```
docker run -d \
  --name postgres-db \
  -e POSTGRES_DB=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:14

```

5. **Запустите контейнер с вашим приложением:**

`bash`

```
docker run -d \
  --name pawcontroll-web \
  --link postgres-db:db \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres \
  pawcontroll

```

_Ваше приложение будет доступно по адресу http://localhost:8000._

**Второй метод : Запуск без Docker**

1. **Клонируйте репозиторий на свою локальную машину:**

`bash`

```
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository

```

2. **Создайте виртуальное окружение и активируйте его:**

`bash`

```
python -m venv venv
source venv/bin/activate  # Для Windows используйте: venv\Scripts\activate

```

3. **Установите необходимые зависимости:**

`bash`

```
pip install -r requirements.txt

```

4. **Создайте файл .env в корневой директории проекта и укажите параметры подключения к базе данных PostgreSQL:**

`env`

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres

```

5. **Запустите базу данных PostgreSQL (если она не установлена):**

- Вы можете запустить PostgreSQL в Docker:

`bash`

```
docker run -d \
  --name postgres-db \
  -e POSTGRES_DB=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:14
```

6. **Запустите приложение FastAPI:**

`bash`

```
uvicorn main:app --reload
```

_Ваше приложение так же будет доступно по адресу http://localhost:8000._
