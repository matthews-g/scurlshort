# scurlshort

Quick readme

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
Don't forget to make sure the secondary terminal is in the same virtual environment by `source env/bin/activate`
