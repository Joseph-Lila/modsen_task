<h1>Таск для LLK (Артур Прокопенко)</h1>

[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-informational?style=flat&logo=linkedin&logoColor=white&color=1CA2F1)](https://www.linkedin.com/in/artur-prakapenka-9894a3214/)
[![GitHub Badge](https://img.shields.io/badge/GitHub-informational?style=flat&logo=github&logoColor=white&color=black)](https://github.com/Joseph-Lila)
[![Codewars Badge](https://www.codewars.com/users/Joseph-Lila/badges/small)](https://www.codewars.com/users/Joseph-Lila)
[![Vkontakte Badge](https://img.shields.io/badge/VK-informational?style=flat&logo=vk&logoColor=white&color=red)](https://vk.com/lilalokikali)

<h2>Содержание</h2>
<h3>
[1. Гайд по поднятию (Windows) (без Docker)](#windows_without_docker)
</h3>
<strike>
<h3>
[2. Гайд по поднятию (Windows) (с Docker)](#windows_with_docker)
</h3>
</strike>

<a id="windows_without_docker"></a>
<h2>Гайд по поднятию (Windows) (без Docker)</h2>

1. Перейти в папку с проектами python
2. Открыть cmd (путь должен совпадать с путем к текущей папке) 
3. Запустить команду для клонирования репозитория

```commandline
git clone https://github.com/Joseph-Lila/modsen_task.git
```

4. Установить Python3.10
5. Открыть проект и установить все зависимости 

```commandline
pip install -r requirements.txt
```

6. Создать .env файл в корневой папке проекта (modsen_test) и поместить туда следующий текст (с добавлением значений):

```commandline
### TESTING POSTGRESQL DATABASE
POSTGRESQL_TEST_HOST = 'xxx'
POSTGRESQL_TEST_PORT = xxx
POSTGRESQL_TEST_MAINTENANCE_DATABASE = 'xxx'
POSTGRESQL_TEST_USERNAME = 'xxx'
POSTGRESQL_TEST_PASSWORD = 'xxx'

### POSTGRESQL DATABASE
POSTGRESQL_HOST = 'xxx'
POSTGRESQL_PORT = xxx
POSTGRESQL_MAINTENANCE_DATABASE = 'xxx'
POSTGRESQL_USERNAME = 'xxx'
POSTGRESQL_PASSWORD = 'xxx'

### TESTING ELASTICSEARCH
ELASTICSEARCH_TEST_URI = 'xxx'

### ELASTICSEARCH
ELASTICSEARCH_URI = 'xxx'

```

7. Настроить PostgreSQL в соответствии с указанными в .env данными
8. Запустить Elasticsearch (в соответствии с установленными в .env переменными)
9. Из корня проекта запустить приложение (!!! путь к файлу с тестовыми данными указать свой):

```commandline
python -m src.entrypoints.fastapi_app --drop_create_tables True --drop_create_indices True --init_with_csv True --init_elastic_with_db True --initial_csv_path D:/PycharmProjects/modsen_test/assets/task/posts.csv 
```

* этот скрипт создает таблицы в бд, создает индекс в elasticsearch, заполняет бд из csv-файла и, наконец, добавляет документы из бд в elasticsearch в необходимом формате (только id, text). 

10. Дальнейшие запуски приложения осуществлять с помощью команды:

```commandline
python -m src.entrypoints.fastapi_app
```

11. Перейти по ссылке, предложенной в терминале.
12. Чтобы перейти к swagger, дописать к текущему адресу страницы /docs.
13. The end :)

<a id="windows_with_docker"></a>
<strike>
<h2 style="color:#FF0000">Гайд по поднятию (Windows) (с Docker)</h2>
</strike>

1. Перейти в папку с проектами python
2. Открыть cmd (путь должен совпадать с путем к текущей папке) 
3. Запустить команду для клонирования репозитория

```commandline
git clone https://github.com/Joseph-Lila/modsen_task.git
```

4. Создать .env файл в корневой папке проекта (modsen_test) и поместить туда следующий текст (с добавлением значений):

```commandline
### TESTING POSTGRESQL DATABASE
POSTGRESQL_TEST_HOST = 'xxx'
POSTGRESQL_TEST_PORT = xxx
POSTGRESQL_TEST_MAINTENANCE_DATABASE = 'xxx'
POSTGRESQL_TEST_USERNAME = 'xxx'
POSTGRESQL_TEST_PASSWORD = 'xxx'

### POSTGRESQL DATABASE
POSTGRESQL_HOST = 'xxx'
POSTGRESQL_PORT = xxx
POSTGRESQL_MAINTENANCE_DATABASE = 'xxx'
POSTGRESQL_USERNAME = 'xxx'
POSTGRESQL_PASSWORD = 'xxx'

### TESTING ELASTICSEARCH
ELASTICSEARCH_TEST_URI = 'xxx'

### ELASTICSEARCH
ELASTICSEARCH_URI = 'xxx'

```

5. Запустить приложение в Docker, используя следующую команду:

```commandline
docker compose up
```
6. Перейти по ссылке, предложенной в терминале.
7. Чтобы перейти к swagger, дописать к текущему адресу страницы /docs.
8. The end :)
