# Проект menu-api-crud

## **Описание**. 
 
Сервис предоставляет api crud для меню.

## **Стек технологий**
fastapi, postgesql, alembic, 


## **Установка**:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Kaliendos/menu-api-crud.git
```


Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```



Запустить проект:

```
uvicorn main:app --reload

```

## **Примеры запросов**
api/v1/menus/ - возвращает список всех меню 
api/v1/menus/menu_id - возвращает конкретное меню
api/v1/menus/menu_id/submenus - возвращает список подменб конкретного меню
Доументация доступна после запуска сервера по адрессу:

http://127.0.0.1:8000/docs/
