## Описание проекта

#### Взаимодействие с API  
В ходе работы были загружены данные из API Кинопоиска по фильмам с рейтингом от 6 до 8 баллов по оценке КП.

Необходимо произвести вычисления:
-  Среднее расхождение оценки от платформы IMBD и Кинопоиск 
- Самый успешный год кинопроизводства с точки зрения оценок
- Самая успешная страна с точки зрения оценок  

Ссылка на документацию к API: 

https://api.kinopoisk.dev/v1/documentation

Для выполнения ТЗ был использован Python, библиотеки requests для загрузки данных из API Кинопоиска, numpy для вычислений, psycord2 для работы с базой данных PostgreSQL  

В функции `load_movies()` мы отправляем GET-запрос к API Кинопоиска с заданными параметрами рейтинга от 6 до 8 баллов. Мы также передаем заголовок с нашим API-ключом. Затем мы возвращаем данные в формате JSON.  

Затем мы вызываем функции для вычисления среднего расхождения оценки, самого успешного года и самой успешной страны кинопроизводства. Затем мы сохраняем данные в базу данных PostgreSQL с помощью функции `save_to_database()`. Наконец, мы выводим результаты вычислений на экран.

## Запуск проекта

Клонируем себе репозиторий:
```
git@github.com:Adelina1231/kinopoisk_parser.git
```

```
cd kinopoisk_parser/
```

Cоздать и активировать виртуальное окружение:
```
py -m venv venv
```

```
. venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Запустить проект:
```
py movies.py
```