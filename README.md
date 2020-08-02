# PSP (Personal Software Process) 
#
#### ¿What is PSP?

> PSP is a structured software development process that is designed to help software engineers better understand and improve their performance by bringing discipline to the way they develop software and tracking their predicted and actual development of the code.
* [More details about PSP]

### Dependencies
- Python > 3.0
- Django >= 3.0
- Database: PostgreSQL

### Installation

Remember to create and configure the parameters of access to the database in the file ```varlocal.py```:

```sh
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_PORT = ""
```

#### Linux:
```sh
1. python3 -m venv .env
2. source .env/bin/activate
3. pip install -r requirements.txt 
4. python manage.py migrate
5. python manage.py runserver
```
#### Windows:
```sh
1. python -m venv .env
2. cd .env/Scripts/
3. activate
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py runserver
```
#
Verify the deployment by navigating to your server address in your preferred browser.

```sh
127.0.0.1:8000
```


   [More details about PSP]: <https://en.wikipedia.org/wiki/Personal_software_process>