### Pre requirements:

- You have to have a <b>Virtual Environment</b> to install all the dependencies in the <b>requirements.txt</b>

<b>Virtual enviroment settings:</b>

```sh
python3 -m venv ENV
source ENV/bin/activate
deactivate
```

<b>Installation of the required packages:</b>

```sh
pip freeze > requirements. txt
pip install -r requirements.txt
```

- You have to keep running both Django and Vue.js in terminal:

### Connection to the django

1. Go into the vendor folder:

```sh
python3 manage.py runserver
```

2. <b>URL Addresses</b> :
   Backend: http://127.0.0.1:8000/
   Admin Panel: http://127.0.0.1:8000/admin/
   For the admin panel you need Username Password, so please contact me
   Data to JSON: http://127.0.0.1:8000/api/v1/latest-products/

### Connection to the vue

1. Go into the vendor_vue folder:

```sh
npm run serve
```

2. <b>URL Address</b> :
   Frontend: 127.0.0.1:8080
