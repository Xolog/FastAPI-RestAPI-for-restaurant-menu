# Ylab Homework 1 "Меню ресторана"

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
Далее добавьте в директорию проекта свой **.env** файл с данными для подключения к БД 
```
cd api
uvicorn main:app --reload  
```
