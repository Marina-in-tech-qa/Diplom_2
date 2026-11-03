
# Stellar Burgers — API Autotests

Автоматизированное тестирование API учебного сервиса Stellar Burgers.

Проект выполнен в рамках второго задания дипломной работы по автоматизации тестирования в Яндекс Практикуме.

## Технологии

- Python
- Pytest
- Requests
- Allure Framework

## Тестируемый сервис

https://qa-stellarburgers.education-services.ru/

## Структура проекта

```text
Diplom_2/
├── tests/
│   ├── test_create_user.py
│   ├── test_login_user.py
│   └── test_create_order.py
├── conftest.py
├── helpers.py
├── urls.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Тестовые сценарии

### Создание пользователя

- Регистрация уникального пользователя.
- Регистрация уже существующего пользователя.
- Регистрация без обязательных полей: email, password, name.

### Авторизация пользователя

- Авторизация с корректными учётными данными.
- Авторизация с некорректным email.
- Авторизация с некорректным паролем.

### Создание заказа

- Создание заказа авторизованным пользователем.
- Создание заказа без авторизации.
- Создание заказа без ингредиентов.
- Создание заказа с некорректным ингредиентом.

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Marina-in-tech-qa/Diplom_2.git
cd Diplom_2
git checkout develop2
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
```

Активировать окружение в Windows CMD:

```cmd
venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Запустить тесты

```bash
python -m pytest -v
```

## Allure-отчёт

Для формирования результатов тестирования:

```bash
python -m pytest -v --alluredir=allure-results --clean-alluredir
```

Для просмотра отчёта:

```bash
allure serve allure-results
```

Для просмотра отчёта необходим установленный Allure CLI.

## Результаты тестирования

При последнем локальном запуске:

- Всего тестов: 12
- Успешно: 12
- Ошибок: 0

## Автор

[Marina-in-tech-qa](https://github.com/Marina-in-tech-qa)
