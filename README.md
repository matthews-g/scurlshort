# scurlshort

## URL shortener API created with Django REST API framework.
This is a sample project I have made using Django REST API Framework. 

# Requirements
- [Requirements.txt](https://github.com/matthews-g/scurlshort/blob/main/requirements.txt)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Database information must be configured here!](https://github.com/matthews-g/scurlshort/blob/main/.idea/database_config.env)

# Easy setup!
0. Install PostgreSQL, create the database, and edit database_config.env

1. Clone repo:
```
git clone https://github.com/matthews-g/scurlshort.git
```
2. Create virtual environment:
```
python3 -m venv env
source env/bin/activate
```

3. Install requirements: (do not forget to cd/scurlshort)
```
pip install -r requirements.txt
```
4. Make migrations and sync db model
```
python manage.py makemigrations
python manage.py migrate
```
5. Run the server
``` 
python manage.py runserver
```

6. WHILE THE SERVER IS RUNNING (use another terminal maybe): Run tests

``` 
python manage.py test
```
 Don't forget to make sure the secondary terminal is in the same virtual environment by `source env/bin/activate` while testing!
 
# API endpoints

| Method  | Endpoint | Example usage | Description
| ------------- | ------------- | ------------- | ------------- |
| POST  | /shorten/ | http://127.0.0.1:8000/shorten/ | Make sure to include "url" parameter in the body. "shortcode" parameter is optional if you want custom shortcode!
| GET  | /\<shortcode>/  | http://127.0.0.1:8000/iFxlBj/ | This request will redirect to the shorted URL.
| GET | /\<shortcode>/stats | http://127.0.0.1:8000/iFxlBj/stats | Get the creation date, last redirect date, redirect count data of the given shortcode.




