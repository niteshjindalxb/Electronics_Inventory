from flask import Flask, render_template, redirect, url_for, session
# from model import Admin, StudentDetails, Issue, Inventory
from . import model
from . import settings

import os
import csv

def createApp():
    # create app
    app = Flask(__name__)
    # Set the secret key to some random bytes. Keep this really secret!
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    return app

def home():
    if validate_user():
        return redirect(url_for('dashboard'))

    if os.path.isfile(settings.rollno_file):
        return redirect(url_for('login'))        

    return render_template("home.html")


def login():
    if validate_user():
        print(settings.rollno)
        return redirect(url_for('dashboard'))
        
    try:
        with open(settings.rollno_file, "r") as f:
            settings.rollno = f.read()
    except FileNotFoundError:
        pass   
    else:
        # Remove the file already read
        os.remove(settings.rollno_file)
        
        session['username'] = settings.rollno
        return redirect(url_for('dashboard'))

    return redirect(url_for('home'))


def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    settings.rollno = None
    return redirect(url_for('home'))


def dashboard():
    if not validate_user():
        return redirect(url_for('home'))

    # Find student details with rollno
    cur_student = model.StudentDetails(None)

    for stud in settings.student_details:
        if int(stud.get_rollno()) == int(settings.rollno):
            cur_student = stud
            break

    return render_template("index.html", student=cur_student)

def issue():
    if not validate_user():
        return redirect(url_for('home'))

    # list_of_component
    # get all the id of items issued by rollno
    issued_id = []  # [id, quantity_issued]
    for log in settings.issue_log:
        if log.get_rollno() == settings.rollno:
            issued_id.append([log.get_id(), log.get_quantity()])

    # Get the items details having ID = id
    # Store the issued item list in issued_item
    issued_items = []   # [Items, quantity_issued]
    for item in settings.inventory_items:
        for log in issued_id:
            if item.get_id() == log[0]:
                issued_items.append([item, log[1]])

    return render_template("issue_page.html", items=issued_items)

def renew():
    if not validate_user():
        return redirect(url_for('home'))
        
    return render_template("renew_page.html")

def return_item():
    if not validate_user():
        return redirect(url_for('home'))
        
    return render_template("return_page.html")
    
def account():
    if not validate_user():
        return redirect(url_for('home'))
        
    return render_template("account.html")

def show_list():
    if not validate_user():
        return redirect(url_for('home'))
        
    return render_template("list_of_components.html", items=settings.inventory_items)

def admin():
    if not validate_user():
        return redirect(url_for('home'))
        
    return render_template("admin_login.html")

def validate_user():
    if 'username' in session and settings.rollno is not None:
        return True
    else:
        return False

# To load data from filename
def load(filename, classname, collection):

    with open(filename, "r") as csvFile:
        data = csv.reader(csvFile)
        flag = False

        for row in data:
            if flag == False:
                flag = True
                pass
            else:
                obj = classname(row)
                collection.append(obj)

# Load data
def load_data():
    dir_path = os.path.dirname(__file__)
    data_dir_path = os.path.join(dir_path, 'data')

    # Get path of files
    student_details_file = os.path.join(data_dir_path, 'student_details.csv')
    inventory_file = os.path.join(data_dir_path, 'inventory_list.csv')
    issue_file = os.path.join(data_dir_path, 'issue_list.csv')
    
    # load from each file
    load(student_details_file, model.StudentDetails, settings.student_details)
    load(inventory_file, model.Inventory, settings.inventory_items)
    load(issue_file, model.Issue, settings.issue_log)