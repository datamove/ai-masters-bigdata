# Примерный проект

Несмотря на то, что в этом проекте содержатся задания в виде "напишите", "создайте", этот проект не надо делать, но можно  (и нужно) посмотреть, как он устроен, и что ожидается от вас в настоящих заданиях. Все приведенные команды - рабочие и их можно запускать.

## Общие принципы заданий

* Большие данные служит задачам машинного обучения
  * в каждом задании у вас будет модель машинного обучения
* Большие данные (и вообще production) накладывают определенные рамки из задают определенный формат работы
  * мы делаем для вас такие рамки
* Обучение модели производится, как правило, локально. Исключение -  Spark ML
* Тренировочная и валидационные выборки предоставляются.
* Проверка модели производится на невиданных ранее данных.
* Мы запускаем ваш код для проверки - обучаем модель, делаем предсказания на неиспользуемых ранее данных.

## Описание задачи

Вам требуется предсказать общий рейтинг отеля из датасета [Tripadvisor Hotel Review](https://github.com/kavgan/OpinRank).

Поля датасета:

`doc_id,hotel_name,hotel_url,street,city,state,country,zip,class,price,num_reviews,CLEANLINESS,ROOM,SERVICE,LOCATION,VALUE,COMFORT,overall_ratingsource`

Вам надо предсказать `overall_ratingsource`. Метрика - МАЕ.

Датасет содержится в файле hotels.cvs в папке референсного проекта.

## Последовательность действий

* обучение модели на заданном тренровочном датасете (локально)
* валидация модели на заданном валидационном датасете (локально или на кластере)
* валидация фильтрации и предсказания на фильтрованном датасете для заданного валидационного датасета и условий фильтрации (на кластере).
* коммит кода в ваш приватный репо ozon-masters-bigdata
* вызов проверки

## Оформление работы

Создайте в гитхабе репозиторий `ozon-masters-bigdata`. В папке репозитория создайте рекурсивно папки `projects/0`. Все ваши файлы с моделями и кодом для тренировки и инференса будут располагаться в этой папке.

Вот файлы референсного проекта:

```
README.md
filter.py
filter.sh
filter_cond.py
filter_predict.sh
hotels.csv
model.py
predict.py
predict.sh
scorer.py
scorer.sh
train.py
train.sh
```

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

Также в файле с моделью мы определяем поля датасета:

```
fields = """doc_id,hotel_name,hotel_url,street,city,state,country,zip,class,price,
num_reviews,CLEANLINESS,ROOM,SERVICE,LOCATION,VALUE,COMFORT,overall_ratingsource""".replace("\n",'').split(",")
```

и так же импортируем их:

`from model import fields`

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
projects/0/train.sh 0 projects/0/hotels.csv
```

где 0 - номер проекта, hotels.csv - путь к файлу с тренировочной выборкой (включен в папке проекта в репо ozon-masters-bigdata).

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
#copy input dataset to HDFS
hdfs dfs -copyFromLocal hotels.csv hotels.csv
#remove output dataset if exists
hdfs dfs -rm -r -f -skipTrash predicted.csv
projects/0/predict.sh projects/0/predict.py,0.joblib hotels.csv predicted.csv predict.py
```

где параметры:

* файлы для посылки с задачей (включая тренированную модель)
* путь к тестовому датасету (в примере используется тренировочный для простоты)
* путь к файлу с предсказаниями
* скрипт для запуска


## Расчет метрики на валидационной выборке

Мы будем проверять работу модели на нескольких срезах датасета. Разработайте скрипт, для фильтрации по заданному условию. Это скрипт должен будет считывать датасет из стандартного ввода и выводить на стандортный вывод только записи, удовлетворяющие заданным условиям. Кроме того, поскольку мы делаем валидиционную выбюорку, то нужно будет получить 2 файла - с целевой переменной и с фичами.

## Фильтрация датасета

Разработайте скрипт filter.py для фильтрации датасета, который берет записи из датасета на стандартном входе, применяет некоторую функцию фильтрации и выводит записи, прошедшие фильтр, на стандартный вывод.

Для одновременного выделения целевой переменной из датасета, подайте ее название в качестве агрумента со знаком `+`.
Для выделения признаков, подайте название целевой переменной в качестве агрумента со знаком `-`.
В обоих случаях первая колонка (идентификатор записи) так же выводится.

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

Разработайте `filter.sh`, который должен запускать map-reduce задачу на кластер:

Параметры скрипта filter.sh:

* файлы, которые надо послать вместе с задачей, через запятую
* путь к входному файлу
* путь к выходному файлу
* имя файла с программой маппером, то есть filter.py, с опциональным аргументом +column or -column, где column - ваша целевая переменная.

Помните, что если путь к файлам hotels.csv and filtered.csv задан без '/' в начале, то  файлы берутся относительно вашей домашней директории в HDFS /user/$USER.

### Простая фильтрация

```
cd ozon-masters-bigdata
hdfs dfs -rm -f -r -skipTrash filtered.csv
projects/0/filter.sh projects/0/filter.py,projects/0/filter_cond.py hotels.csv filtered.csv filter.py
```

### Фильтрация с выводом только целевой переменной

```
cd ozon-masters-bigdata
hdfs dfs -rm -f -r -skipTrash filtered.csv
projects/0/filter.sh projects/0/filter.py,projects/0/filter_cond.py hotels.csv filtered-target.csv "filter.py +overall_ratingsource"
```

### Фильтрация с выводом только признаков

```
cd ozon-masters-bigdata
hdfs dfs -rm -f -r -skipTrash filtered.csv
projects/0/filter.sh projects/0/filter.py,projects/0/filter_cond.py hotels.csv filtered-features.csv  "filter.py -overall_ratingsource"
```

## Расчет метрики на валидационных срезах

Запустите predict.sh на валидационном среде и получите `predicted.csv`

Разработайте программу для подсчета выбранной метрики на кластере. Вспомните, что у нас filtered-target.csv и predicted.csv содержат идентификатор записи. Воспользуемся им в качестве ключа для редюсера. Маппер нам не нужен, вернее, мы воспользуемся им для объединения filtered-target.csv и predicted.csv. Затем понадобится стадия shuffle, после которой записи будут отсортированы по ключу, то есть иметь вид:

```
usa_san francisco_the_herbert_hotel,3.3796997285893906	
usa_san francisco_the_herbert_hotel,3.4216216216216218	
```

где одно из значений - истинное, другое предсказанное.

В редьюсере мы будем считывать их и считать метрику на этих парах.

Запуск скорера:

```
hdfs dfs -rm -r -f -skipTrash score
projects/0/scorer.sh projects/0/scorer.py filtered-target.csv predicted.csv score scorer.py
```

где аргументы:

* файлы, которые надо послать вместе с задачей, через запятую
* путь к входному файлу с истинным значение целевой переменной
* путь к выходному файлу с предсказанным значениес
* путь к файлу со значением метрики
* имя файла с программой редьюсера, то есть scorer.py.

Результат работы - файл с одним значением - метрикой.

```
$ hdfs dfs -cat score/*
0.03830651020242537	
```

## Фильтрация и предсказания одной задачей

Выше мы запускали отдельно фильтрацию и предсказания. Теперь мы запустим одну mapreduce задачу в которой мы будем фильтровать датасет на стадии map и предсказывать на стадии reduce. Приемущество - всего одна задача и не надо управлять промежуточными данными.

```
projects/0/filter_predict.sh projects/0/filter.py,projects/0/predict.py,projects/0/filter_cond.py,0.joblib hotels.csv pred_with_filter filter.py predict.py
```

где аргументы:

* файлы, которые надо послать вместе с задачей, через запятую
* путь к входному файлу 
* путь к выходному файлу 
* имя файла с программой маппера, то есть filter.py.
* имя файла с программой редьюсера, то есть predict.py.

## Проверка

Для проверки нам понадобится доступ к содержимому вашего репозитория.

### Deploy keys

Для доступа (только для чтения) в ваш репозиторий ozon-masters-bigdata, добавте следующий публичный ключ в ваш репизиторий, используя инструкцию https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys (пункты 2-8; отмечать галочку Allow write access НЕ надо).

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC+K60wfXNhZ+hUu155vf/xzfPIce23exvmAV09cBO6cAGAburmb9KOpfOzLqmAMs9fWjnO0dzwQPy7/vxFT7+Swy4QILX2oI2GkIxCo0l9A2b2lyj2krlhE1NRWLtoSs90F/U4muTqh0pObwkllWrqgUy75hxq2txODETb+T1k7pSWg3MjQaSJXqIGFHzmd7BaDxLQWupDWt1Wd/ZK7jOEXoPaGU7voGNI0NEtn6UFkeMODmHrrUAXxI0wFQQnok9Vn6CyWN6AG/pwVCMnHU3IdQnA2zaADv7WVdFp+4jnw/ggg7Px4iyzRzQh305gx0FRnJKm/2dh+smWKemr6XQp datamove@ip-10-0-1-212
```

### Шаги проверки

* клонирование вашего репозитория.
* запуск тренировки модели на известном тренировочном датасете
* запуск фильтрации+предсказания неизвестного заранее тестового датасета с неизвестным заранее условием
* запуск расчета метрики для полученных предсказаний.
* запись полученной метрики.

## Flask app

Для проверки работы shell скриптов можно использовать простой REST API сервер на основе Flask.

Запустите: ./flask-app.py` 

### Train

This triggers training of the model 0 by calling train.sh:

`curl -X POST -H "Content-Type: application/json" -d '["0", "projects/0/hotels.csv"]' localhost:5000/train/0`

and so on
