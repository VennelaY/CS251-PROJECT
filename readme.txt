To open the website run this command inside the project directory 
python3 manage.py runserver

If we add any field in any model we need to run this command so that cloumns of that field are created in the database file
python3 manage.py migrate --run-syncdb

python3 manage.py makemigrations
 python3 manage.py migrate
