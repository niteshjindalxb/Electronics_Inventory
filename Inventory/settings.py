import os

global admin_accounts, inventory_items, issue_log, student_details
global rollno, rollno_file

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

dir_path = os.path.dirname(__file__)
data_dir_path = os.path.join(dir_path, 'data')

# Get path of files
# File in which current rollno exists
rollno_file = os.path.join(data_dir_path, 'rollno.txt')