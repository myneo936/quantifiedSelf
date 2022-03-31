# Quantified Self
### _By: Sanskar Vatsal_
Quantified Self is a web based platform form users to track their habits and well being. It is a  web-app created using python. Several other modules like flask, flask-sqlalchemy, flask_login and matplotlib are also used.

## Replit run
- Go to shell and run
    `pip install --upgrade poetry`
- Click on `main.py` and click button run
- Sample project is at https://replit.com/@neo936/qself
- The web app will is availabe at https://qself.neo936.repl.co

## To run on your local device
- Download all the files in one directory.
- Make a virtual environment using in your command prompt using `py -3 -m venv venv`
- Activate the virtual environment using `venv\Scripts\activate`
- Use command `pip install -r requirements.txt` to install all the modules required to run the web-app.
- Use `python main.py` to run the application.


# Folder Structure
- `main.py` is the file which assembles and runs the web-app.
- `db_directory` has the sqlite database named 'project.sqlite3'
- `application` is where our application code is contained
-  `templates` folder contains the html files. Bootstrap is used for styling
- `static` default `static` files folder. It serves at '/static' path and contains images.
- `feedback.txt` contains the output of feedback forms given by users.
- `multiple.csv` contains necessary data files for tracking.
- `requirements.txt` contains the necessary modules used in application to run the web-app.# quantifiedSelf
# quantifiedSelf
