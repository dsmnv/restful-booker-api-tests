# Restful Booker API Tests

Набор автоматизированных тестов для публичного API: [Restful Booker](https://restful-booker.herokuapp.com/)

Проект написан на `Python + Pytest + Requests` с генерацией отчётов в **Allure**, фикстурами, и CI на GitHub Actions.

---

## Что покрыто тестами

- ✅ Получение бронирования по ID (GET)
- ✅ Создание нового бронирования (POST)
- ✅ Полное и частичное обновление (PUT/PATCH)
- ✅ Удаление бронирования (DELETE)
- ✅ Негативные проверки (невалидный ID, без авторизации, неполный payload)

---
## Как запустить тесты локально

```bash
pip install -r requirements.txt
pytest --alluredir=reports
```

Чтобы открыть Allure-отчёт:

```bash
allure serve reports
```

---

## CI / GitHub Actions

Проект интегрирован с GitHub Actions: тесты автоматически запускаются при каждом `push` и `pull request`.

---

## Структура проекта

```
├── .github/workflows/       # Конфигурация GitHub Actions (CI)
├── tests/                   # Тесты (разделены по методам: GET, POST, PUT/PATCH, DELETE)
├── utils/
│   ├── api_client.py        # API-клиент: функции-обёртки над запросами
│   ├── assertions.py        # Общие проверки (валидность структуры, соответствие payload'у)
│   └── data_generator.py    # Генерация тестовых данных (Faker)
├── conftest.py              # Фикстуры Pytest
├── requirements.txt         # Зависимости проекта
├── pytest.ini               # Конфигурация Pytest
└── README.md
```

---

## Используемые технологии

- Python 3.10
- Pytest
- Requests
- Faker
- Allure Pytest
- GitHub Actions

---

## 👨‍💻 Автор

Этот проект создан как pet-проект для практики API тестирования, работы с CI и структурирования автотестов.

Автор: [@dsmnv](https://github.com/dsmnv)