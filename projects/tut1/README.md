# Примерный проект (тьюториал)

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
* коммит кода в ваш приватный репо `ozon-masters-bigdata`
* вызов проверки

## Оформление работы

Создайте в гитхабе репозиторий `ozon-masters-bigdata`. В папке репозитория создайте рекурсивно папки `projects/tut1`. Все ваши файлы с моделями и кодом для тренировки и инференса будут располагаться в этой папке.

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

Обученная модель сохраняется в файл `tut1.joblib` используя сериализатор joblib:

```
from joblib import dump
dump(model, "tut1.joblib")
```

## Запуск обучения

Напишите shell-wrapper для train.py, который будет запускаться из корня репо следующим образом:

```
cd ozon-masters-bigdata
projects/tut1/train.sh tut1 projects/tut1/hotels.csv
```

где tut1 - номер проекта, hotels.csv - путь к файлу с тренировочной выборкой (включен в папке проекта в репо datamove/ozon-masters-bigdata).

## Предсказания (инференс)

Напишите программу predict.py, которая загружает обученную модель и сохраненную ранее модель:

```
from joblib import load
model = load("tut1.joblib")
```

и выдает предсказания на стандартный вывод для тестовых записей, которые подаются на стандартный ввод.

## Запуск инференса

Напишите shell-wrapper predict.sh для запуска инференса как map-reduce задачи на кластере:

```
cd ozon-masters-bigdata
#copy input dataset to HDFS
hdfs dfs -copyFromLocal hotels.csv hotels.csv
#remove output dataset if exists
hdfs dfs -rm -r -f predicted.csv
projects/tut1/predict.sh projects/tut1/predict.py,projects/tut1/model.py,tut1.joblib hotels.csv predicted.csv predict.py
```

где параметры:

* файлы для посылки с задачей (включая тренированную модель)
* путь к тестовому датасету (в примере используется тренировочный для простоты)
* путь к файлу с предсказаниями
* скрипт для запуска

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
* имя файла с программой маппером, то есть filter.py

Помните, что если путь к файлам hotels.csv and filtered.csv задан без '/' в начале, то  файлы берутся относительно вашей домашней директории в HDFS /user/$USER.

```
cd ozon-masters-bigdata
hdfs dfs -rm -f -r filtered.csv
projects/tut1/filter.sh projects/tut1/filter.py,projects/tut1/filter_cond.py,projects/tut1/model.py hotels.csv filtered.csv filter.py
```
О дополнительном фукнционале filter.py, который позволяет самостоятельно "нарезать" валижационные выборки см. ниже в разделе Дополнительные возможности.


## Фильтрация и предсказания одной задачей

Выше мы запускали отдельно фильтрацию и предсказания. Теперь мы запустим одну mapreduce задачу в которой мы будем фильтровать датасет на стадии map и предсказывать на стадии reduce. Приемущество - всего одна задача и не надо управлять промежуточными данными.

```
projects/tut1/filter_predict.sh projects/tut1/filter.py,projects/tut1/predict.py,projects/tut1/filter_cond.py,projects/tut1/model.py,tut1.joblib hotels.csv pred_with_filter filter.py predict.py
```

где аргументы:

* файлы, которые надо послать вместе с задачей, через запятую
* путь к входному файлу 
* путь к выходному файлу 
* имя файла с программой маппера, то есть filter.py.
* имя файла с программой редьюсера, то есть predict.py.

## Расчет метрики

Для расчета метрики на валидационном датасете запустите

`filter_local.py true_target predicted_target` 

где аргументы - пути к файлам с истинным занчением целевой переменной и предсказанным значениемцелевой переменной соответственно. Для простоты реализации, это скрипт работает не на кластере, а локально, считывая истинные и предсказанные значения в память.

Запуск метрики:

```
$ projects/tut1/scorer_local.py projects/tut1/filtered-target.csv  'http://name1:50070/webhdfs/v1/user/'$USER'/pred_with_filter/part-00000?op=OPEN'
INFO:root:CURRENT_DIR /home/users/datamove/ozon-masters-bigdata
INFO:root:SCRIPT CALLED AS projects/tut1/scorer_local.py
INFO:root:ARGS ['projects/tut1/filtered-target.csv', 'http://name1:50070/webhdfs/v1/user/datamove/pred_with_filter/part-00000?op=OPEN']
INFO:root:TRUE PATH projects/tut1/filtered-target.csv
INFO:root:PRED PATH http://head1:50070/webhdfs/v1/user/datamove/pred_with_filter/part-00000?op=OPEN
INFO:root:TRUE RECORDS 1746
INFO:root:PRED RECORDS 1746
0.096756706895581
```

Заметьте, как мы обращаемся к файлу, который находится в HDFS - через Webhdfs REST API.

Общее замечание: для некоторых метрик возможен расчет на кластере в парадигме мап-редьюс, см. ниже раздел Дополнительные возможности.

## Проверка

Для проверки нам понадобится доступ к содержимому вашего репозитория.

### Deploy keys

Для доступа (только для чтения) в ваш репозиторий ozon-masters-bigdata, добавьте в него публичный ключ, который был сгенерирован индивидуально для каждого и находится у каждого в домашней директории под именем:

`~/.ssh/id_rsa_deploy_key.pub`

Чтобы получить контент ключа для копи-вставки, воспользутейсь командой `cat`:

```
datamove@ozonm:~$ cat ~/.ssh/id_rsa_deploy_key.pub 
ssh-rsa AAAAB3NzaC .... GjwKt Github deploy key
```
Ключ - это одна строка, выделите и скопируйте ее в буфер обмена, затем вставьте в нужную форму на сайте гитхаб. Используйте инструкцию по добавлению deploy-ключа в репозиторий https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys (пункты 2-8; отмечать галочку Allow write access НЕ надо). Важно, что это нет то же самое что вы дела раньше для доступа на кластер. Ранее вы добавляли публичный ключ на весь аккаунт гитхаба, сейчас вы добавляете другой публичный ключ только в один репозиторий.



### Шаги проверки

* клонирование вашего репозитория.
* запуск тренировки модели на известном тренировочном датасете
* запуск фильтрации+предсказания неизвестного заранее тестового датасета с неизвестным заранее условием
* запуск расчета метрики для полученных предсказаний.
* запись полученной метрики.

### Запуск чекера

Вызовите `checker.sh tut1`

где tut1 - номер домашнего задания. Чекер запускается от имени служебного пользователя и сохраняет лог каждой попытки (лог так же показывается вам в терминал). Чекер запускается фоном и вы может закрыть терминал и не дожидаться его выполнения. Для того, чтобы получить через телеграмм уведомление об окончании работы чекера, создайте в корне вашего репо файл `tguserid` в который поместите id вашего пользователя в Телеграм, который можно получить командой /id нашего бота (@ozonm_big_data_bot).

Запуск и работа чекера, как это выглядит:

```
datamove@ozonm:~$ checker.sh tut1
ATTEMPT 17
DEPLOY_KEY=/home/ubuntu/.ssh/id_rsa_deploy_key_datamove
GIT_SSH_COMMAND=ssh -i /home/ubuntu/.ssh/id_rsa_deploy_key_datamove -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no
git clone git@github.com:datamove/ozon-masters-bigdata.git
Cloning into 'ozon-masters-bigdata'...
Warning: Permanently added 'github.com,140.82.121.3' (RSA) to the list of known hosts.
warning: unable to access '/home/users/datamove/.config/git/attributes': Permission denied
ATEMPTDIR /home/ubuntu/ozonmasters-checkers/hws/tut1/datamove/17
WORKDIR /home/ubuntu/ozonmasters-checkers/hws/tut1/datamove/17/ozon-masters-bigdata
=
= Train the model
=
INFO:root:CURRENT_DIR /home/ubuntu/ozonmasters-checkers/hws/tut1/datamove/17/ozon-masters-bigdata
INFO:root:SCRIPT CALLED AS projects/tut1/train.py
INFO:root:ARGS ['tut1', 'projects/tut1/hotels.csv']
INFO:root:TRAIN_ID tut1
INFO:root:TRAIN_PATH projects/tut1/hotels.csv
INFO:root:model score: 0.989
CHECK EXISTS http://name1:50070/webhdfs/v1/user/ubuntu/students/datamove?op=GETFILESTATUS
=
= Launch filter-predict
=
Deleted /user/ubuntu/students/datamove/predict
packageJobJar: [] [/usr/hdp/3.1.4.0-315/hadoop-mapreduce/hadoop-streaming-3.1.1.3.1.4.0-315.jar] /var/lib/ambari-agent/tmp/hadoop_java_io_tmpdir/streamjob4315838629947716612.jar tmpDir=null
21/02/11 08:56:46 INFO client.RMProxy: Connecting to ResourceManager at name1.ru-central1.internal/10.0.1.11:8050
21/02/11 08:56:47 INFO client.AHSProxy: Connecting to Application History server at name1.ru-central1.internal/10.0.1.11:10200
21/02/11 08:56:47 INFO client.RMProxy: Connecting to ResourceManager at name1.ru-central1.internal/10.0.1.11:8050
21/02/11 08:56:47 INFO client.AHSProxy: Connecting to Application History server at name1.ru-central1.internal/10.0.1.11:10200
21/02/11 08:56:48 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /user/datamove/.staging/job_1612971527524_0006
21/02/11 08:56:49 INFO mapred.FileInputFormat: Total input files to process : 1
21/02/11 08:56:49 INFO mapreduce.JobSubmitter: number of splits:2
21/02/11 08:56:50 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1612971527524_0006
21/02/11 08:56:50 INFO mapreduce.JobSubmitter: Executing with tokens: []
21/02/11 08:56:50 INFO conf.Configuration: found resource resource-types.xml at file:/etc/hadoop/3.1.4.0-315/0/resource-types.xml
21/02/11 08:56:51 INFO impl.YarnClientImpl: Submitted application application_1612971527524_0006
21/02/11 08:56:51 INFO mapreduce.Job: The url to track the job: http://name1.ru-central1.internal:8088/proxy/application_1612971527524_0006/
21/02/11 08:56:51 INFO mapreduce.Job: Running job: job_1612971527524_0006
21/02/11 08:57:00 INFO mapreduce.Job: Job job_1612971527524_0006 running in uber mode : false
21/02/11 08:57:00 INFO mapreduce.Job:  map 0% reduce 0%
21/02/11 08:57:09 INFO mapreduce.Job:  map 100% reduce 0%
21/02/11 08:57:16 INFO mapreduce.Job:  map 100% reduce 100%
21/02/11 08:57:16 INFO mapreduce.Job: Job job_1612971527524_0006 completed successfully
21/02/11 08:57:16 INFO mapreduce.Job: Counters: 53
	File System Counters
		FILE: Number of bytes read=558740
		FILE: Number of bytes written=1831896
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=1053534
		HDFS: Number of bytes written=104658
		HDFS: Number of read operations=11
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=2
	Job Counters 
		Launched map tasks=2
		Launched reduce tasks=1
		Data-local map tasks=2
		Total time spent by all maps in occupied slots (ms)=52756
		Total time spent by all reduces in occupied slots (ms)=33472
		Total time spent by all map tasks (ms)=13189
		Total time spent by all reduce tasks (ms)=4184
		Total vcore-milliseconds taken by all map tasks=13189
		Total vcore-milliseconds taken by all reduce tasks=4184
		Total megabyte-milliseconds taken by all map tasks=54022144
		Total megabyte-milliseconds taken by all reduce tasks=34275328
	Map-Reduce Framework
		Map input records=3096
		Map output records=1746
		Map output bytes=551945
		Map output materialized bytes=558746
		Input split bytes=220
		Combine input records=0
		Combine output records=0
		Reduce input groups=1746
		Reduce shuffle bytes=558746
		Reduce input records=1746
		Reduce output records=1746
		Spilled Records=3492
		Shuffled Maps =2
		Failed Shuffles=0
		Merged Map outputs=2
		GC time elapsed (ms)=388
		CPU time spent (ms)=6900
		Physical memory (bytes) snapshot=4954349568
		Virtual memory (bytes) snapshot=19421818880
		Total committed heap usage (bytes)=4811915264
		Peak Map Physical memory (bytes)=2369576960
		Peak Map Virtual memory (bytes)=5276372992
		Peak Reduce Physical memory (bytes)=218079232
		Peak Reduce Virtual memory (bytes)=8869089280
	Shuffle Errors
		BAD_ID=0
		CONNECTION=0
		IO_ERROR=0
		WRONG_LENGTH=0
		WRONG_MAP=0
		WRONG_REDUCE=0
	File Input Format Counters 
		Bytes Read=1053314
	File Output Format Counters 
		Bytes Written=104658
21/02/11 08:57:16 INFO streaming.StreamJob: Output directory: /user/ubuntu/students/datamove/predict
=
= Launch scorer
=
INFO:root:CURRENT_DIR /home/ubuntu/ozonmasters-checkers/hws/tut1/datamove/17/ozon-masters-bigdata
INFO:root:SCRIPT CALLED AS projects/tut1/scorer_local.py
INFO:root:ARGS ['/tmp/filtered-target.csv', 'http://name1:50070/webhdfs/v1/user/ubuntu/students/datamove/predict/part-00000?op=OPEN']
INFO:root:TRUE PATH /tmp/filtered-target.csv
INFO:root:PRED PATH http://name1:50070/webhdfs/v1/user/ubuntu/students/datamove/predict/part-00000?op=OPEN
INFO:root:TRUE RECORDS 1746
INFO:root:PRED RECORDS 1746
=
= SCORE 0.09716128066162834
=
PASSED 1
```

## Дополнительные возможности

### Собственные валидационные выборки

Опционально filter.py позволяет нарезать собственные валидационные выборки. Для этого вызовите filter.py с опциональным аргументом +column or -column, где column - ваша целевая переменная.

#### Фильтрация с выводом только целевой переменной

```
cd ozon-masters-bigdata
hdfs dfs -rm -f -r -skipTrash filtered.csv
projects/tut1/filter.sh projects/tut1/filter.py,projects/tut1/filter_cond.py hotels.csv filtered-target.csv "filter.py +overall_ratingsource"
```

#### Фильтрация с выводом только признаков

```
cd ozon-masters-bigdata
hdfs dfs -rm -f -r -skipTrash filtered.csv
projects/tut1/filter.sh projects/tut1/filter.py,projects/tut1/filter_cond.py hotels.csv filtered-features.csv  "filter.py -overall_ratingsource"
```

### Расчет метрики на кластере

Разработайте программу для подсчета выбранной метрики на кластере. Вспомните, что у нас filtered-target.csv и predicted.csv содержат идентификатор записи. Воспользуемся им в качестве ключа для редюсера. Маппер нам не нужен, вернее, мы воспользуемся им для объединения filtered-target.csv и predicted.csv. Затем понадобится стадия shuffle, после которой записи будут отсортированы по ключу, то есть иметь вид:

```
usa_san francisco_the_herbert_hotel,3.3796997285893906	
usa_san francisco_the_herbert_hotel,3.4216216216216218	
```

где одно из значений - истинное, другое предсказанное.

В редьюсере мы будем считывать их и считать метрику на этих парах. Это сработает для таких метрик, как МАЕ, но в общем случае (для произвольной метрики) так сделать не получится.

Запуск скорера:

```
hdfs dfs -rm -r -f -skipTrash score
projects/tut1/scorer.sh projects/tut1/scorer.py filtered-target.csv predicted.csv score scorer.py
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
