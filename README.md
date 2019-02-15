#Conference room app

### Requirements:
* python3==3.7
* Django==2.1.7
* psycopg2-binary==2.7.7
* pytz==2018.9


## How to start

1. [*Fork*](https://guides.github.com/activities/forking/) the project to your profile.
2. [*Clone*](https://help.github.com/articles/cloning-a-repository/) the repository on your computer.
3. From postgreSQL interface, run the command `CREATE DATABASE confroom_db`, the database that the app will interact with will be create.
4. From the repository you just cloned, cd to [git_repository]/confroom and run command `python3 manage.py makemigrations` then `python3 manage.py migrate`.
5. You are ready now to run the app, run the command `python3 manage.py runserver`, the link to reach the app will be showing below.


##App content

* From the main page, you will be able to add, delete or edit existing rooms. You will have also the possibility to room details from which you will be able to book the chosen room.
* There is also a search menu from which you will be able to find available rooms on a given day.