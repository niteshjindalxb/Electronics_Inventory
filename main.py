import csv
import os
from flask import Flask, render_template, redirect, url_for, request, session
app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Collection of all the admin users
admin_accounts = []
# Collection of items
inventory_items = []
# Collection of issue logs
issue_log = []
# Collection of student details
student_details = []

# Current active rollno
rollno = None
# File in which current rollno exists
rollno_file = "rollno.txt"

class Issue():
    id = ""
    rollno = 0
    quantity = 0

    def __init__(self, data):
        if data:
            self.id = data[0]
            self.rollno = data[1]
            self.quantity = data[2]

    def get_id(self):
        return self.id

    def get_rollno(self):
        return self.rollno

    def get_issued_quantity(self):
        return self.rollno


class Inventory():
    id=""
    name=""
    type=""
    quantity=0
    location = ""
    issued_quantity=0
    description=""

    def __init__(self,data):
        if data:
            self.id = data[0]
            self.name = data[1]
            self.type = data[2]
            self.description = data[3]
            self.quantity = data[4]
            self.location = data[5]
            if data[6]:
                self.issued_quantity = data[6]
            else:
                self.issued_quantity = 0

    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_type(self):
        return self.type
    def get_description(self):
        return self.description
    def get_quantity(self):
        return self.quantity
    def get_location(self):
        return self.location
    def get_issued_quantity(self):
        return self.issued_quantity
    
    
class StudentDetails():
    rollno=0
    name=""
    fine=0
    remarks=""
    def __init__(self, data):
        if data:
            self.rollno = data[0]
            self.name = data[1]
            self.fine = data[2]
            self.remarks = data[3]

    def get_rollno(self):
        return self.rollno
    def get_name(self):
        return self.name
    def get_fine(self):
        return self.fine
    def  get_remarks(self):
        return self.remarks
    def __str__(self):
        return self.name


class Admin():
    userid=0
    password=""

    def __init__(self, data):
        if data:
            self.userid = data[0]
            self.password = data[1]

    def get_Userid(self):
        return self.userid

    def get_Password(self):
        return self.password

    def __str__(self):
        return self.userid


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


@app.route("/", methods = ['GET', 'POST'])
def home():
    if validate_user():
        return redirect(url_for('dashboard'))

    if os.path.isfile(rollno_file):
        return redirect(url_for('login'))        

    return render_template("home.html")


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if validate_user():
        return redirect(url_for('dashboard'))
        
    global rollno
    global rollno_file

    try:
        with open(rollno_file, "r") as f:
            rollno = f.read()
            
        # Remove the file already read
        os.remove(rollno_file)
        
        session['username'] = rollno
        return redirect(url_for('dashboard'))
    except FileNotFoundError:
        pass

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    global rollno
    # remove the username from the session if it is there
    session.pop(rollno, None)
    rollno = None
    return redirect(url_for('home'))

@app.route("/dashboard/")
def dashboard():
    if not validate_user():
        return redirect(url_for('home'))

    global rollno
    # Find student details with rollno
    cur_student = StudentDetails(None)

    for stud in student_details:
        if int(stud.get_rollno()) == int(rollno):
            cur_student = stud
            break

    return render_template("index.html", student=cur_student)

@app.route("/issue/")
def issue():
    if not validate_user():
        return redirect(url_for('home'))

    global rollno
    # list_of_component
    # get all the id of items issued by rollno
    issued_id = []  # [id, quantity_issued]
    for log in issue_log:
        if log.get_rollno() == rollno:
            issued_id.append([log.get_id(), log.get_quantity()])

    # Get the items details having ID = id
    # Store the issued item list in issued_item
    issued_items = []   # [Items, quantity_issued]
    for item in inventory_items:
        for log in issued_id:
            if item.get_id() == log[0]:
                issued_items.append([item, log[1]])

    return render_template("issue_page.html", items=issued_items)

@app.route("/renew/")
def renew():
    if not validate_user():
        return redirect(url_for('home'))
        
    return render_template("renew_page.html")

@app.route("/return_item/")
def return_item():
    if not validate_user():
        return redirect(url_for('home'))
        
    return render_template("return_page.html")
    
@app.route("/account/")
def account():
    if not validate_user():
        return redirect(url_for('home'))
        
    return render_template("account.html")

@app.route("/show_list/")
def show_list():
    if not validate_user():
        return redirect(url_for('home'))
        
    return render_template("list_of_components.html", items=inventory_items)

@app.route("/admin/")
def admin():
    if not validate_user():
        return redirect(url_for('home'))
        
    return render_template("admin_login.html")

def validate_user():
    global rollno
    if rollno == session['username']:
        return True
    else:
        return False

# Main function
if __name__ == "__main__":
    load("data/student_details.csv", StudentDetails, student_details)
    load("data/inventory_list.csv", Inventory, inventory_items)
    load("data/issue_list.csv", Issue, issue_log)

    app.run(debug=True)