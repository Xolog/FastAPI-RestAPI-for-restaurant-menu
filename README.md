# RestAPI "Меню ресторана"

Проект на _FastAPI_, в котором отображена работа с фреймворком и _SQLAlchemyORM_, а также выполнение всех **CRUD** операций 
на примере трёх связанных сущностей.

## Зависимости
* Windows / Linux
* Python 3.12
* Poetry
* PostgreSQL

## Установка
```
git clone https://github.com/Xolog/Ylab_homework.git
cd Ylab_homework  
poetry install  
```
Если виртуальное окружение не активировалось в **shell**, то активируйте его с помощью команды
```
poetry shell
```

Далее добавьте в директорию проекта свой **.env** файл с данными для подключения к БД и примените миграции
```
alembic upgrade head 
```
Запустите проект
```
cd api
uvicorn main:app --reload  
```
Перейдите в браузере по ссылке из терминала (по умолчанию http://127.0.0.1:8000)
