# Salary Report Generator

## Описание

Скрипт для обработки CSV-файлов с данными сотрудников и генерации отчётов по зарплатам.  
Поддерживается передача нескольких файлов и выбор типа отчёта через CLI.  
Архитектура позволяет легко добавлять новые отчёты и вычисляемые поля.

---

## Установка

1. Клонируйте репозиторий:

    ```
    git clone https://github.com/NurgazievichR/csv-report-generator.git
    cd csv-report-generator
    ```

2. Создайте и активируйте виртуальное окружение:

    ```
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    ```

3. Установите зависимости (если есть):

    ```
    pip install -r requirements.txt
    ```

---

## Запуск скрипта


    python3 main.py path/to/file1.csv path/to/file2.csv --report payout


- `path/to/fileX.csv` — пути к CSV-файлам с данными сотрудников.  
- `--report` — имя отчёта (например, `payout`).

---

## Как добавить новый отчёт

## Как создавать новые отчёты

---

### 1. Где писать?

Рекомендуется помещать все функции отчётов в отдельный файл — **`app/reports.py`**.  
Это удобно для поддержки и расширения.

---

### 2. Используем декоратор `@report_decorator`

    from core import report_decorator

- При декорировании можно указать имя отчёта через параметр `name`.  
- Это имя нужно будет передавать в CLI через параметр `--report`, чтобы выбрать нужный отчёт.

---

### 3. Сигнатура функции отчёта

- Функция отчёта **всегда принимает один аргумент** — объект `obj` типа `CSVParser`:  

    ```python
    def payout(obj: CSVParser):
        ...
    ```

---

### 4. Как формировать вывод

У объекта `CSVParser` есть два метода для вывода отчётов:

- `output(*fields, calculated_fields_functions=[])` — печатает построчный отчёт с выбранными полями.  
- `output_group(group_by='department', calculated_group_fields_functions=[])` — группирует данные по выбранному полю и вычисляет групповые функции.

---

### 5. Примеры функций-отчётов

    @report_decorator(name="payout")
    def payout(obj: CSVParser):
        # Вывод отчёта по зарплатам с использованием вычисляемого поля 'payout'
        obj.output(calculated_fields_functions=['payout'])

    @report_decorator(name="average_hourly_rate_in_department")
    def average_hourly_rate_in_department(obj: CSVParser):
        # Группируем по отделу и выводим среднюю почасовую ставку
        obj.output_group(group_by='department', calculated_group_fields_functions=['average_hourly_rate'])

---

### 6. Аргументы методов

#### `output(*fields, calculated_fields_functions=[])`

- `fields` — имена колонок (из оригинального списка) которые нужно вывести (например, `'name'`, `'hours_worked'`).  
- `calculated_fields_functions` — список имён функций для вычисляемых полей (например, `'payout'`).

Пример:


    obj.output('name', 'hours_worked', calculated_fields_functions=['payout'])


---

#### `output_group(group_by='department', calculated_group_fields_functions=[])`

- `group_by` — поле, по которому группировать (по умолчанию `'department'`).  
- `calculated_group_fields_functions` — список имён функций, которые вычисляют агрегированные значения по группам (аналогично агрегатам в SQL, например `SUM`, `AVG`).

Пример:

    obj.output_group(group_by='department', calculated_group_fields_functions=['average_hourly_rate'])

## Как добавить вычисляемое поле

---

### 1. Импортируем декоратор

    from core import calculated_field_decorator

---

### 2. Параметры декоратора

- `name` — имя поля, которое будет отображаться в отчёте (рекомендуется указывать явно).  
- `max_size` — максимальная ширина поля в символах, нужна для правильного выравнивания вывода (рекомендуется всегда задавать).  
- `group` — булево значение, указывающее, является ли функция групповой (для агрегированных вычислений по группам) или вычисляет поле для отдельной строки (`True` или `False`).

---

### 3. Пример групповой функции

    @calculated_field_decorator(max_size=10, group=True)
    def average_hourly_rate(dct: dict):
        group_size = dct['group_size']
        total = sum(dct['hourly_rate']
        result = total / group_size
        return f"{result:.2f}"

---

### 4. Ещё пример групповой функции

    @calculated_field_decorator(max_size=10, group=True)
    def group_size(dct: dict):
        return dct['group_size']

---

### 5. Пример обычных вычисляемых полей (не групповых)

    @calculated_field_decorator(max_size=10)
    def payout(dct: dict):
        return dct['hourly_rate'] * dct['hours_worked']

    @calculated_field_decorator(max_size=10)
    def payout_year(dct: dict):
        return dct['hourly_rate'] * dct['hours_worked'] * 12

    @calculated_field_decorator(max_size=10)
    def first_name(dct: dict):
        return dct['name'].split()[0]

---

### 6. Где хранить вычисляемые функции?

Рекомендуется группировать вычисляемые функции в отдельные модули, например:

    calculated_fields.py  # для обычных (построчных) функций
    calculated_group_fields.py  # для групповых функций

---
## О колонках (COLUMNS)

- `COLUMNS_ORIGINALS` — список основных имён полей, которые использует программа, например:  
  `'id'`, `'email'`, `'name'`, `'department'`, `'hours_worked'`, `'hourly_rate'`.

- `COLUMNS_AND_ALIASES` — набор вариантов названий для каждого поля, чтобы поддерживать разные CSV. Например:  
  Для поля `'hourly_rate'` могут быть алиасы `'rate'` и `'salary'`.

- При загрузке CSV заголовки сопоставляются с этими алиасами, чтобы корректно обработать разные форматы.

- Чтобы добавить новое поле, нужно добавить его имя в `COLUMNS_ORIGINALS` и список алиасов в `COLUMNS_AND_ALIASES` в `app/columns.py`.

---

Так можно легко работать с разными файлами и расширять поля без изменений в логике.


## Структура проекта

---

Рекомендуется использовать такую структуру проекта:

    ├── app/                    # Расширяемый код: новые функции, отчёты, вычисляемые поля
    ├── core/                   # Основной функционал: парсер, декораторы, базовая логика
    ├── tests/                  # Тесты на pytest
    ├── main.py                 # Точка входа — CLI
    ├── requirements.txt        # Зависимости
    └── README.md               # Документация проекта

---

**Совет:**  
- Для добавления новых функций, отчётов и вычисляемых полей работайте в папке `app/`.  
- Не изменяйте `core/`, чтобы сохранить стабильность и облегчить поддержку ядра.


---

## Тестирование

Запуск всех тестов:

    pytest

Покрытие кода:

    pytest --cov=core tests/

---