# TODO
# If student details not exists while issuing - ask user to enter details
# Updating file can be improvised
# Fine Calculation
# Limiting renew chances

# Using sql database if possible

from flask import Flask, render_template, redirect, url_for, session, request
# from model import Admin, StudentDetails, Issue, Inventory
from . import model
from . import settings

import os
import csv
import datetime

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
        # os.remove(settings.rollno_file)
        
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

    if request.method == 'POST':
        requested_items = request.form.to_dict()
        # if not validateStudent(settings.rollno):
            # addStudentDetails(requested_items)
            # return redirect(url_for('addStudentDetails'), requested_items)

        date = datetime.datetime.now().strftime("%d-%m-%Y")
        
        # print(requested_items)
        for item in requested_items:
            
            # get item id
            item_id = item
            # quantity required
            req_quantity = int(requested_items[item])

            if req_quantity <= 0:
                continue

            # if required quantity is available then issue
            for avail_item in settings.inventory_items:
                if avail_item.get_id() == item_id:
                    break
            
            if int(avail_item.get_quantity()) - int(avail_item.get_issued_quantity()) >= req_quantity:
                # Increased the issued quantity record
                avail_item.issued_quantity = avail_item.issued_quantity + req_quantity
                new_obj = model.Issue([item_id, settings.rollno, req_quantity, date])
                # Issue item to the user
                settings.issue_log.append(new_obj)
                # Update the issue file
                dump(settings.issue_file, [item_id, settings.rollno, req_quantity, date])
                # Update Inventory file
                # Set header for inventory file
                header = ["ID","Name","Type","Description","Amount(in num)","location","Issued Quantity",""]
                update_file(settings.inventory_file, item_id, req_quantity, settings.inventory_items, header)

    return redirect(url_for('account'))


def update_file(filename, id, quantity, table, header):
    try:
        os.remove(filename)
    except FileNotFoundError:
        print("File doesn't exists")
    else:
        dump(filename, header)
        for row in table:
            data = list(row.__dict__.values())
            dump(filename, data)


def validateStudent(RollNo):
    for stud in settings.student_details:
        if stud.get_rollno() == RollNo:
            return True
    return False

def dump(filename, data):
    try:
        with open(filename, "a+") as f:
            for item in data:
                f.write('"' + str(item) + '"' +",")
            f.write("\n")
    except FileNotFoundError or ValueError:
        print("Error occurs while writing to file", filename)

def renew():
    if not validate_user():
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        requested_items = request.form.to_dict()
        print(requested_items)
        date = datetime.datetime.now().strftime("%d-%m-%Y")

        for issued_item in settings.issue_log:
            if issued_item.get_id() == requested_items['renew']:
                break
        
        issued_item.issued_date = date
        # Update issue file
        header = ["ID","Rollno","Quantity","Issued Date"]
        update_file(settings.issue_file, requested_items['renew'], None, settings.issue_log, header)
    
    return redirect(url_for('account'))

def return_item():
    if not validate_user():
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        requested_items = request.form.to_dict()
        print(requested_items)
        # Remove item from issue list
        for item in settings.issue_log:
            if item.get_id() == requested_items['return']:
                return_amount = item.get_issued_quantity()
                settings.issue_log.remove(item)
                break
        # Decrease issued quantity of item by return_amount in inventory list
        for row in settings.inventory_items:
            if row.get_id() == requested_items['return']:
                row.issued_quantity = int(row.issued_quantity) - int(return_amount)
                break
        # Update issue file
        header = ["ID","Rollno","Quantity","Issued Date"]
        update_file(settings.issue_file, requested_items['return'], None, settings.issue_log, header)
        # Update inventory file
        header = ["ID","Name","Type","Description","Amount(in num)","location","Issued Quantity",""]
        update_file(settings.inventory_file, requested_items['return'], None, settings.inventory_items, header)
        
    return redirect(url_for('account'))
    
def account():
    if not validate_user():
        return redirect(url_for('home'))
        
    for stud in settings.student_details:
        if stud.get_rollno() == settings.rollno:
            break
    
    # list_of_component
    # get all the id of items issued by rollno
    issued_id = []  # [id, quantity_issued, issued date]
    for log in settings.issue_log:
        if log.get_rollno() == settings.rollno:
            issued_id.append([log.get_id(), log.get_issued_quantity(), log.get_issued_date()])

    # Get the items details having ID = id
    # Store the issued item list in issued_item
    issued_items = []   # [Items, quantity_issued, issued_date]
    for item in settings.inventory_items:
        for log in issued_id:
            if item.get_id() == log[0]:
                issued_items.append([item, log[1], log[2]])

    return render_template("account.html", posts={
        'student':stud,
        'items':issued_items,
    })

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

        for row in list(data)[1:]:
            obj = classname(row)
            collection.append(obj)

# Load data
def load_data():
    # Get path of files
    # load from each file
    load(settings.student_details_file, model.StudentDetails, settings.student_details)
    load(settings.inventory_file, model.Inventory, settings.inventory_items)
    load(settings.issue_file, model.Issue, settings.issue_log)