# absence-logger
A Web Application for Tracking and Analyzing Student Absences

## Description
`absence-logger` was developed in early 2019 to solve a simple problem: when students sign in and out of class on paper, it
is difficult to keep track of exactly how much class they are missing. `absence-logger` provides a simple interface to replace
paper sign-out sheets when students sign in and out of class; at the same time, it logs each absence in a database, and
and provides data-analytics tools for teachers to track how these absences are affecting students' performances.

The site consists of two main web apps: `hall_pass` and `teacher_view`. `hall_pass` provides the sign in and out interface
for students to use when leaving/re-entering class; `teacher_view` allows teachers to view this data later on.

## Architecture
`absence-logger` is built on a Django web framework and runs on a Gunicorn web server. This allows us to develop in Python :).

## Setup
This assumes you are developing on a Mac with homebrew and Python 3.7.2. If that's not you, well, then good luck...

### PostgreSQL
`absence_logger` runs on a PostgreSQL database. In order for the app to function, you must install the software and launch a
database server.

1. Install PostgreSQL
   * `brew install postgresql`
1. Start the Database Server
   * `pg_ctl -D /usr/local/var/postgres start`
   * (you can stop it with `pg_ctl -D /usr/local/var/postgres stop`)
1. Create a new table for the project
   * `createuser <database user>`
   * `createdb <database name>`
   * `psql`
     ```
     \du
     ALTER USER <database user> WITH PASSWORD '<database password>';
     GRANT ALL PRIVILEGES ON DATABASE <database name> TO <database user>;
     ALTER USER <database user> CREATEDB;
     ```
### Virtual Environments
`absence_logger` uses virtual environments for managing dependencies. Follow the below instructions to install and configure
the appropriate environment for development.

1. Install `virtualenv` and `virtualenvwrapper`
   * I used the instructions [here](http://www.marinamele.com/2014/07/install-python3-on-mac-os-x-and-use-virtualenv-and-virtualenvwrapper.html)
   * In an ideal world, if you have everything configured correctly, then these few lines should do the trick (nothing is ever
   that easy, though):
     ```
     pip3 install virtualenv
     pip3 install virtualenvwrapper
     echo 'export WORKON_HOME=~/.virtualenvs' >> ~/.bashrc
     echo 'VIRTUALENVWRAPPER_PYTHON=`which python3`' >> ~/.bashrc
     echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
     ```
1. Create a virtual environment for this project
   * `mkvirtualenv --python=/usr/local/bin/python3 absence_dev`
     * You can exit the virtual environment using `deactivate`, and reactivate with `workon absence_dev`
1. Install the project's dependencies
   * `pip install -r requirements/development.txt`

### Configure Environment Variables
Now that you have a running database server and a working virtual environment, you should configure the appropriate environment
variables so that the site works. So that we don't have to reset these each time we activate our environment, we leverage
the virtual environment wrapper.

1. If your virtual environment deactivated, activate it
   * `workon absence_dev`
1. Change into the virtual environment's bin directory
   * `cd $VIRTUAL_ENV/bin`
1. Add the following lines to the `postactivate` file
   1. `export DJANGO_SETTINGS_MODULE="absence_logger.settings.development"`
   1. `export SECRET_KEY=<secret>` (this is a secret kept out of version control, ask me for it :) )
   1. `export DATABASE_NAME=<database name>`
   1. `export DATABASE_USER=<database user>`
   1. `export DATABASE_PASSWORD='<database password>'`
1. Add the following lines to the `predeactivate` file
   1. `unset DJANGO_SETTINGS_MODULE`
   1. `unset SECRET_KEY`
   1. `unset DATABASE_NAME`
   1. `unset DATABASE_USER`
   1. `unset DATABASE_PASSWORD`

### Run the server!
If your database server is running and your virtual environment is activated with the correct dependencies installed, you
should be all set to run the app.

1. Apply database migrations (only need to do this once every time the database schema is updated on your local machine)
   * `python manage.py migrate`
1. Create a login so that you can manage the database (this is your local database instance, not the production one)
   * `python manage.py createsuperuser`
1. Run server
   * `python manage.py runserver`
1. Create a Course
   * navigate to http://localhost:8000/admin/
   * Create a TimberlaneSemester
   * Create a TimberlaneSchedule
   * Create a few Students
   * Create a Course based on your Students and the created Schedule
1. You should be able to access the site at http://localhost:8000/

## Currently working on:
1. Leverage Django's [admin](https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/) app for user
   authentication.
1. Create the `teacher_view` app for viewing database contents.
1. Implement schedule rules for Timberlane (right now, creating a `TimberlaneSchedule` just creates a default and kind of
   lame `Schedule` object.
1. Simplify code with [Django Generic Views](https://docs.djangoproject.com/en/2.1/topics/class-based-views/)
1. Improve the look of the web page using CSS
1. When creating a new absence, ensure that `datetime.now()` falls within a valid period as specified by the course schedule.
1. Develop a mechanism for signing students back in who have signed out and forgot to sign back in. Ideas:
   1. When rendering the sign_out page, assign `time_in` to the end of the period in which they signed out (cheap but lame)
   1. Launch a background service (heroku dyno?) which periodically checks and performs this task (better but may cost money)
1. Deploy to Heroku!
