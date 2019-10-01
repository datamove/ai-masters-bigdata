# Примерный проект

Этот проект не надо делать, но можно посмотреть, как он устроен, и что ожидается от вас в настоящих заданиях.
Для образца проекта возьмите `https://github.com/datamove/ozon-masters-bigdata`

## Описание задачи

Вам требуется предсказать общий рейтинг отеля из датасета [Tripadvisor Hotel Review](https://github.com/kavgan/OpinRank).

Поля датасета:

`doc_id,hotel_name,hotel_url,street,city,state,country,zip,class,price,num_reviews,CLEANLINESS,ROOM,SERVICE,LOCATION,VALUE,COMFORT,overall_ratingsource
`
Вам надо предсказать overall_ratingsource

Датасет содержится в файле hotels.cvs в папке референсного проекта.

## Оформление работы

Создайте в гитхабе репозиторий `ozon-masters-bigdata`. В папке репозитория создайте рекурсивно папки `projects/0`. Все ваши файлы с моделями и кодом для тренировки и инференса будут располагаться в этой папке.

Вот файлы референсного проекта:

```
README.md
filter.py
filter.sh
filter_cond.py
hotels.csv
model.py
predict.py
predict.sh
train.py
train.sh
```

## Семплирование датасета

Разработайте скрипт sample.py который сэмплирует большой датасет и получает репрезентативный датасет маленького размера, пригодного для обучения на одном сервере

## Фильтрация датасета

Разработайте скрипт filter.py для фильтрации датасета, который берет записи из датасета на стандартном входе, применяет некоторую функцию фильтрации и выводит записи, прошедшие фильтр, на стандартный вывод.

Фильтрующая функция определяется в файле `filter_cond.py` и имеет следующий интерфейс:

```
def filter_cond(line_dict):
    """Filter function
    Takes a dict with field names and values as the argument
    Returns True if conditions are satisfied
    """
    cond_match = (
       int(line_dict["num_reviews"]) > 20
    ) 
    return True if cond_match else False
```

## Запуск фильтрации

Скопируйте датасет на HDFS:

```
cd ozon-masters-bigdata
hdfs dfs -copyFromLocal projects/0/hotels.csv /user/$USER/hotels.csv
```

Разработайте `filter.sh`, который должен запускать map-reduce задачу на кластер:

```
cd ozon-masters-bigdata
hdfs dfs -rm -f -r -skipTrash filtered.csv
projects/0/filter.sh hotels.csv filtered.csv projects/0/filter.py,projects/0/filter_cond.py filter.py
```

Параметры скрипта filter.sh:

* путь к входному файлу
* путь к выходному файлу
* файлы, которые надо послать вместе с задачей, через запятую
* имя файла с программой маппером, то есть filter.py

Помните, что если путь к файлам hotels.csv and filtered.csv задан без '/' в начале, то  файлы берутся относительно вашей домашней директории в HDFS /user/$USER.

## Model

Разработайте модель, используя `sklearn.pipeline.Pipeline` и определите её в файле model.py . Назовите вашу переменную `model`:

```
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('linearregression', LinearRegression())
])
```

и тогда ее можно будет импортировать в других программах как:

`from model import model`

## Обучение модели

Обучение модели проводится на семплированном датасете на одном узле. Разработайте программу train.py, которая импортирует ранее определенную модель и обучает её. На вход в качестве аргумента подается 

* номер проекта
* путь к файлу с обучающей выборкой. 

Обученная модель сохраняется в файл `0.joblib` используя сериализатор joblib:

```
from joblib import dump
dump(model, "0.joblib")
```

## Запуск обучения

Напишите shell-wrapper для train.py, который будет запускаться из следующим образом:

This assumes that filtered.csv is in the current folder, not in hdfs:

```
cd ozon-masters-bigdata
hdfs dfs -getmerge filtered.csv filtered.csv
projects/0/train.sh 0 filtered.csv
```

где 0 - номер проекта, filtered.csv - путь к файлу с тренировочной выборкой (в этом примере предполагается, что файл лежит в ozon-masters-bigdata).

## Предсказания (инференс)

Напишите программу predict.py, которая загружает обученную модель и сохраненную ранее модель:

```
from joblib import load
model = load("0.joblib")
```

и выдает предсказания на стандартный вывод для тестовых записей, которые подаются на стандартный ввод.

## Запуск инференса

Напишите shell-wrapper predict.sh для запуска инференса как map-reduce задачи на кластере:

```
cd ozon-masters-bigdata
hdfs dfs -rm -r -f -skipTrash predicted.csv
projects/0/predict.sh filtered.csv predicted.csv projects/0/predict.py,0.joblib predict.py
```

где параметры:

* путь к тестовому датасету (в примере используется тренировочный для простоты)
* путь к файлу с предсказаниями
* файлы для посылки с задачей (включая тренированную модель)
* скрипт для запуска

## Проверка

Для проверки на понадобится доступ к собержимому вашего репозитория.

### Deploy keys

Для доступа (только для чтения) в ваш репохиторий ozon-masters-bigdata, добавте следующий публичный ключ в ваш репизиторий, используя инструкцию https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys (пункты 2-8; отмечать галочку Allow write access НЕ надо).

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC+K60wfXNhZ+hUu155vf/xzfPIce23exvmAV09cBO6cAGAburmb9KOpfOzLqmAMs9fWjnO0dzwQPy7/vxFT7+Swy4QILX2oI2GkIxCo0l9A2b2lyj2krlhE1NRWLtoSs90F/U4muTqh0pObwkllWrqgUy75hxq2txODETb+T1k7pSWg3MjQaSJXqIGFHzmd7BaDxLQWupDWt1Wd/ZK7jOEXoPaGU7voGNI0NEtn6UFkeMODmHrrUAXxI0wFQQnok9Vn6CyWN6AG/pwVCMnHU3IdQnA2zaADv7WVdFp+4jnw/ggg7Px4iyzRzQh305gx0FRnJKm/2dh+smWKemr6XQp datamove@ip-10-0-1-212
```

## Flask app

Длф проверки работы shell скриптов можно использовать простой REST API сервер на основе Flask.

Запустите: ./flask-app.py` 

### Train

This triggers training of the model 0 by calling train.sh:

`curl -X POST -H "Content-Type: application/json" -d '["0", "projects/0/filtered.csv"]' localhost:5000/train/0`

and so on
