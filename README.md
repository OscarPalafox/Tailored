# Tailored

## Objective
The objective of our application is to establish a safe and reliable trading environment that allows people to put their used clothes up for sale as well as offer them the chance of buying used clothes at a cheaper price.


## Environment Requiments
Python 3.6 or later is required for the web application to run. Earlier 3.x versions will not work and will result in syntax errors.


### Additional Packages
These packages can all be installed in a single command: pip install -r requirements.txt

- Django v1.11.27

Installation: pip install django

- django-registration-redux v2.6

Installation: pip install django-registration-redux

- django-cleanup v3.2.0

Installation: pip install django-cleanup

- Pillow v6.2.1

Installation: pip install pillow

- pytz v2019.1

Installation: pip install pytz


### Additional technologies and libraries used:
- Jquery
- JavaScript
- Bootstrap4
- animate Css library
- Poppins font
- Select2 Css library
- Used an example template found [here](https://colorlib.com/preview/theme/karl/index.html).


## Running the Population Script
You need to make migrations first:
- python manage.py makemigrations

You then need to migrate:
- python manage.py migrate

Finally you run the population script:
- python populate_tailored.py


## Testing
-	python manage.py test tailored


## PythonAnywhere
Url :  [tailored.pythonanywhere.com](https://tailored.pythonanywhere.com)
