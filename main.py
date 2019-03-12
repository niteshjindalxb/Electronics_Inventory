import csv
from flask import Flask, render_template
app = Flask(__name__)

# Collection of all the admin users
admin_accounts = []
# Collection of items
inventory_items = []


class Issue():
    ID = ""
    rollno = 0

    def get_ID(self):
        return self.ID

    def get_rollno(self):
        return self.rollno


class Inventory():
    ID=""
    Name=""
    Type=""
    Description=""
    Quantity=0
    IssuedQuantity=0

    def get_ID(self):
        return self.ID
    def get_Name(self):
        return self.Name
    def get_Typr(self):
        return self.Type
    def get_Description(self):
        return self.Description
    def get_Quantity(self):
        return self.Quantity
    def get_IssuedQuantity(self):
        return self.IssuedQuantity
    
    
class Details():
    Roll_no=0
    Name=""
    Dept=""
    Year=0
    Fine=0
    def get_Roll_no(self):
        return self.Roll_no
    def get_Name(self):
        return self.Name
    def get_Dept(self):
        return self.Dept
    def  get_Year(self):
        return self.Year
    def get_Fine(self):
        return self.Fine


class Admin():
    UserId=0
    Password=""

    def __init__(self, userId, password):
        self.UserId = userId
        self.Password = password

    def __str__(self):
        return self.UserId

    def get_Userid(self):
        return self.Userid

    def get_Password(self):
        return self.Password


# To load admin users from filename
def load_admin_accounts(filename):

    with open(filename, "r") as csvFile:
        data = csv.reader(csvFile)
        flag = False

        for row in data:
            if flag == False:
                flag = True
                pass
            else:
                obj = Admin(row[0], row[1])
                admin_accounts.append(obj)


@app.route("/")
@app.route("/home/")
def home():
    return render_template('home.html')


# Main function
if __name__ == "__main__":
    # app.run(debug=True)
    load_admin_accounts('accounts.csv')
    for obj in admin_accounts:
        print(obj)