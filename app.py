success_message = ''

try:
    from datetime import datetime, timedelta, date
    import os
    from pymongo import MongoClient
    from flask import Flask, jsonify, request, render_template, redirect, session, url_for, make_response, flash
    from werkzeug.utils import secure_filename
    import numpy as np
    from flask_bcrypt import Bcrypt
    import pandas as pd
    from functools import wraps
    import random
    import os
    from email.message import EmailMessage
    import ssl
    import webbrowser
    import threading
    import time
    import smtplib
except Exception as e:
    success_message = e
    # Log the error or print it for debugging purposes
    

password = "beub kbft vpdx tswm"

dues_data = []

Page_value = ''

try:
    def open_browser():
        time.sleep(1)
        webbrowser.open("http://127.0.0.1:5000")
    app = Flask(__name__)
    app.secret_key = os.urandom(24)  # Generate a secure random key
    bcrypt = Bcrypt(app)
except Exception as e:
    success_message = e
    # Log the error or print it for debugging purposes
    

try:
    current_date = datetime.now().strftime('%d-%m-%Y')
    current_month = datetime.now().strftime('%m')
except Exception as e:
    success_message = e
    # Log the error or print it for debugging purposes
    
try:
    
    client = MongoClient("mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/")
    db = client['Book']
    db1 = client.userdatabase
    users_collection = db1.users
    code_collection = db1.secretnumber
    
except Exception as e:
    success_message = e
    # Log the error or print it for debugging purposes
    


def updateFootfall():
    global success_message
    try:
        # Database and Collection Name
        db = client['Book']
        collection = db['attendance']

        # Get current date, month, and year
        current_date = datetime.now().strftime('%d-%m-%Y')
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Define date strings for the current year, month, and day
        start_of_year = datetime(current_year, 1, 1).strftime('%d-%m-%Y')
        start_of_month = datetime(current_year, current_month, 1).strftime('%d-%m-%Y')

        # Count the documents for the current year
        footfall_year = collection.count_documents({
            'DATE': {'$gte': start_of_year, '$regex': f'{current_year}$'}
        })

        # Count the documents for the current month
        footfall_month = collection.count_documents({
            'DATE': {'$gte': start_of_month, '$regex': f'{current_month:02}-{current_year}$'}
        })

        # Count the documents for the current day
        footfall_day = collection.count_documents({
            'DATE': current_date
        })
    except Exception as e:
        success_message = e
        footfall_year, footfall_month, footfall_day = 0, 0, 0
        

    

    return footfall_year, footfall_month, footfall_day


def updateDue():
    global success_message
    try:
        db = client['Book']
        collection = db['IssueLog']
        data = list(collection.find({}))
    except Exception as e:
        success_message = e
        
        data = []  # Set data to an empty list in case of an error
    return data
dues_data = updateDue()

def updateIssuedCount():
    global success_message
    try:
        db = client['Book']
        collection = db['IssueLog']
        issued_count = collection.count_documents({})
    except Exception as e:
        success_message = e
        
        issued_count = 0  # Set issued_count to 0 in case of an error
    return issued_count


def updateMembersCount():
    global success_message
    try:
        db = client['Book']
        collection = db['Members']
        members_count = collection.count_documents({})
    except Exception as e:
        success_message = e
        
        members_count = 0  # Set members_count to 0 in case of an error
    return members_count
members_count = updateMembersCount()

def updateBookCount():
    global success_message
    try:
        db = client['Book']
        collection = db['BookData']
        query = {'Status': {'$regex': '^available$', '$options': 'i'},'DOCTYPE':{'$regex': '^book$', '$options': 'i'}}
        book_available = collection.count_documents(query)
        
    except Exception as e:
        success_message = e
        
        book_available = 0  # Set book_available to 0 in case of an error
    return book_available


def total_books():
    global success_message
    try:
        db = client['Book']
        collection = db['BookData']
        totalbooks = collection.count_documents({})
    except Exception as e:
        success_message = e
        
        totalbooks = 0  # Set totalbooks to 0 in case of an error
    return totalbooks


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('index'))
        return f(*args, **kwargs)

    return decorated_function


def encrypt_password(password):
    global success_message
    try:
        bcrypt = Bcrypt()
        return bcrypt.generate_password_hash(password).decode('utf-8')
    except Exception as e:
        success_message = e
        


def send_email(code):
    global success_message
    try:
        email_sender = "libraryautomation218@gmail.com"
        email_password = password
        email_receiver = "mation218@gmail.comlibraryauto"

        subject = "New code"
        body = f"New Code : {code}"
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            
    except Exception as e:
        success_message = e
        


def authenticate_code(given_code):
    global success_message
    try:
        # Retrieve the hashed code from the database
        stored_code_doc = code_collection.find_one({})

        if stored_code_doc:
            stored_code = stored_code_doc.get('code')

            # Check if the given code matches the stored hashed code
            if bcrypt.check_password_hash(stored_code, given_code):
                
                # Generate new random code
                new_code = str(random.randint(100000, 999999))
               
                send_email(str(new_code))
                hashed_new_code = encrypt_password(new_code)
                # Update the code in the database
                result = code_collection.update_one(
                    {"_id": stored_code_doc["_id"]},
                    {"$set": {"code": hashed_new_code}}
                )
                if result.modified_count > 0:
                    
                    return True
                else:
                    print("")
                return True
        
        return False
    except Exception as e:
        success_message = e
        


def check_credentials(username, password, Page_value):
    global success_message
    try:
        db1 = client.userdatabase
        users_collection = db1.users
        if Page_value == 'L':
            user = users_collection.find_one({"username": username})
            if username == "librarian" and user and bcrypt.check_password_hash(user['password'], password):
                
                return True
            else:
                
                return False

        if Page_value == 'S':

            user = users_collection.find_one({"username": username})
            if username == "sublibrarian" and user and bcrypt.check_password_hash(user['password'], password):
                
                return True
            else:
                
                return False
    except Exception as e:
        success_message = e
        


@app.route('/')
def index():
    global success_message
    global Page_value
    try:
        return render_template("index.html", success_message="Welcome", Page_value=Page_value)
    except Exception as e:
       
        return render_template("error.html", success_message="An error occurred while loading the page")


@app.route('/api/get_footfall')
@login_required
def get_footfall():
    global success_message
    try:
        footfall_year, footfall_month, footfall_day = updateFootfall()
        return jsonify({
            'footfall_year': footfall_year,
            'footfall_month': footfall_month,
            'footfall_day': footfall_day
        })
    except Exception as e:
        success_message = e
        
        return jsonify({'error': 'An error occurred while fetching footfall data'})


@app.route('/api/get_bookcount')
@login_required
def get_bookcount():
    global success_message
    try:
        book_count = updateBookCount()
        return jsonify({'book_count': book_count})
    except Exception as e:
        success_message = e
        
        return jsonify({'error': 'An error occurred while fetching book count data'})


@app.route('/api/get_issuedcount')
@login_required
def get_issuedcount():
    global success_message
    try:
        issued_count = updateIssuedCount()
        return jsonify({'issued_count': issued_count})
    except Exception as e:
        success_message = e
        
        return jsonify({'error': 'An error occurred while fetching issued count data'})


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    global success_message
    try:
        session.pop('logged_in', None)
        session.clear()
        return redirect('/')
    except Exception as e:
        success_message = e
        
        return render_template("error.html", success_message="An error occurred while logging out")


@app.route('/redirected_page')
@login_required
def redirected_page():
    global Page_value
    try:
        if 'logged_in' in session and session['logged_in']:
            if Page_value == 'L':
                return redirect("/librarianDashboard")
            if Page_value == 'S':
                return redirect("/sublibrarianDashboard")
        else:
            return redirect('/')
    except Exception as e:
        
        return render_template("index.html", success_message="An error occurred while loading the redirected page")


@app.route('/toggle', methods=['POST'])

def toggle():
    try:
        global Page_value
        toggle_value = request.form.get('toggle_value')
        username = request.form.get('username')
        password = request.form.get('password')

        if toggle_value == "left_value":
            Page_value = 'L'
            if check_credentials(username, password, Page_value):
                Page_value = 'L'
                session['logged_in'] = True
                session['Page_value'] = Page_value
                return redirect('/redirected_page')
        elif toggle_value == "right_value":
            Page_value = 'S'
            if check_credentials(username, password, Page_value):
                Page_value = 'S'
                session['logged_in'] = True
                session['Page_value'] = Page_value
                return redirect('/redirected_page')

        return render_template('index.html', success_message="Invalid Credentials")
    except Exception as e:
        
        return render_template("index.html", success_message="An error occurred while processing the request")


@app.route('/reset_password', methods=['POST'])

def reset_password():
    try:
        db1 = client.userdatabase
        users_collection = db1.users
        code_collection = db1.secretnumber
        global Page_value
        reset_value = request.form.get('toggle_value')
        user_entered_key = request.form['secret_key']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        username = request.form["user_name"]

        if authenticate_code(user_entered_key):
            if reset_value == "right_value" and username == "sublibrarian":
                hashed_new_password = encrypt_password(new_password)
                result = users_collection.update_one(
                    {"username": username},
                    {"$set": {"password": hashed_new_password}}
                )
                if result.modified_count > 0:
                    
                    return render_template("index.html", success_message="Password updated successfully")
                else:
                    
                    return render_template("forgot_password.html", success_message="Unexpected Error")
            elif reset_value == "left_value":
                hashed_new_password = encrypt_password(new_password)
                result = users_collection.update_one(
                    {"username": username},
                    {"$set": {"password": hashed_new_password}}
                )
                if result.modified_count > 0:
                    
                    return render_template("index.html", success_message="Password updated successfully")
                else:
                    
                    return render_template("forgot_password.html", success_message="Unexpected Error")
        else:
            return render_template("forgot_password.html", success_message="Incorrect institutional key")

        # Password rules checks
        if len(new_password) < 8:
            return render_template("forgot_password.html", success_message="Password is less than 8 characters")
        if new_password != confirm_password:
            return render_template("forgot_password.html", success_message="Passwords did not match")
        if not any(char.isdigit() for char in new_password):
            return render_template("forgot_password.html", success_message="Password must contain at least one digit")
        if not any(char.isalpha() for char in new_password):
            return render_template("forgot_password.html", success_message="Password must contain at least one letter")
        if new_password.islower():
            return render_template("forgot_password.html",
                                   success_message="Password must contain at least one uppercase letter")
        if new_password.isupper():
            return render_template("forgot_password.html",
                                   success_message="Password must contain at least one lowercase letter")
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in new_password):
            return render_template("forgot_password.html",
                                   success_message="Password must contain at least one special character")
        else:
            return render_template("forgot_password.html", success_message="Username doesn't match")
    except Exception as e:
        
        return render_template("index.html", success_message="An error occurred while processing the request")


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    try:
        global Page_value
        return render_template('forgot_password.html')
    except Exception as e:
        
        return render_template("index.html",
                               success_message="An error occurred while rendering the forgot password page")

client = MongoClient("mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/")
db = client['Book']
@app.route('/view_dues')
@login_required
def view_page():
    try:
        issue_log = db['IssueLog']
        due_log = db['due_log']
        dues_data = list(issue_log.find())

        current_date = datetime.now()
        for due in dues_data:
            due_date = datetime.strptime(due['DUEDATE'], '%d-%m-%Y')
            difference = (due_date - current_date).days + 1
            if difference < 0:
                due_log.insert_one(due)
                issue_log.delete_one({'_id': due['_id']})
            
            elif difference == 0:
                due['DIFFERENCE'] = "Today"
            elif difference == 1:
                due['DIFFERENCE'] = f"{difference} day"
            else:
                due['DIFFERENCE'] = f"{difference} days" 
        
        return render_template('view_dues.html', dues_data=dues_data)
    except Exception as e:
        
        return render_template("dashboard.html", success_message="An error occurred while rendering the view dues page", dues_data=dues_data, members_count=members_count)

client = MongoClient("mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/")
db = client['Book']
@app.route('/subview_dues')
@login_required
def subview_page():
    try:
        issue_log = db['IssueLog']
        due_log = db['due_log']
        dues_data = list(issue_log.find())

        current_date = datetime.now()
        for due in dues_data:
            due_date = datetime.strptime(due['DUEDATE'], '%d-%m-%Y')
            difference = (due_date - current_date).days + 1
            if difference < 0:
                due_log.insert_one(due)
                issue_log.delete_one({'_id': due['_id']})
            
            elif difference == 0:
                due['DIFFERENCE'] = "Today"
            elif difference == 1:
                due['DIFFERENCE'] = f"{difference} day"
            else:
                due['DIFFERENCE'] = f"{difference} days"

        return render_template('view_duessub.html', dues_data=dues_data)
    except Exception as e:
        
        return render_template("dashboardsub.html",
                               success_message="An error occurred while rendering the forgot password page", dues_data=dues_data, members_count=members_count)

client = MongoClient("mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/")
db = client['Book']
@app.route('/librarianDashboard')
@login_required
def dashboard():
    try:
        # Fetch data from IssueLog collection
        issue_log = db['IssueLog']
        due_log = db['due_log']
        dues_data = list(issue_log.find())

        current_date = datetime.now()

        for due in dues_data:
            due_date = datetime.strptime(due['DUEDATE'], '%d-%m-%Y')
            difference = (due_date - current_date).days + 1

            # Move overdue books to due_log and delete from IssueLog
            if difference < 0:
                due_log.insert_one(due)
                issue_log.delete_one({'_id': due['_id']})
            
            elif difference == 0:
                due['DIFFERENCE'] = "Today"
            elif difference == 1:
                due['DIFFERENCE'] = f"{difference} day"
            else:
                due['DIFFERENCE'] = f"{difference} days"    

        # After moving overdue books, fetch the updated dues_data
        #dues_data = list(issue_log.find())

        members_count = updateMembersCount()
        return render_template('dashboard.html', dues_data=dues_data, members_count=members_count)
    except Exception as e:
       
        return render_template("index.html", success_message="An error occurred while rendering the dashboard")

client = MongoClient("mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/")
db = client['Book']
@app.route('/sublibrarianDashboard')
@login_required
def subdashboard():
    try:
        global dues_data
        dues_data = updateDue()
        
        issue_log = db['IssueLog']
        due_log = db['due_log']
        dues_data = list(issue_log.find())
        current_date = datetime.now()

        for due in dues_data:
            due_date = datetime.strptime(due['DUEDATE'], '%d-%m-%Y')
            difference = (due_date - current_date).days + 1

            # Move overdue books to due_log and delete from IssueLog
            if difference < 0:
                due_log.insert_one(due)
                issue_log.delete_one({'_id': due['_id']})
            else:
                if difference == 0:
                    due['DIFFERENCE'] = "Today"
                elif difference == 1:
                    due['DIFFERENCE'] = f"{difference} day"
                else:
                    due['DIFFERENCE'] = f"{difference} days"

        # After moving overdue books, fetch the updated dues_data
        #dues_data = list(issue_log.find())

        members_count = updateMembersCount()
        return render_template('dashboardsub.html', dues_data=dues_data, members_count=members_count)
    except Exception as e:
        return render_template("index.html", success_message="An error occurred while rendering the subdashboard")


# add book page inside inventory
@app.route('/abook', methods=['GET', 'POST'])
@login_required
def abook():
    try:
        return render_template('inventory_book_add.html')
    except Exception as e:
        
        return render_template("inventory.html", success_message="An error occurred while rendering the add book page", totalbooks=tb)


# Add member page
@app.route('/student', methods=['GET', 'POST'])
@login_required
def student():
    try:
        return render_template('student.html')
    except Exception as e:
        
        return render_template("dashboard.html", success_message="An error occurred while rendering the student page", dues_data=dues_data, members_count=members_count)
    
@app.route('/studentedit', methods=['GET', 'POST'])
@login_required
def studentedit():
    try:
        return render_template('studentedit.html')
    except Exception as e:

        return render_template("dashboard.html", success_message="An error occurred while rendering the student page", dues_data=dues_data, members_count=members_count)


@app.route('/studentremove', methods=['GET', 'POST'])
@login_required
def studentremove():
    try:
        return render_template('studentremove.html')
    except Exception as e:

        return render_template("dashboard.html", success_message="An error occurred while rendering the student page", dues_data=dues_data, members_count=members_count)



@app.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    try:
        global tb
        tb = total_books()
        return render_template('inventory.html', totalbooks=tb)
    except Exception as e:
        
        return render_template("dashboard.html", success_message="An error occurred while rendering the inventory page", dues_data=dues_data, members_count=members_count)


@app.route('/subinventory', methods=['GET', 'POST'])
@login_required
def subinventory():
    try:
        tb = total_books()
        return render_template('inventorysub.html', totalbooks=tb)
    except Exception as e:
        
        return render_template("dashboardsub.html",
                               success_message="An error occurred while rendering the subinventory page", dues_data=dues_data, members_count=members_count)


# BACKEND CODE FOR ADD MEMBERS
@app.route('/log_stu', methods=['POST'])
@login_required
def log_stu():
    try:
        user_id = request.form.get('user_id').strip().upper()
        name = request.form.get('name').strip()
        designation = request.form.get('designation').strip().capitalize()
        dept = request.form.get('dept').strip().upper()
        year = request.form.get('year').strip()
        mail = request.form.get('mail').strip()
        phone = request.form.get('phone_no').strip()

        db = client['Book']
        collection = db['Members']
        data=list(collection.find({"REGISTERNO": user_id}, {'_id': 0}))


        if data==[]:
            if designation == 'Student' or designation == 'Staff':
                student = {
                    'REGISTERNO': user_id,
                    'NAME': name,
                    'DESIGNATION': designation,
                    'DEPARTMENT': dept,
                    'YEAR': year,
                    'PHONE': phone,
                    'MAIL': mail
                }
                collection.insert_one(student)
                success_message = 'Student data added successfully!'

            else:
                success_message = 'Invalid Designation'

        else:
            success_message='Member ID already exists!'

        return render_template('student.html', success_message=success_message)
    except Exception as e:

        return render_template("student.html", success_message="An error occurred while trying to add data ")

@app.route('/stu_edit', methods=['POST'])
@login_required
def stu_edit():
    try:
        db = client['Book']
        collection = db['Members']
        regno = request.form.get('user_id')
        btn = request.form.get('submit')
        if btn=='submit':
            data=collection.find_one({"REGISTERNO": regno}, {'_id': 0})

            if data:
                return render_template('studentedit.html',found=data,regno=regno)
            else:
                return render_template('studentedit.html',success_message='User Not found')

        elif btn=='update':
            regno = request.form.get('user_id').strip().upper()
            name = request.form.get('name').strip()
            designation = request.form.get('designation').strip().capitalize()
            dept = request.form.get('dept').strip().upper()
            year = request.form.get('year').strip()
            mail = request.form.get('mail').strip()
            phone = request.form.get('phone_no').strip()
            data = collection.find_one({"REGISTERNO": regno}, {'_id': 0})
            collection.delete_one({"REGISTERNO": regno})

            student = {
                'REGISTERNO':regno,
                'NAME':name,
                'MAIL':mail,
                'YEAR':year,
                'DESIGNATION':designation,
                'DEPARTMENT':dept,
                'PHONE':phone,
            }
            if 'ROLLNO' in data:
                student['ROLLNO'] = data['ROLLNO']
            if 'GENDER' in data:
                student['GENDER'] = data['GENDER']
            if 'FATHERNAME' in data:
                student['FATHERNAME'] = data['FATHERNAME']
            if 'DATE OF BIRTH' in data:
                student['DATE OF BIRTH'] = data['DATE OF BIRTH']
            collection.insert_one(student)

            return render_template('studentedit.html', success_message='Updated Succesfully')
    except Exception as e:
        return render_template("studentedit.html", success_message="An error occurred while trying to update data ")

@app.route('/stu_remove', methods=['POST'])
@login_required
def stu_remove():
    try:
        db = client['Book']
        collection = db['Members']
        regno = request.form.get('user_id')
        btn = request.form.get('submit')
        if btn=='submit':
            data=collection.find_one({"REGISTERNO": regno}, {'_id': 0})
            if data:
                return render_template('studentremove.html',found=data,regno=regno)
            else:
                return render_template('studentremove.html',success_message='User Not Found!')

        elif btn=='remove':
            collection.delete_one({"REGISTERNO": regno})
            return render_template('studentremove.html', success_message='Removed Succesfully')

    except Exception as e:
        return render_template("studentremove.html", success_message="An error occurred while trying to Remove data ")


# Backend for add books
@app.route('/log_book', methods=['POST'])
@login_required
def log_book():
    try:
        acc_no = request.form.get('acc_no').strip()
        call_no = request.form.get('call_no').strip()
        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        edition = request.form.get('edition').strip()
        year = request.form.get('year').strip()
        page_no = request.form.get('page_no').strip()
        price = request.form.get('price').strip()
        isbn = request.form.get('isbn').strip()
        location = request.form.get('location').strip()
        sub_title = request.form.get('sub_title').strip()
        book_ava = 'available'
        db = client['Book']
        collection = db['BookData']
        data=list(collection.find({"ACC":  acc_no}, {'_id': 0}))
        if data==[]:
            book = {
                'ACC': acc_no,
                'CALLNO': int(call_no),
                'TITLE': title,
                'SUB TITLE': sub_title,
                'AUTHOR': author,
                'EDITION': edition,
                'YEAR': year,
                'PAGE NO': page_no,
                'PRICE': price,
                'ISBN': isbn,
                'Location': location,
                'Status': book_ava,
                'DOCTYPE':'Book'
            }

            collection.insert_one(book)
            success_message = 'Book added Successfully!'

        else:
            success_message='Access Number Exists!'
        
        return render_template('inventory_book_add.html', success_message=success_message)
    except Exception as e:
        return render_template("inventory_book_add.html", success_message="An error occurred while trying to add data ")


# import book as csv in add book page
@app.route('/import_book_csv', methods=['POST'])
@login_required
def import_book_csv():
    try:
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/')
        client = MongoClient(mongo_uri)
        db = client['Book']  # Database name
        collection = db['BookData']  # Collection name

        if 'csv_file' not in request.files:
            flash('No file part')
            return redirect('/')

        csv_file = request.files['csv_file']

        if csv_file.filename == '':
            flash('No selected file')
            return redirect('/')

        if csv_file and csv_file.filename.endswith('.csv'):
            filename = secure_filename(csv_file.filename)

            # Ensure the temporary directory exists
            temp_dir = os.path.join(app.root_path, 'tmp')
            os.makedirs(temp_dir, exist_ok=True)

            # Save the file to the temporary directory
            temp_file_path = os.path.join(temp_dir, filename)
            csv_file.save(temp_file_path)

            # Process the CSV file and insert data into MongoDB
            try:

                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes
                df['ACC'] = df['ACC'].astype(str)
                df['CALLNO'] = pd.to_numeric(df['CALLNO'], errors='coerce').fillna(0)
                df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce').fillna(0).astype(np.int64)

                data = df.to_dict(orient='records')

                if data:
                    collection.insert_many(data)

                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:

                    flash('CSV file is empty')
            except Exception as e:

                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

            return render_template("inventory_book_add.html", success_message="Book file imported successfully")
        else:

            flash('Invalid file type. Please upload a CSV file.')
            return redirect('/')
    except Exception as e:

        return render_template("inventory_book_add.html", success_message="An error occurred while trying to add data ")


@app.route('/import_cds_csv', methods=['POST'])
@login_required
def import_cds_csv():
    try:
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/')
        client = MongoClient(mongo_uri)
        db = client['Book']  # Database name
        collection = db['CDs']
        collection2 = db['BookData']  # Collection name

        if 'csv_file' not in request.files:
            flash('No file part')
            return redirect('/')

        csv_file = request.files['csv_file']

        if csv_file.filename == '':
            flash('No selected file')
            return redirect('/')

        if csv_file and csv_file.filename.endswith('.csv'):
            filename = secure_filename(csv_file.filename)

            # Ensure the temporary directory exists
            temp_dir = os.path.join(app.root_path, 'tmp')
            os.makedirs(temp_dir, exist_ok=True)

            # Save the file to the temporary directory
            temp_file_path = os.path.join(temp_dir, filename)
            csv_file.save(temp_file_path)

            # Process the CSV file and insert data into MongoDB
            try:
                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes

                df['ACC'] = df['ACC'].astype(str)

                df['CATALOGNO'] = pd.to_numeric(df['CATALOGNO'], errors='coerce').fillna(0)
                df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce').fillna(0).astype(np.int64)

                data = df.to_dict(orient='records')

                if data:
                    collection.insert_many(data)
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    print("")
            try:
                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes

                df['ACC'] = df['ACC'].astype(str)

                df['CATALOGNO'] = pd.to_numeric(df['CATALOGNO'], errors='coerce').fillna(0)
                df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce').fillna(0).astype(np.int64)

                data = df.to_dict(orient='records')

                if data:
                    collection2.insert_many(data)
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            return render_template("inventory_cds_add.html", success_message="CDs file imported successfully")
        else:
            flash('Invalid file type. Please upload a CSV file.')
            return redirect('/')
    except Exception as e:
        return render_template("inventory_cds_add.html", success_message="An error occurred while trying to add data ")


@app.route('/import_thesis_csv', methods=['POST'])
@login_required
def import_thesis_csv():
    try:
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/')
        client = MongoClient(mongo_uri)
        db = client['Book']  # Database name
        collection = db['Thesis']
        collection2 = db['BookData']  # Collection name

        if 'csv_file' not in request.files:
            flash('No file part')
            return redirect('/')

        csv_file = request.files['csv_file']

        if csv_file.filename == '':
            flash('No selected file')
            return redirect('/')

        if csv_file and csv_file.filename.endswith('.csv'):
            filename = secure_filename(csv_file.filename)

            # Ensure the temporary directory exists
            temp_dir = os.path.join(app.root_path, 'tmp')
            os.makedirs(temp_dir, exist_ok=True)

            # Save the file to the temporary directory
            temp_file_path = os.path.join(temp_dir, filename)
            csv_file.save(temp_file_path)

            # Process the CSV file and insert data into MongoDB
            try:

                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes

                df['ACC'] = df['ACC'].astype(str)

                data = df.to_dict(orient='records')

                if data:
                    collection.insert_many(data)
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    print("")

            try:

                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes

                df['ACC'] = df['ACC'].astype(str)

                data = df.to_dict(orient='records')

                if data:
                    collection2.insert_many(data)
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

            return render_template("inventory_thesis_add.html", success_message="Thesis file imported successfully")
        else:
            flash('Invalid file type. Please upload a CSV file.')
            return redirect('/')
    except Exception as e:
        return render_template("inventory_thesis_add.html",
                               success_message="An error occurred while trying to add data ")


@app.route('/import_journals_csv', methods=['POST'])
@login_required
def import_journals_csv():
    try:
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/')
        client = MongoClient(mongo_uri)
        db = client['Book']  # Database name
        collection = db['Journals']
        collection2 = db['BookData']  # Collection name

        if 'csv_file' not in request.files:
            flash('No file part')
            return redirect('/')

        csv_file = request.files['csv_file']

        if csv_file.filename == '':
            flash('No selected file')
            return redirect('/')

        if csv_file and csv_file.filename.endswith('.csv'):
            filename = secure_filename(csv_file.filename)

            # Ensure the temporary directory exists
            temp_dir = os.path.join(app.root_path, 'tmp')
            os.makedirs(temp_dir, exist_ok=True)

            # Save the file to the temporary directory
            temp_file_path = os.path.join(temp_dir, filename)
            csv_file.save(temp_file_path)

            # Process the CSV file and insert data into MongoDB
            try:

                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes

                df['ACC'] = df['ACC'].astype(str)

                df['ISSUENO'] = pd.to_numeric(df['ISSUENO'], errors='coerce').fillna(0).astype(np.int64)
                df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce').fillna(0).astype(np.int64)

                data = df.to_dict(orient='records')

                if data:
                    collection.insert_many(data)
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    print("")

            try:

                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes

                df['ACC'] = df['ACC'].astype(str)

                df['ISSUENO'] = pd.to_numeric(df['ISSUENO'], errors='coerce').fillna(0).astype(np.int64)
                df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce').fillna(0).astype(np.int64)

                data = df.to_dict(orient='records')

                if data:
                    collection2.insert_many(data)
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

            return render_template("inventory_journals_add.html", success_message="Journal file imported successfully")
        else:
            flash('Invalid file type. Please upload a CSV file.')
            return redirect('/')
    except Exception as e:
        return render_template("inventory_journals_add.html",
                               success_message="An error occurred while trying to add data ")


@app.route('/import_projects_csv', methods=['POST'])
@login_required
def import_projects_csv():
    try:
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/')
        client = MongoClient(mongo_uri)
        db = client['Book']  # Database name
        collection = db['Projects']
        collection2 = db['BookData']  # Collection name

        if 'csv_file' not in request.files:
            flash('No file part')
            return redirect('/')

        csv_file = request.files['csv_file']

        if csv_file.filename == '':
            flash('No selected file')
            return redirect('/')

        if csv_file and csv_file.filename.endswith('.csv'):
            filename = secure_filename(csv_file.filename)

            # Ensure the temporary directory exists
            temp_dir = os.path.join(app.root_path, 'tmp')
            os.makedirs(temp_dir, exist_ok=True)

            # Save the file to the temporary directory
            temp_file_path = os.path.join(temp_dir, filename)
            csv_file.save(temp_file_path)

            # Process the CSV file and insert data into MongoDB
            try:

                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes

                df['ACC'] = df['ACC'].astype(str)
                df['MEMBERS'] = df['MEMBERS'].astype(str)

                data = df.to_dict(orient='records')

                if data:
                    collection.insert_many(data)
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    print("")
            try:

                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes

                df['ACC'] = df['ACC'].astype(str)
                df['MEMBERS'] = df['MEMBERS'].astype(str)
                data = df.to_dict(orient='records')

                if data:
                    collection2.insert_many(data)
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            return render_template("inventory_projects_add.html", success_message="Projects file imported successfully")
        else:
            flash('Invalid file type. Please upload a CSV file.')
            return redirect('/')
    except Exception as e:
        return render_template("inventory_projects_add.html",
                               success_message="An error occurred while trying to add data ")


@app.route('/import_eresource_csv', methods=['POST'])
@login_required
def import_eresource_csv():
    try:

        db = client['Book']  # Database name
        collection = db['E_Resource']
        collection2 = db['BookData']  # Collection name

        if 'csv_file' not in request.files:
            flash('No file part')
            return redirect('/')

        csv_file = request.files['csv_file']

        if csv_file.filename == '':
            flash('No selected file')
            return redirect('/')

        if csv_file and csv_file.filename.endswith('.csv'):
            filename = secure_filename(csv_file.filename)

            # Ensure the temporary directory exists
            temp_dir = os.path.join(app.root_path, 'tmp')
            os.makedirs(temp_dir, exist_ok=True)

            # Save the file to the temporary directory
            temp_file_path = os.path.join(temp_dir, filename)
            csv_file.save(temp_file_path)

            # Process the CSV file and insert data into MongoDB
            try:

                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes

                df['ACC'] = df['ACC'].astype(str)

                data = df.to_dict(orient='records')

                if data:
                    collection.insert_many(data)
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    print("")
            try:

                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes

                df['ACC'] = df['ACC'].astype(str)

                data = df.to_dict(orient='records')

                if data:
                    collection2.insert_many(data)
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            return render_template("inventory_eresource_add.html",
                                   success_message="E-Resource file imported successfully")
        else:
            flash('Invalid file type. Please upload a CSV file.')
            return redirect('/')
    except Exception as e:
        return render_template("inventory_eresource_add.html",
                               success_message="An error occurred while trying to add data ")


# import student csv file from add member page
@app.route('/import_csv', methods=['POST'])
@login_required
def import_csv():
    try:
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb+srv://Monica:libraryautomation@cluster0.feu2lx8.mongodb.net/')
        client = MongoClient(mongo_uri)
        db = client['Book']  # Database name
        collection1 = db['Members']
        collection2 = db['AttendanceStudentData']  # Collection name
        
        if 'csv_file' not in request.files:
            flash('No file part')
            return redirect('/student')

        csv_file = request.files['csv_file']

        if csv_file.filename == '':
            flash('No selected file')
            return redirect('/student')

        if csv_file and csv_file.filename.endswith('.csv'):
            filename = secure_filename(csv_file.filename)

            # Ensure the temporary directory exists
            temp_dir = os.path.join(app.root_path, 'tmp')
            os.makedirs(temp_dir, exist_ok=True)

            # Save the file to the temporary directory
            temp_file_path = os.path.join(temp_dir, filename)
            csv_file.save(temp_file_path)

            # Process the CSV file and insert data into MongoDB
            try:
                
                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes
                
                df['REGISTERNO'] = df['REGISTERNO'].astype(str)
                df['PHONE'] = df['PHONE'].astype(np.int64)

                # df['another_column'] = pd.to_datetime(df['another_column'])  # Example conversion
                
                # Convert DataFrame to a list of dictionaries
                data = df.to_dict(orient='records')

                if data:
                    collection1.insert_many(data)
                    
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    print("")

            try:
                
                # Read the CSV file with pandas
                df = pd.read_csv(temp_file_path)

                # Convert column datatypes
                
                df['REGISTERNO'] = df['REGISTERNO'].astype(str)

                # df['another_column'] = pd.to_datetime(df['another_column'])  # Example conversion
                
                # Convert DataFrame to a list of dictionaries
                data = df.to_dict(orient='records')

                if data:
                    collection2.insert_many(data)
                    
                    flash('CSV file successfully imported and data uploaded to MongoDB')
                else:
                    flash('CSV file is empty')
            except Exception as e:
                # logger.error(f'Error processing CSV file: {e}')
                flash(f'Error processing CSV file: {e}')
            finally:
                # Ensure the temporary file is deleted
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

            return redirect('/student')
        else:
            flash('Invalid file type. Please upload a CSV file.')
            return redirect('/student')
    except Exception as e:
        return render_template("student.html", success_message="An error occurred while trying to add data ")


@app.route('/searchmember', methods=['GET', 'POST'])
@login_required
def M_search():
    try:
        return render_template('searchmember.html')
    except Exception as e:
        return render_template("dashboard.html",
                               success_message="An error occurred while rendering the search member page", dues_data=dues_data, members_count=members_count)


# Backend for search member page
@app.route('/msearch', methods=['POST'])
@login_required
def mem_input():
    try:
        reg_no = request.form.get('user_id').strip().upper()
        name = request.form.get('name').strip()
        designation = request.form.get('designation').strip().capitalize()
        dept = request.form.get('dept').strip().upper()
        year = request.form.get('year').strip()
        phone_no = request.form.get('phone_no').strip()
        db = client['Book']
        collection = db['Members']

        if reg_no != '':
            data = list(collection.find({"REGISTERNO": reg_no}, {'_id': 0, 'SNO': 0, }))
            

        else:
            if phone_no != '':
                data = list(collection.find({"PHONE": int(phone_no)}, {'_id': 0, 'SNO': 0, }))
                

            else:
                if name != '' and designation == '' and dept == '' and year == '':
                    data = list(collection.find({"NAME": {"$regex": name,"$options": "i"}}, {'_id': 0, 'SNO': 0, }))


                elif name == '' and designation != '' and dept == '' and year == '':
                    data = list(collection.find({"DESIGNATION": {"$regex": designation}}, {'_id': 0, 'SNO': 0, }))

                    

                elif name == '' and designation == '' and dept != '' and year == '':
                    data = list(collection.find({"DEPARTMENT": dept}, {'_id': 0, 'SNO': 0, }))
                    

                elif name == '' and designation == '' and dept == '' and year != '':
                    data = list(collection.find({"YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation != '' and dept == '' and year == '':
                    data = list(
                        collection.find({"NAME": {"$regex": name,"$options": "i"}, "DESIGNATION": {"$regex": designation}}, {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation == '' and dept != '' and year == '':
                    data = list(collection.find({"NAME": {"$regex": name,"$options": "i"}, "DEPARTMENT": dept}, {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation == '' and dept == '' and year != '':
                    data = list(collection.find({"NAME": {"$regex": name,"$options": "i"}, "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif name == '' and designation != '' and dept != '' and year == '':
                    data = list(collection.find({"DESIGNATION": {"$regex": designation}, "DEPARTMENT": dept}, {'_id': 0, 'SNO': 0}))
                    

                elif name == '' and designation != '' and dept == '' and year != '':
                    data = list(collection.find({"DESIGNATION": {"$regex": designation}, "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif name == '' and designation == '' and dept != '' and year != '':
                    data = list(collection.find({"DEPARTMENT": dept, "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation != '' and dept != '' and year == '':
                    data = list(collection.find({"NAME": {"$regex": name,"$options": "i"}, "DESIGNATION": {"$regex": designation}, "DEPARTMENT": dept},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation != '' and dept == '' and year != '':
                    data = list(
                        collection.find({"NAME": {"$regex": name,"$options": "i"}, "DESIGNATION": {"$regex": designation}, "YEAR": int(year)},
                                        {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation == '' and dept != '' and year != '':
                    data = list(
                        collection.find({"NAME": {"$regex": name,"$options": "i"}, "DEPARTMENT": dept, "YEAR": int(year)},
                                        {'_id': 0, 'SNO': 0}))
                    

                elif name == '' and designation != '' and dept != '' and year != '':
                    data = list(collection.find({"DESIGNATION": {"$regex": designation}, "DEPARTMENT": dept, "YEAR": int(year)},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation != '' and dept != '' and year != '':
                    data = list(collection.find(
                        {"NAME": {"$regex": name,"$options": "i"}, "DESIGNATION": {"$regex": designation}, "DEPARTMENT": dept, "YEAR": int(year)},
                        {'_id': 0, 'SNO': 0}))
                    

                else:
                    data = ['Invalid Choice']
                    return render_template('searchmember.html', success_message="Invalid Choice")

        return render_template('searchmember.html', places=data)
    except Exception as e:
        return render_template("searchmember.html", success_message="An error occurred while trying to search data ")


@app.route('/subsearchmember', methods=['GET', 'POST'])
@login_required
def M_search_sub():
    try:
        return render_template('searchmembersub.html')
    except Exception as e:
        return render_template("dashboardsub.html",
                               success_message="An error occurred while rendering the sub search member page", dues_data=dues_data, members_count=members_count)


# Backend for search member page for sublibrarian
@app.route('/submsearch', methods=['POST'])
@login_required
def mem_input_sub():
    try:
        reg_no = request.form.get('user_id').strip().upper()
        name = request.form.get('name').strip()
        designation = request.form.get('designation').strip().capitalize()
        dept = request.form.get('dept').strip().upper()
        year = request.form.get('year').strip()
        phone_no = request.form.get('phone_no').strip()
        db = client['Book']
        collection = db['Members']

        param='.'

        if reg_no != '':
            data = list(collection.find({"REGISTERNO": reg_no}, {'_id': 0, 'SNO': 0, }))
            if data == []:
                success_message = 'Register Number Not valid'
                return render_template('searchmembersub.html', success_message=success_message)
            

        else:
            if phone_no != '':
                data = list(collection.find({"PHONE": int(phone_no)}, {'_id': 0, 'SNO': 0, }))
                
            
            else:
                if name != '' and designation == '' and dept == '' and year == '':
                    data = list(collection.find({"NAME": {"$regex": name,"$options": "i"}}, {'_id': 0, 'SNO': 0, }))
                    
                    

                elif name == '' and designation != '' and dept == '' and year == '':
                    data = list(collection.find({"DESIGNATION": {"$regex": designation}}, {'_id': 0, 'SNO': 0, }))
                    

                elif name == '' and designation == '' and dept != '' and year == '':
                    data = list(collection.find({"DEPARTMENT": dept}, {'_id': 0, 'SNO': 0, }))
                    

                elif name == '' and designation == '' and dept == '' and year != '':
                    data = list(collection.find({"YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation != '' and dept == '' and year == '':
                    data = list(
                        collection.find({"NAME": {"$regex": name,"$options": "i"}, "DESIGNATION": {"$regex": designation}}, {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation == '' and dept != '' and year == '':
                    data = list(collection.find({"NAME": {"$regex": name,"$options": "i"}, "DEPARTMENT": dept}, {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation == '' and dept == '' and year != '':
                    data = list(collection.find({"NAME": {"$regex": name,"$options": "i"}, "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif name == '' and designation != '' and dept != '' and year == '':
                    data = list(collection.find({"DESIGNATION": {"$regex": designation, "DEPARTMENT": dept}}, {'_id': 0, 'SNO': 0}))
                    

                elif name == '' and designation != '' and dept == '' and year != '':
                    data = list(collection.find({"DESIGNATION": {"$regex": designation, "YEAR": int(year)}}, {'_id': 0, 'SNO': 0}))
                    

                elif name == '' and designation == '' and dept != '' and year != '':
                    data = list(collection.find({"DEPARTMENT": dept, "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation != '' and dept != '' and year == '':
                    data = list(collection.find({"NAME": {"$regex": name,"$options": "i"}, "DESIGNATION": {"$regex": designation, "DEPARTMENT": dept}},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation != '' and dept == '' and year != '':
                    data = list(
                        collection.find({"NAME": {"$regex": name,"$options": "i"}, "DESIGNATION": {"$regex": designation, "YEAR": int(year)}},
                                        {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation == '' and dept != '' and year != '':
                    data = list(
                        collection.find({"NAME": {"$regex": name,"$options": "i"}, "DEPARTMENT": dept, "YEAR": int(year)},
                                        {'_id': 0, 'SNO': 0}))
                    

                elif name == '' and designation != '' and dept != '' and year != '':
                    data = list(collection.find({"DESIGNATION": {"$regex": designation}, "DEPARTMENT": dept, "YEAR": int(year)},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif name != '' and designation != '' and dept != '' and year != '':
                    data = list(collection.find(
                        {"NAME": {"$regex": name,"$options": "i"}, "DESIGNATION": {"$regex": designation}, "DEPARTMENT": dept, "YEAR": int(year)},
                        {'_id': 0, 'SNO': 0}))
                    

                else:
                    success_message = 'No Data Found'
                    render_template('searchmembersub.html', success_message=success_message)

        return render_template('searchmembersub.html', places=data)
    except Exception as e:
        return render_template("searchmembersub.html", success_message="An error occurred while trying to search data ")


# report page ------------------------------------------------------------------------------------------

@app.route("/report")
@login_required
def report():
    try:
        return render_template('Report.html')
    except Exception as e:
        return render_template("dashboard.html", success_message="An error occurred while rendering the report page", dues_data=dues_data, members_count=members_count)


# backend for report page
@app.route('/report_gen', methods=['POST'])
@login_required
def report_input():
    global report
    global fro
    global to

    report=request.form.get("report")
    fro = request.form.get("fromDate")
    to = request.form.get("toDate")
    if report=='footfall' or report=='issue' or report=='return' or report=='fine'  or report=='collect':
        if fro != '' and to != '':
            csv_data = report_gen()
            if csv_data[0]!=None:
                response = make_response(csv_data[0])
                response.headers['Content-Type'] = 'text/csv'
                response.headers['Content-Disposition'] = 'attachment; filename={}.csv'.format(csv_data[1])
                return response
            else:
                return render_template('Report.html',success_message=csv_data[2])

        else:
            success_message='Choose Dates to retrieve'
            return render_template('Report.html',success_message=success_message)

    else:
        csv_data = report_gen()
        if csv_data[0]!=None:

            response = make_response(csv_data[0])
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = 'attachment; filename={}.csv'.format(csv_data[1])
            return response
        else:
            return render_template('Report.html', success_message=csv_data[2])

def report_gen():
    global message
    try:
        db = client['Book']
        user_collection = db['Members']

        if report == 'footfall':
            collection = db['attendance']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                for i in data:
                    user=i['REGISTERNO']
                    data1 = user_collection.find_one({"REGISTERNO":user} ,{'_id': 0})
                    if 'MAIL' in data1.keys():
                        i['MAIL'] = data1['MAIL']
                    else:
                        i['MAIL'] = 'NONE'

                d = pd.DataFrame(data)
                d['DATE'] = pd.to_datetime(d['DATE'],dayfirst=True)
                start=pd.to_datetime(fro)
                end=pd.to_datetime(to)
                df=d.loc[(d['DATE'] >= start) & (d['DATE'] <= end)]
                csv = df.to_csv(index=False)
                value = 'Footfall-report'
                message = None

            else:
                csv = None
                value = None
                message = 'No Data Available'


        elif report == 'issue':
            collection = db['IssueLog']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                for i in data:
                    user=i['REGISTERNO']
                    data1 = user_collection.find_one({"REGISTERNO":user} ,{'_id': 0})
                    if 'MAIL' in data1.keys():
                        i['MAIL'] = data1['MAIL']
                    else:
                        i['MAIL'] = 'NONE'

                d = pd.DataFrame(data)
                d['ISSUEDATE'] = pd.to_datetime(d['ISSUEDATE'],dayfirst=True)
                start = pd.to_datetime(fro)
                end = pd.to_datetime(to)
                df = d.loc[(d['ISSUEDATE'] >= start) & (d['ISSUEDATE'] <= end)]
                csv = df.to_csv(index=False)
                value = 'Issue-report'
                message = None

            else:
                csv = None
                value = None
                message = 'No Data Available'

        elif report == 'return':
            collection = db['ReturnLog']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                for i in data:
                    user=i['REGISTERNO']
                    data1 = user_collection.find_one({"REGISTERNO":user} ,{'_id': 0})
                    if 'MAIL' in data1.keys():
                        i['MAIL'] = data1['MAIL']
                    else:
                        i['MAIL'] = 'NONE'

                d = pd.DataFrame(data)
                d['RETURNEDDATE'] = pd.to_datetime(d['RETURNEDDATE'],dayfirst=True)
                start = pd.to_datetime(fro)
                end = pd.to_datetime(to)
                df = d.loc[(d['RETURNEDDATE'] >= start) & (d['RETURNEDDATE'] <= end)]
                csv = df.to_csv(index=False)
                value = 'Return-report'
                message = None

            else:
                csv = None
                value = None
                message = 'No Data Available'

        elif report == 'fine':
            collection = db['due_log']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                for i in data:
                    user=i['REGISTERNO']
                    data1=user_collection.find_one({"REGISTERNO":user} ,{'_id': 0})
                    if 'MAIL' in data1.keys():
                        i['MAIL'] = data1['MAIL']
                    else:
                        i['MAIL'] = 'NONE'

                    d = i['DUEDATE']
                    due = datetime.strptime(d, '%d-%m-%Y').date()
                    current = date.today()
                    days = abs((due - current).days)
                    fine = days * 2
                    i['FINE'] = fine

                d = pd.DataFrame(data)
                d['DUEDATE'] = pd.to_datetime(d['DUEDATE'],dayfirst=True)
                start = pd.to_datetime(fro)
                end = pd.to_datetime(to)
                df = d.loc[(d['DUEDATE'] >= start) & (d['DUEDATE'] <= end)]
                csv = df.to_csv(index=False)
                value = 'Fine-report'
                message = None

            else:
                csv = None
                value = None
                message = 'No Data Available'

        elif report == 'collect':
            collection = db['CollectedCollection']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                d = pd.DataFrame(data)
                d['RETURNEDDATE'] = pd.to_datetime(d['RETURNEDDATE'],dayfirst=True)
                start = pd.to_datetime(fro)
                end = pd.to_datetime(to)
                df = d.loc[(d['RETURNEDDATE'] >= start) & (d['RETURNEDDATE'] <= end)]
                csv = df.to_csv(index=False)
                value = 'Collection-report'
                message = None

            else:
                csv = None
                value = None
                message = 'No Data Available'
        


        elif report == 'acquisition':
            collection = db['BookAcquisition']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                value = 'BooksAcquisition-report'
                message = None

            else:
                csv = None
                value = None
                message = 'No Data Available'

        elif report == 'missing':
            collection = db['Missinglog']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:

                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                value = 'MissingBooks-report'
                message = None
            else:
                csv = None
                value = None
                message = 'No Data Available'

        elif report == 'book':
            collection = db['BookData']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                value = 'Books-report'
                message = None
            else:
                csv = None
                value = None
                message = 'No Data Available'


        elif report == 'user':
            collection = db['Members']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                value = 'Members-report'
                message = None
            else:
                csv = None
                value = None
                message = 'No Data Available'

        elif report == 'cd':
            collection = db['CDs']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                value = 'CDs-report'
                message = None
            else:
                csv = None
                value = None
                message = 'No Data Available'

        elif report == 'thesis':
            collection = db['Thesis']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                value = 'Thesis-report'
                message = None
            else:
                csv = None
                value = None
                message = 'No Data Available'

        elif report == 'journal':
            collection = db['Journals']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                value = 'Journals-report'
                message = None
            else:
                csv = None
                value = None
                message = 'No Data Available'

        elif report == 'eresources':
            collection = db['E_Resources']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                value = 'E-Resources-report'
                message = None
            else:
                csv = None
                value = None
                message = 'No Data Available'
        
        elif report == 'project':
            collection = db['Projects']
            data = list(collection.find({}, {'_id': 0}))
            if data != []:
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                value = 'Projects-report'
                message = None
            else:
                csv = None
                value = None
                message = 'No Data Available'

        else:
            csv = None
            value = None
            message = 'Invalid Choice'

        return csv, value, message

    except Exception as e:
        print(e)
        csv=None
        value=None
        message=e
        return csv,value,message

# --------------------------------------------BOOK SEARCH----------------------------------------------------------------------------------------------- ----------------------------------------------BOOK SEARCH----------------------------------------------------------------------------------------------

@app.route('/booksearch')
@login_required
def booksearch():
    try:
        return render_template('searchbook.html')
    except Exception as e:
        return render_template("dashboard.html",
                               success_message="An error occurred while rendering the bookseach  page", dues_data=dues_data, members_count=members_count)


# backend for book search page
@app.route('/bsearch', methods=['POST'])
def book_input():
    try:
        acc_no = request.form.get('acc_no').strip().upper()
        call_no = request.form.get('call_no').strip()
        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        location = request.form.get('location').strip().upper()
        year = request.form.get('year').strip()

        db = client['Book']
        collection = db['BookData']

        if acc_no != '':
            data = list(collection.find({"ACC":  acc_no}, {'_id': 0, 'SNO': 0, }))
            if data == []:
                return render_template('searchbook.html', success_message="Invalid Access Number")
            

        else:
            if call_no != '':
                data = list(collection.find({"CALLNO": {"$regex": call_no, "$options": "i"}}, {'_id': 0, 'SNO': 0, }))
                

            else:
                if author != '' and title == '' and location == '' and year == '':
                    data = list(
                        collection.find({"AUTHOR": {"$regex": author, "$options": "i"}}, {'_id': 0, 'SNO': 0, }))
                    

                elif author == '' and title != '' and location == '' and year == '':
                    data = list(collection.find({"TITLE": {"$regex": title, "$options": "i"}}, {'_id': 0, 'SNO': 0, }))
                    

                elif author == '' and title == '' and location != '' and year == '':
                    data = list(collection.find({"Location": location}, {'_id': 0, 'SNO': 0, }))
                    

                elif author == '' and title == '' and location == '' and year != '':
                    data = list(collection.find({"YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title != '' and location == '' and year == '':
                    data = list(collection.find(
                        {"AUTHOR": {"$regex": author, "$options": "i"}, "TITLE": {"$regex": title, "$options": "i"}},
                        {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title == '' and location != '' and year == '':
                    data = list(collection.find({"AUTHOR": {"$regex": author, "$options": "i"}, "Location": location},
                                                {'_id': 0, 'SNO': 0}))
                   

                elif author != '' and title == '' and location == '' and year != '':
                    data = list(collection.find({"AUTHOR": {"$regex": author, "$options": "i"}, "YEAR": int(year)},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif author == '' and title != '' and location != '' and year == '':
                    data = list(collection.find({"TITLE": {"$regex": title, "$options": "i"}, "Location": location},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif author == '' and title != '' and location == '' and year != '':
                    data = list(collection.find({"TITLE": {"$regex": title, "$options": "i"}, "YEAR": int(year)},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif author == '' and title == '' and location != '' and year != '':
                    data = list(collection.find({"Location": location, "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title != '' and location != '' and year == '':
                    data = list(collection.find(
                        {"AUTHOR": {"$regex": author, "$options": "i"}, "TITLE": {"$regex": title, "$options": "i"},
                         "Location": location}, {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title != '' and location == '' and year != '':
                    data = list(collection.find(
                        {"AUTHOR": {"$regex": author, "$options": "i"}, "TITLE": {"$regex": title, "$options": "i"},
                         "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title == '' and location != '' and year != '':
                    data = list(collection.find(
                        {"AUTHOR": {"$regex": author, "$options": "i"}, "Location": location, "YEAR": int(year)},
                        {'_id': 0, 'SNO': 0}))
                    

                elif author == '' and title != '' and location != '' and year != '':
                    data = list(collection.find(
                        {"TITLE": {"$regex": title, "$options": "i"}, "Location": location, "YEAR": int(year)},
                        {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title != '' and location != '' and year != '':
                    data = list(collection.find(
                        {"AUTHOR": {"$regex": author, "$options": "i"}, "TITLE": {"$regex": title, "$options": "i"},
                         "Location": location, "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                else:
                    data = ['Invalid Choice']
                    return render_template('searchbook.html', success_message="Invalid Choice")

        return render_template('searchbook.html', places=data)
    except Exception as e:
        return render_template("searchbook.html", success_message="An error occurred while trying to search data ")


@app.route('/subbooksearch')
@login_required
def booksearchsub():
    try:
        return render_template('searchbooksub.html')
    except Exception as e:
        return render_template("dashboardsub.html",
                               success_message="An error occurred while rendering the search book page", dues_data=dues_data, members_count=members_count)


# backend for sub book search
@app.route('/subbsearch', methods=['POST'])
def book_input_sub():
    try:
        acc_no = request.form.get('acc_no').strip().upper()
        call_no = request.form.get('call_no').strip()
        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        location = request.form.get('location').strip().upper()
        year = request.form.get('year').strip()

        db = client['Book']
        collection = db['BookData']

        if acc_no != '':
            data = list(collection.find({"ACC":  acc_no}, {'_id': 0, 'SNO': 0, }))
            

        else:
            if call_no != '':
                data = list(
                    collection.find({"CALLNO": {"$regex": call_no, "$options": "i"}}, {'_id': 0, 'SNO': 0, }))
                

            else:
                if author != '' and title == '' and location == '' and year == '':
                    data = list(
                        collection.find({"AUTHOR": {"$regex": author, "$options": "i"}}, {'_id': 0, 'SNO': 0, }))
                    

                elif author == '' and title != '' and location == '' and year == '':
                    data = list(collection.find({"TITLE": {"$regex": title, "$options": "i"}}, {'_id': 0, 'SNO': 0, }))
                    

                elif author == '' and title == '' and location != '' and year == '':
                    data = list(collection.find({"Location": location}, {'_id': 0, 'SNO': 0, }))
                    

                elif author == '' and title == '' and location == '' and year != '':
                    data = list(collection.find({"YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title != '' and location == '' and year == '':
                    data = list(collection.find(
                        {"AUTHOR": {"$regex": author, "$options": "i"}, "TITLE": {"$regex": title, "$options": "i"}},
                        {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title == '' and location != '' and year == '':
                    data = list(collection.find({"AUTHOR": {"$regex": author, "$options": "i"}, "Location": location},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title == '' and location == '' and year != '':
                    data = list(collection.find({"AUTHOR": {"$regex": author, "$options": "i"}, "YEAR": int(year)},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif author == '' and title != '' and location != '' and year == '':
                    data = list(collection.find({"TITLE": {"$regex": title, "$options": "i"}, "Location": location},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif author == '' and title != '' and location == '' and year != '':
                    data = list(collection.find({"TITLE": {"$regex": title, "$options": "i"}, "YEAR": int(year)},
                                                {'_id': 0, 'SNO': 0}))
                    

                elif author == '' and title == '' and location != '' and year != '':
                    data = list(collection.find({"Location": location, "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title != '' and location != '' and year == '':
                    data = list(collection.find(
                        {"AUTHOR": {"$regex": author, "$options": "i"}, "TITLE": {"$regex": title, "$options": "i"},
                         "Location": location}, {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title != '' and location == '' and year != '':
                    data = list(collection.find(
                        {"AUTHOR": {"$regex": author, "$options": "i"}, "TITLE": {"$regex": title, "$options": "i"},
                         "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title == '' and location != '' and year != '':
                    data = list(collection.find(
                        {"AUTHOR": {"$regex": author, "$options": "i"}, "Location": location, "YEAR": int(year)},
                        {'_id': 0, 'SNO': 0}))
                    

                elif author == '' and title != '' and location != '' and year != '':
                    data = list(collection.find(
                        {"TITLE": {"$regex": title, "$options": "i"}, "Location": location, "YEAR": int(year)},
                        {'_id': 0, 'SNO': 0}))
                    

                elif author != '' and title != '' and location != '' and year != '':
                    data = list(collection.find(
                        {"AUTHOR": {"$regex": author, "$options": "i"}, "TITLE": {"$regex": title, "$options": "i"},
                         "Location": location, "YEAR": int(year)}, {'_id': 0, 'SNO': 0}))
                    

                else:
                    data = ['Invalid Choice']
                    return render_template('searchbooksub.html', success_message="Invalid Choice")

        return render_template('searchbooksub.html', places=data)
    except Exception as e:
        return render_template("searchbooksub.html", success_message="An error occurred while trying to search data ")


# ----------------------------------------- book manager -------------------------------------------------------------------


@app.route('/bookmanager')
@login_required
def bookmanager():
    try:
        return render_template('bookmanager.html')
    except Exception as e:
        
        return render_template("dashboard.html", success_message="An error occurred while rendering the bookmanger page", dues_data=dues_data, members_count=members_count)


global user_id
global acc_no


# search button for given register no and user id in bookmanager
@app.route('/submit', methods=['POST'])
@login_required
def handle_submit():
    try:
        user_id = request.form.get('user_id').upper()
        acc_no = request.form.get('acc_no')
        action = request.form.get('action')

        if not user_id:
            return render_template('bookmanager.html', error="User ID is required",
                                   success_message="User ID is required")

        if action == 'submit':
            return submit_data(user_id, acc_no)
        elif action == 'issue':
            acc_no = request.form.get('acc_no')
            if not acc_no:
                return render_template('bookmanager.html', error="ACC No is required for issuing a book",
                                       success_message="ACC No is required for issuing a book")
            return issue_book(user_id, acc_no)
        elif action == 'return':
            acc_no = request.form.get('acc_no')
            if not acc_no:
                return render_template('bookmanager.html', error="ACC No is required for returning a book",
                                       success_message="ACC No is required for returning a book")
            return return_book(user_id, acc_no)
        elif action == 'renew':
            acc_no = request.form.get('acc_no')
            if not acc_no:
                return render_template('bookmanager.html', error="ACC No is required for returning a book",
                                       success_message="ACC No is required for returning a book")
            return renew_book(user_id, acc_no)

        else:
            return render_template('bookmanager.html', error="Invalid action", success_message="Invalid action")
    except Exception as e:
        return render_template("bookmanager.html",
                               success_message="An error occurred while trying to handle your request ")


def submit_data(user_id, acc_no):
    try:
        db = client['Book']
        book_data_collection = db['BookData']
        student_data_collection = db['Members']
        issue_log_collection = db['IssueLog']
        due_log_collection = db['due_log']
        
        try:

            
            data = list(student_data_collection.find({"REGISTERNO":user_id}))
            
            
            bookData = list(book_data_collection.find({"ACC": acc_no}))
            issued_details = list(issue_log_collection.find({'REGISTERNO': user_id}))
            due_details = list(due_log_collection.find({'REGISTERNO': user_id}))
            for due in due_details:
                issued_details.append(due)  # appending due details to issued details for displaying purposes
        except ValueError:
            return render_template('bookmanager.html', error="User ID must be an integer",
                                   success_message="User ID must be an integer")

        # Calculate fine
        current_date = datetime.now()
        total_fine = 0
        for due in due_details:
            
            due_date = datetime.strptime(due['DUEDATE'], '%d-%m-%Y')
            if current_date > due_date:
                days_overdue = (current_date - due_date).days
                total_fine += days_overdue * 2
                
            
        
        if data and bookData:
            user_data = data[0]
            name = user_data['NAME']
            desig = user_data['DESIGNATION']
            department = user_data['DEPARTMENT']
            year_stu = user_data['YEAR']
            phone = user_data['PHONE']
            
            book_data = bookData[0]
            callno = book_data['CALLNO']
            title = book_data['TITLE']
            author = book_data['AUTHOR']
            edition = book_data['EDITION']
            year = book_data['YEAR']
            location = book_data['Location']
            

            
            return render_template('bookmanager.html', user_id=user_id, name=name, desig=desig, department=department,
                                   year_stu=year_stu, acc_no=acc_no, callno=callno, title=title, author=author,
                                   year=year,edition=edition,
                                   location=location, phone=phone, issued_details=issued_details,
                                    fineamount=total_fine)
        elif not data:
            return render_template('bookmanager.html', error="User not found", success_message="User not found")
        else:
            
            return render_template('bookmanager.html', error="Book not found", success_message="Book not found")
    except Exception as e:

        return render_template("bookmanager.html", success_message=f"An error occurred while trying to retrieve data ")


def issue_book(user_id, acc_no):
    
    try:
        db = client['Book']
        issue_log_collection = db['IssueLog']
        book_data_collection = db['BookData']
        student_data_collection = db['Members']
        due_log_collection = db['due_log']
        due_details = list(due_log_collection.find({'REGISTERNO': user_id}))
        due_book_count = len(due_details)

        try:
            data = list(student_data_collection.find({"REGISTERNO": user_id}))
            bookData = list(book_data_collection.find({"ACC": acc_no}))
        except ValueError:
            return render_template('bookmanager.html', error="User ID and ACC No must be integers",
                                   success_message="User ID and ACC No must be integers")
        current_date = datetime.now()
        total_fine = 0
        for due in due_details:
            
            due_date = datetime.strptime(due['DUEDATE'], '%d-%m-%Y')
            if current_date > due_date:
                days_overdue = (current_date - due_date).days
                total_fine += days_overdue * 2
            issued_details = list(issue_log_collection.find({'REGISTERNO': user_id}))
            issued_details.append(due)  # appending due details to issued details for displaying purposes
       
        if data and bookData:
            user_data = data[0]
            name = user_data['NAME']
            desig = user_data['DESIGNATION']
            department = user_data['DEPARTMENT']
            year_stu = user_data['YEAR']
            phone = user_data['PHONE']
            book_data = bookData[0]
            callno = book_data['CALLNO']
            title = book_data['TITLE']
            author = book_data['AUTHOR']
            year = book_data['YEAR']
            location = book_data['Location']

            # Get issued details from MongoDB
            issued_details = list(issue_log_collection.find({'REGISTERNO': user_id}))
            
            issued_book_count = len(issued_details)
            if book_data.get('Status') == 'Currently Issued':
                return render_template('bookmanager.html',issued_details=issued_details, success_message="The book is currently issued")
            # Check if the user has already issued 3 books
            due_details = list(due_log_collection.find({'REGISTERNO': user_id}))
            
            for due in due_details:
                
                issued_details.append(due)  # adding due log datas
            if issued_book_count + due_book_count < 3:

                # Log user details in MongoDB

                issue_date = datetime.now().strftime('%d-%m-%Y')
                if desig=='Staff':
                    due_date = (datetime.now() + timedelta(months=6)).strftime('%d-%m-%Y')
                else:
                    due_date = (datetime.now() + timedelta(days=14)).strftime('%d-%m-%Y')
                renewal_count = 0

                issue_data = {
                    'REGISTERNO': user_id,
                    'NAME': name,
                    'DESIGNATION': desig,
                    'DEPARTMENT': department,
                    'YEAR': year_stu,
                    'ACC': acc_no,
                    'TITLE': title,
                    'ISSUEDATE': issue_date,
                    'DUEDATE': due_date,
                    'RENEWALCOUNT': renewal_count
                }
                issue_log_collection.insert_one(issue_data)

                # Update the book status in the MongoDB
                book_data_collection.update_one({'ACC': acc_no}, {'$set': {'Status': 'Currently Issued'}})
                # Update issued details after logging the new book
                issued_details.append(issue_data)
                
                return render_template('bookmanager.html', user_id=user_id, name=name, desig=desig,
                                       department=department,
                                       year_stu=year_stu,callno=callno,
                                       issued_details=issued_details, acc_no=acc_no, title=title, issue_date=issue_date,
                                       due_date=due_date, author=author,
                                       year=year, location=location,phone=phone,fineamount=total_fine, success_message="Issued successfully")
            else:
                
                return render_template('bookmanager.html', 
                                       issued_details=issued_details, success_message="User already has three books")


        else:
            return render_template('bookmanager.html', error="User or Book not found",
                                   success_message="User or Book not found")
    except Exception as e:
        
        return render_template("bookmanager.html", success_message=f"An error occurred while trying to add data ")


@app.route('/quick_return', methods=['POST'])
@login_required
def quick_return_route():
    try:
        db = client['Book']
        issue_log_collection = db['IssueLog']
        book_data_collection = db['BookData']
        return_log_collection = db['ReturnLog']
        due_log_collection = db['due_log']
        collected_collection= db['CollectedCollection']

        acc_no = request.form.get('acc_no')

        if not acc_no:
            return render_template('bookmanager.html', error="Missing acc_no parameter.",
                                   success_message="Missing acc_no parameter.")

        try:
            acc_no = acc_no
        except ValueError:
            return render_template('bookmanager.html', error="Invalid acc_no parameter.",
                                   success_message="Invalid acc_no parameter.")

        try:
            # Check if the book is in the IssueLog collection
            issue_data = issue_log_collection.find_one({'ACC': acc_no})

            if issue_data :
                # Calculate the fine amount
                returned_date = datetime.now()

                # Insert into the return log collection
                return_data = {
                    'REGISTERNO': issue_data['REGISTERNO'],
                    'NAME': issue_data['NAME'],
                    'DESIGNATION': issue_data['DESIGNATION'],
                    'DEPARTMENT': issue_data['DEPARTMENT'],
                    'YEAR': issue_data['YEAR'],
                    'ACC': issue_data['ACC'],
                    'TITLE': issue_data['TITLE'],
                    'ISSUEDATE': issue_data['ISSUEDATE'],
                    'RETURNEDDATE': returned_date.strftime('%d-%m-%Y')
                }
               
                return_log_collection.insert_one(return_data)

                # Delete the issue log
                issue_log_collection.delete_one({'ACC': acc_no})
                # Update the book status in the MongoDB
                book_data_collection.update_one({'ACC': acc_no}, {'$set': {'Status': 'Available'}})

            else:
                # Process for books in the due_log collection
                due_data = due_log_collection.find_one({'ACC': acc_no})
                if due_data:
                    due_date = datetime.strptime(due_data['DUEDATE'], '%d-%m-%Y')  # Convert to datetime object

                    # Calculate the fine amount
                    returned_date = datetime.now()
                    fine_amount = (returned_date - due_date).days * 2

                    # Insert into the return log collection
                    return_data = {
                        'REGISTERNO': due_data['REGISTERNO'],
                        'NAME': due_data['NAME'],
                        'DESIGNATION': due_data['DESIGNATION'],
                        'DEPARTMENT': due_data['DEPARTMENT'],
                        'YEAR': due_data['YEAR'],
                        'ACC': due_data['ACC'],
                        'TITLE': due_data['TITLE'],
                        'ISSUEDATE': due_data['ISSUEDATE'],
                        'RETURNEDDATE': returned_date.strftime('%d-%m-%Y')
                    }

                    return_log_collection.insert_one(return_data)

                    # Insert into the collected collection
                    collected_data = {
                        'REGISTERNO': due_data['REGISTERNO'],
                        'ACC': due_data['ACC'],
                        'TITLE': due_data['TITLE'],
                        'DUEDATE': due_date.strftime('%d-%m-%Y'),
                        'RETURNEDDATE': returned_date.strftime('%d-%m-%Y'),
                        'FINECOLLECTED': fine_amount
                    }
                    collected_collection.insert_one(collected_data)

                    # Delete the due log
                    due_log_collection.delete_one({'ACC': acc_no})
                    # Update the book status in the MongoDB
                    book_data_collection.update_one({'ACC': acc_no}, {'$set': {'Status': 'Available'}})

                else:
                    return render_template('bookmanager.html',
                                           error="No such issued or overdue book found for the user.",
                                           success_message="No such issued or overdue book found for the user.")
            return render_template('bookmanager.html', success_message="Book returned successfully")

        except Exception as e:
            return render_template('bookmanager.html', error=f"An error occurred: {e}",
                                   success_message=f"An error occurred")
    except Exception as e:
        return render_template("bookmanager.html", success_message="An error occurred while trying to search data ")


def return_book(user_id, acc_no):
    try:
        db = client['Book']
        issue_log_collection = db['IssueLog']
        book_data_collection = db['BookData']
        student_data_collection = db['Members']
        return_log_collection = db['ReturnLog']
        collected_collection = db['CollectedCollection']
        due_log_collection = db['due_log']

        try:
            

            # Check if the book is in the IssueLog collection
            issue_data = issue_log_collection.find_one({'REGISTERNO': user_id, 'ACC': acc_no})

            if issue_data:
                
                # Process for books in the IssueLog collection
                due_data = due_log_collection.find_one({'REGISTERNO': user_id, 'ACC': acc_no})
                due_date = due_data['DUEDATE'] if due_data else issue_data['ISSUEDATE']

                # Calculate the fine amount
                returned_date = datetime.now()

                # Insert into the return log collection
                return_data = {
                    'REGISTERNO': issue_data['REGISTERNO'],
                    'NAME': issue_data['NAME'],
                    'DESIGNATION': issue_data['DESIGNATION'],
                    'DEPARTMENT': issue_data['DEPARTMENT'],
                    'YEAR': issue_data['YEAR'],
                    'ACC': issue_data['ACC'],
                    'TITLE': issue_data['TITLE'],
                    'ISSUEDATE': issue_data['ISSUEDATE'],
                    'RETURNEDDATE': returned_date.strftime('%d-%m-%Y')
                }
               
                return_log_collection.insert_one(return_data)

                # Delete the issue log
                issue_log_collection.delete_one({'REGISTERNO': user_id, 'ACC': acc_no})
               

            else:
                # Process for books in the due_log collection
                due_data = due_log_collection.find_one({'REGISTERNO': user_id, 'ACC': acc_no})

                if not due_data:
                    return render_template('bookmanager.html',
                                           error="No such issued or overdue book found for the user",
                                           success_message="No such issued or overdue book found for the user")

                due_date = datetime.strptime(due_data['DUEDATE'], '%d-%m-%Y')  # Convert to datetime object

                # Calculate the fine amount
                returned_date = datetime.now()
                fine_amount = (returned_date - due_date).days * 2

                # Insert into the return log collection
                return_data = {
                    'REGISTERNO': due_data['REGISTERNO'],
                    'NAME': due_data.get('NAME', ''),
                    'DESIGNATION': due_data.get('DESIGNATION', ''),
                    'DEPARTMENT': due_data.get('DEPARTMENT', ''),
                    'YEAR': due_data.get('YEAR', ''),
                    'ACC': due_data['ACC'],
                    'TITLE': due_data['TITLE'],
                    'ISSUEDATE': due_data['ISSUEDATE'],
                    'RETURNEDDATE': returned_date.strftime('%d-%m-%Y')
                }
               
                return_log_collection.insert_one(return_data)

                # Insert into the collected collection
                collected_data = {
                    'REGISTERNO': due_data['REGISTERNO'],
                    'ACC': due_data['ACC'],
                    'TITLE': due_data['TITLE'],
                    'DUEDATE': due_date.strftime('%d-%m-%Y'),
                    'RETURNEDDATE': returned_date.strftime('%d-%m-%Y'),
                    'FINECOLLECTED': fine_amount
                }
               
                collected_collection.insert_one(collected_data)

                # Delete the due log
                due_log_collection.delete_one({'REGISTERNO': user_id, 'ACC': acc_no})
               

            # Update the book status in the MongoDB
            book_data_collection.update_one({'ACC': acc_no}, {'$set': {'Status': 'Available'}})
            

            issued_details = list(issue_log_collection.find({'REGISTERNO': user_id}))

            return render_template('bookmanager.html', success_message="Book returned successfully",
                                   issued_details=issued_details)
        except Exception as e:
            
            return render_template('bookmanager.html', error=f"An error occurred: {e}",
                                   success_message="An error occurred")
    except Exception as e:
        return render_template("searchmember.html", success_message="An error occurred while trying to search data ")


def renew_book(user_id, acc_no):
    try:
        db = client['Book']
        issue_log_collection = db['IssueLog']

        

        # Find the issued book data
        query = {'REGISTERNO': user_id, 'ACC': acc_no}
        
        issue_data = issue_log_collection.find_one(query)
        

        if not issue_data:
            return render_template('bookmanager.html', error="No such issued book found for the user",
                                   success_message="No such issued book found for the user")

        # Check if the book has been renewed more than 2 times
        if issue_data['RENEWALCOUNT'] > 1:
            return render_template('bookmanager.html', error="This book has already been renewed 2 times.",
                                   success_message="This book has already been renewed 2 times.")

        # Update the due date and renewal count in the issue log collection
        due_date = datetime.now() + timedelta(days=14)
        
        issue_log_collection.update_one({'_id': issue_data['_id']}, {
            '$set': {'DUEDATE': due_date.strftime('%d-%m-%Y'), 'RENEWALCOUNT': issue_data['RENEWALCOUNT'] + 1}})

        # Update the issued details after renewing the book
        issued_details = list(issue_log_collection.find({'REGISTERNO': user_id}))
        

        issued_details[-1]['DUEDATE'] = due_date.strftime('%d-%m-%Y')

        return render_template('bookmanager.html', issued_details=issued_details,
                               success_message="Book renewed successfully")

    except Exception as e:
        
        return render_template('bookmanager.html', error=f"An error occurred: {e}",
                               success_message=f"An error occurred: {e}")


@app.route('/subbookmanager')
@login_required
def bookmanagersub():
    try:
        return render_template('bookmanagersub.html')
    except Exception as e:
        return render_template("dashboardsub.html",
                               success_message="An error occurred while rendering the search member page", dues_data=dues_data, members_count=members_count)


# Backend for handling which button is pressed in sub book manager
@app.route('/subsubmit', methods=['POST'])
@login_required
def handle_submit_sub():
    try:
        user_id = request.form.get('user_id').upper()
        acc_no = request.form.get('acc_no')
        action = request.form.get('action')

        if not user_id:
            return render_template('bookmanagersub.html', error="User ID is required",
                                   success_message="User ID is required")

        if action == 'submit':
            return submit_data_sub(user_id, acc_no)
        elif action == 'issue':
            acc_no = request.form.get('acc_no')
            if not acc_no:
                return render_template('bookmanagersub.html', error="ACC No is required for issuing a book",
                                       success_message="ACC No is required for issuing a book")
            return issue_book_sub(user_id, acc_no)

        elif action == 'return':
            acc_no = request.form.get('acc_no')
            if not acc_no:
                return render_template('bookmanagersub.html', error="ACC No is required for returning a book",
                                       success_message="ACC No is required for returning a book")
            return return_book_sub(user_id, acc_no)

        elif action == 'renew':
            acc_no = request.form.get('acc_no')
            if not acc_no:
                return render_template('bookmanagersub.html', error="ACC No is required for returning a book",
                                       success_message="ACC No is required for returning a book")
            return renew_book_sub(user_id, acc_no)

        else:
            return render_template('bookmanagersub.html', error="Invalid action", success_message="Invalid action")
    except Exception as e:
        return render_template("bookmanagersub.html",
                               success_message="An error occurred while trying to handle your request ")


# Backend for sublibrarian book manager submit button for displaying data
def submit_data_sub(user_id, acc_no):
    try:
        db = client['Book']
        book_data_collection = db['BookData']
        student_data_collection = db['Members']
        issue_log_collection = db['IssueLog']
        due_log_collection = db['due_log']
        
        try:

            
            data = list(student_data_collection.find({"REGISTERNO": user_id}))
            bookData = list(book_data_collection.find({"ACC": acc_no}))
            
            issued_details = list(issue_log_collection.find({'REGISTERNO': user_id}))
            due_details = list(due_log_collection.find({'REGISTERNO': user_id}))
            for due in due_details:
                issued_details.append(due)  # appending due details to issued details for displaying purposes
        except ValueError:
            return render_template('bookmanagersub.html', error="User ID must be an integer",
                                   success_message="User ID must be an integer")

        # Calculate fine
        current_date = datetime.now()
        total_fine = 0
        for due in due_details:
            
            due_date = datetime.strptime(due['DUEDATE'], '%d-%m-%Y')
            if current_date > due_date:
                days_overdue = (current_date - due_date).days
                total_fine += days_overdue * 2
                
              

        if data and bookData:
            user_data = data[0]
            name = user_data['NAME']
            desig = user_data['DESIGNATION']
            department = user_data['DEPARTMENT']
            year_stu = user_data['YEAR']
            phone = user_data['PHONE']
            book_data = bookData[0]
            callno = book_data['CALLNO']
            title = book_data['TITLE']
            author = book_data['AUTHOR']
            edition = book_data['EDITION']
            year = book_data['YEAR']
            location = book_data['Location']
            # fine = collected_data['FINECOLLECTED']

            

            return render_template('bookmanagersub.html', user_id=user_id, name=name, desig=desig, department=department,
                                   year_stu=year_stu, acc_no=acc_no, callno=callno, title=title, author=author,
                                   year=year,edition=edition,
                                   location=location, phone=phone, issued_details=issued_details,
                                    fineamount=total_fine)
        elif not data:
            return render_template('bookmanagersub.html', error="User not found", success_message="User not found")
        else:
            
            return render_template('bookmanagersub.html', error="Book not found", success_message="Book not found")
    except Exception as e:
        return render_template("bookmanagersub.html", success_message="An error occurred while trying to retrieve data ")


def issue_book_sub(user_id, acc_no):
    try:

        db = client['Book']
        issue_log_collection = db['IssueLog']
        book_data_collection = db['BookData']
        student_data_collection = db['Members']
        due_log_collection = db['due_log']
        due_details = list(due_log_collection.find({'REGISTERNO': user_id}))
        due_book_count = len(due_details)

        try:
            data = list(student_data_collection.find({"REGISTERNO": user_id}))
            bookData = list(book_data_collection.find({"ACC": acc_no}))
        except ValueError:
            return render_template('bookmanagersub.html', error="User ID and ACC No must be integers",
                                   success_message="User ID and ACC No must be integers")
        current_date = datetime.now()
        total_fine = 0
        for due in due_details:
            
            due_date = datetime.strptime(due['DUEDATE'], '%d-%m-%Y')
            if current_date > due_date:
                days_overdue = (current_date - due_date).days
                total_fine += days_overdue * 2
            issued_details = list(issue_log_collection.find({'REGISTERNO': user_id}))
            issued_details.append(due)  # appending due details to issued details for displaying purposes
        if data and bookData:
            user_data = data[0]
            name = user_data['NAME']
            desig = user_data['DESIGNATION']
            department = user_data['DEPARTMENT']
            year_stu = user_data['YEAR']
            phone = user_data['PHONE']
            book_data = bookData[0]
            callno = book_data['CALLNO']
            title = book_data['TITLE']
            author = book_data['AUTHOR']
            year = book_data['YEAR']
            location = book_data['Location']

            # Get issued details from MongoDB
            issued_details = list(issue_log_collection.find({'REGISTERNO': user_id}))
           
            issued_book_count = len(issued_details)
            if book_data.get('Status') == 'Currently Issued':
                return render_template('bookmanagersub.html',issued_details=issued_details, success_message="The book is currently issued")
            # Check if the user has already issued 3 books
            due_details = list(due_log_collection.find({'REGISTERNO': user_id}))
            
            for due in due_details:
                
                issued_details.append(due)  # adding due log datas
            if issued_book_count + due_book_count < 3:

                # Log user details in MongoDB

                issue_date = datetime.now().strftime('%d-%m-%Y')
                due_date = (datetime.now() + timedelta(days=14)).strftime('%d-%m-%Y')
                renewal_count = 0

                issue_data = {
                    'REGISTERNO': user_id,
                    'NAME': name,
                    'DESIGNATION': desig,
                    'DEPARTMENT': department,
                    'YEAR': year_stu,
                    'ACC': acc_no,
                    'TITLE': title,
                    'ISSUEDATE': issue_date,
                    'DUEDATE': due_date,
                    'RENEWALCOUNT': renewal_count
                }
                issue_log_collection.insert_one(issue_data)

                # Update the book status in the MongoDB
                book_data_collection.update_one({'ACC': acc_no}, {'$set': {'Status': 'Currently Issued'}})
                # Update issued details after logging the new book
                issued_details.append(issue_data)
                
                return render_template('bookmanagersub.html', user_id=user_id, name=name, desig=desig,
                                       department=department,
                                       year_stu=year_stu,
                                       issued_details=issued_details,callno=callno, acc_no=acc_no, title=title, issue_date=issue_date,
                                       due_date=due_date, author=author,phone=phone,
                                       year=year, location=location, fineamount=total_fine, success_message="Issued successfully")
            else:
               
                return render_template('bookmanagersub.html', error="User already has three books",
                                       issued_details=issued_details, success_message="User already has three books")


        else:
            return render_template('bookmanagersub.html', error="User or Book not found",
                                   success_message="User or Book not found")
    except Exception as e:
        return render_template("bookmanagersub.html", success_message=f"An error occurred while trying to add data ")



# Need to implement try and except
@app.route('/subquick_return', methods=['POST'])
@login_required
def quick_return_route_sub():
    try:
        db = client['Book']
        issue_log_collection = db['IssueLog']
        book_data_collection = db['BookData']
        return_log_collection = db['ReturnLog']
        due_log_collection = db['due_log']
        collected_collection = db['CollectedCollection']

        acc_no = request.form.get('acc_no')

        if not acc_no:
            return render_template('bookmanager.html', error="Missing acc_no parameter.",
                                   success_message="Missing acc_no parameter.")

        try:
            acc_no = acc_no
        except ValueError:
            return render_template('bookmanager.html', error="Invalid acc_no parameter.",
                                   success_message="Invalid acc_no parameter.")

        try:
            # Check if the book is in the IssueLog collection
            issue_data = issue_log_collection.find_one({'ACC': acc_no})

            if issue_data:

                # Calculate the fine amount
                returned_date = datetime.now()

                # Insert into the return log collection
                return_data = {
                    'REGISTERNO': issue_data['REGISTERNO'],
                    'NAME': issue_data['NAME'],
                    'DESIGNATION': issue_data['DESIGNATION'],
                    'DEPARTMENT': issue_data['DEPARTMENT'],
                    'YEAR': issue_data['YEAR'],
                    'ACC': issue_data['ACC'],
                    'TITLE': issue_data['TITLE'],
                    'ISSUEDATE': issue_data['ISSUEDATE'],
                    'RETURNEDDATE': returned_date.strftime('%d-%m-%Y')
                }

                return_log_collection.insert_one(return_data)

                # Delete the issue log
                issue_log_collection.delete_one({'ACC': acc_no})
                # Update the book status in the MongoDB
                book_data_collection.update_one({'ACC': acc_no}, {'$set': {'Status': 'Available'}})

            else:
                # Process for books in the due_log collection
                due_data = due_log_collection.find_one({'ACC': acc_no})
                if due_data:
                    due_date = datetime.strptime(due_data['DUEDATE'], '%d-%m-%Y')  # Convert to datetime object

                    # Calculate the fine amount
                    returned_date = datetime.now()
                    fine_amount = (returned_date - due_date).days * 2

                    # Insert into the return log collection
                    return_data = {
                        'REGISTERNO': due_data['REGISTERNO'],
                        'NAME': due_data['NAME'],
                        'DESIGNATION': due_data['DESIGNATION'],
                        'DEPARTMENT': due_data['DEPARTMENT'],
                        'YEAR': due_data['YEAR'],
                        'ACC': due_data['ACC'],
                        'TITLE': due_data['TITLE'],
                        'ISSUEDATE': due_data['ISSUEDATE'],
                        'RETURNEDDATE': returned_date.strftime('%d-%m-%Y')
                    }

                    return_log_collection.insert_one(return_data)

                    # Insert into the collected collection
                    collected_data = {
                        'REGISTERNO': due_data['REGISTERNO'],
                        'ACC': due_data['ACC'],
                        'TITLE': due_data['TITLE'],
                        'DUEDATE': due_date.strftime('%d-%m-%Y'),
                        'RETURNEDDATE': returned_date.strftime('%d-%m-%Y'),
                        'FINECOLLECTED': fine_amount
                    }
                    collected_collection.insert_one(collected_data)

                    # Delete the due log
                    due_log_collection.delete_one({'ACC': acc_no})
                    # Update the book status in the MongoDB
                    book_data_collection.update_one({'ACC': acc_no}, {'$set': {'Status': 'Available'}})

                else:
                    return render_template('bookmanager.html',
                                           error="No such issued or overdue book found for the user.",
                                           success_message="No such issued or overdue book found for the user.")
            return render_template('bookmanager.html', success_message="Book returned successfully")

        except Exception as e:
            return render_template('bookmanager.html', error=f"An error occurred: {e}",
                                   success_message=f"An error occurred")
    except Exception as e:
        return render_template("bookmanager.html", success_message="An error occurred while trying to search data ")


def return_book_sub(user_id, acc_no):
    try:
        db = client['Book']
        issue_log_collection = db['IssueLog']
        book_data_collection = db['BookData']
        student_data_collection = db['Members']
        return_log_collection = db['ReturnLog']
        collected_collection = db['CollectedCollection']
        due_log_collection = db['due_log']

        try:
            

            # Check if the book is in the IssueLog collection
            issue_data = issue_log_collection.find_one({'REGISTERNO': user_id, 'ACC': acc_no})

            if issue_data:
                
                # Process for books in the IssueLog collection
                due_data = due_log_collection.find_one({'REGISTERNO': user_id, 'ACC': acc_no})
                due_date = due_data['DUEDATE'] if due_data else issue_data['ISSUEDATE']

                # Calculate the fine amount
                returned_date = datetime.now()

                # Insert into the return log collection
                return_data = {
                    'REGISTERNO': issue_data['REGISTERNO'],
                    'NAME': issue_data['NAME'],
                    'DESIGNATION': issue_data['DESIGNATION'],
                    'DEPARTMENT': issue_data['DEPARTMENT'],
                    'YEAR': issue_data['YEAR'],
                    'ACC': issue_data['ACC'],
                    'TITLE': issue_data['TITLE'],
                    'ISSUEDATE': issue_data['ISSUEDATE'],
                    'RETURNEDDATE': returned_date.strftime('%d-%m-%Y')
                }
                
                return_log_collection.insert_one(return_data)

                # Delete the issue log
                issue_log_collection.delete_one({'REGISTERNO': user_id, 'ACC': acc_no})
                

            else:
                # Process for books in the due_log collection
                due_data = due_log_collection.find_one({'REGISTERNO': user_id, 'ACC': acc_no})

                if not due_data:
                    return render_template('bookmanagersub.html',
                                           error="No such issued or overdue book found for the user",
                                           success_message="No such issued or overdue book found for the user")

                due_date = datetime.strptime(due_data['DUEDATE'], '%d-%m-%Y')  # Convert to datetime object

                # Calculate the fine amount
                returned_date = datetime.now()
                fine_amount = (returned_date - due_date).days * 2

                # Insert into the return log collection
                return_data = {
                    'REGISTERNO': due_data['REGISTERNO'],
                    'NAME': due_data.get('NAME', ''),
                    'DESIG': due_data.get('DESIG', ''),
                    'DEPARTMENT': due_data.get('DEPARTMENT', ''),
                    'YEAR': due_data.get('YEAR', ''),
                    'ACC': due_data['ACC'],
                    'TITLE': due_data['TITLE'],
                    'ISSUEDATE': due_data['ISSUEDATE'],
                    'RETURNEDDATE': returned_date.strftime('%d-%m-%Y')
                }
                
                return_log_collection.insert_one(return_data)

                # Insert into the collected collection
                collected_data = {
                    'REGISTERNO': due_data['REGISTERNO'],
                    'ACC': due_data['ACC'],
                    'TITLE': due_data['TITLE'],
                    'DUEDATE': due_date.strftime('%d-%m-%Y'),
                    'RETURNEDDATE': returned_date.strftime('%d-%m-%Y'),
                    'FINECOLLECTED': fine_amount
                }
                
                collected_collection.insert_one(collected_data)

                # Delete the due log
                due_log_collection.delete_one({'REGISTERNO': user_id, 'ACC': acc_no})
                

            # Update the book status in the MongoDB
            book_data_collection.update_one({'ACC': acc_no}, {'$set': {'Status': 'Available'}})
            

            issued_details = list(issue_log_collection.find({'REGISTERNO': user_id}))

            return render_template('bookmanagersub.html', success_message="Book returned successfully",
                                   issued_details=issued_details)
        except Exception as e:
            
            return render_template('bookmanagersub.html', error=f"An error occurred: {e}",
                                   success_message="An error occurred")
    except Exception as e:
        return render_template("searchmember.html", success_message="An error occurred while trying to search data ")


def renew_book_sub(user_id, acc_no):
    try:
        db = client['Book']
        issue_log_collection = db['IssueLog']

        

        # Find the issued book data
        query = {'REGISTERNO': user_id, 'ACC': acc_no}
        
        issue_data = issue_log_collection.find_one(query)
        

        if not issue_data:
            return render_template('bookmanagersub.html', error="No such issued book found for the user",
                                   success_message="No such issued book found for the user")

        # Check if the book has been renewed more than 2 times
        if issue_data['RENEWALCOUNT'] > 1:
            return render_template('bookmanagersub.html', error="This book has already been renewed 2 times.",
                                   success_message="This book has already been renewed 2 times.")

        # Update the due date and renewal count in the issue log collection
        due_date = datetime.now() + timedelta(days=14)
        
        issue_log_collection.update_one({'_id': issue_data['_id']}, {
            '$set': {'DUEDATE': due_date.strftime('%d-%m-%Y'), 'RENEWALCOUNT': issue_data['RENEWALCOUNT'] + 1}})

        # Update the issued details after renewing the book
        issued_details = list(issue_log_collection.find({'REGISTERNO': user_id}))
        

        issued_details[-1]['DUEDATE'] = due_date.strftime('%d-%m-%Y')

        return render_template('bookmanagersub.html', issued_details=issued_details,
                               success_message="Book renewed successfully")

    except Exception as e:
        
        return render_template('bookmanagersub.html', error=f"An error occurred: {e}",
                               success_message=f"An error occurred: {e}")


# --------------------------------------------------REMOVE PAGE--------------------------------------------------------------------

@app.route('/rbook')
@login_required
def rbook():
    try:
        return render_template('inventory_book_remove.html')
    except Exception as e:
        return render_template("searchmember.html", success_message="An error occurred while rendering the remove page")


@app.route('/search_remove', methods=['POST'])
@login_required
def search_remove():
    try:
        db = client['Book']
        global access_number
        collection = db['BookData']
        access_number = request.form.get('acc_no')
        btn = request.form.get('submit')
        if btn == 'submit':
            found = collection.find_one({'ACC': access_number}, {'_id': 0})
            if found:
                return render_template('inventory_book_remove.html', found=found, acc_no=access_number)

            else:
                return render_template('inventory_book_remove.html', success_message="Book not found")

        elif btn == 'Remove':
            remove()
            return render_template('inventory_book_remove.html', success_message="Removed Successfully")

        elif btn=='Update':
            access_number = request.form.get('acc_no')
            title = request.form.get('title')
            author = request.form.get('author')
            year = request.form.get('year')
            pageno = request.form.get('page_no')
            isbn = request.form.get('isbn')
            callno = request.form.get('call_no')
            edition = request.form.get('edition')
            publisher = request.form.get('publisher')
            price = request.form.get('price')
            location = request.form.get('location')

            book = {
                'ACC':  access_number,
                'CALLNO': float(callno),
                'TITLE': title,
                'AUTHOR': author,
                'EDITION': edition,
                'YEAR': year,
                'PAGE NO': pageno,
                'PRICE': price,
                'ISBN ': isbn,
                'PUBLISHER':publisher,
                'Location': location,
                'Status': 'Available',
                'DOCTYPE': 'Book'
            }

            remove()
            collection = db['BookData']
            collection.insert_one(book)

            return render_template('inventory_book_remove.html',success_message='Updated Succesfully')

    except Exception as e:

        return render_template("inventory_book_remove.html",
                               success_message="An error occurred while trying to handle your request ")


def remove():
    try:
        global access_number
        collection = db['BookData']
        access_number = request.form.get('acc_no')
        collection.delete_one({'ACC': access_number})
    except Exception as e:
        return render_template("inventory.html", success_message="An error occurred while trying to remove data ", totalbooks=tb)




# ----------------------------------------------ADD ITEMS------------------------------------------------------------------------------------------------


@app.route('/athesis')
@login_required
def athesis():
    try:
        return render_template('inventory_thesis_add.html')
    except Exception as e:
        return render_template("inventory.html",
                               success_message="An error occurred while rendering the add thesis page", totalbooks=tb)

@app.route('/addthesis', methods=['POST'])
@login_required
def log_thesis():
    try:
        acc_no = request.form.get('acc_no').strip()
        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        department = request.form.get('department').strip()
        year = request.form.get('year_of_submission').strip()
        page_no = request.form.get('page_no').strip()

        book_ava = 'available'

        collection = db['BookData']
        collection1= db['Thesis']

        thesis = {
            'ACC': acc_no,
            'TITLE': title,
            'YEAR': year,
            'Status': book_ava,
            'DOCTYPE': 'Thesis'
        }
        thesisdb = {
            'ACC': acc_no,
            'TITLE': title,
            'DEPARTMENT': department,
            'AUTHOR': author,
            'YEAR': year,
            'PAGENO': page_no,
        }

        collection.insert_one(thesis)
        collection1.insert_one(thesisdb)
        success_message = 'thesis added Successfully!'
        return render_template('inventory_thesis_add.html', success_message=success_message)
    except Exception as e:
        return render_template('inventory_thesis_add.html', success_message=e)


@app.route('/ajournals')
@login_required
def ajournals():
    try:
        return render_template('inventory_journals_add.html')
    except Exception as e:
        return render_template("inventory.html",
                               success_message="An error occurred while rendering the add journals page", totalbooks=tb)

@app.route('/addjournal', methods=['POST'])
@login_required
def log_journal():
    try:
        acc_no = request.form.get('acc_no').strip()
        title = request.form.get('title').strip()
        publisher = request.form.get('publisher').strip()
        year = request.form.get('year').strip()
        issue_no = request.form.get('issue_no').strip()
        volume = request.form.get('volume_no').strip()

        book_ava = 'available'

        collection = db['BookData']
        
        collection1 = db['Journals']

        journal = {
            'ACC': acc_no,
            'TITLE': title,
            'YEAR': year,
            'Status': book_ava,
            'DOCTYPE': 'Journal'
        }


        journaldb = {
            'ACC': acc_no,
            'TITLE': title,
            'PUBLISHER':publisher,
            'ISSUENO':issue_no,
            'YEAR': year,
            'VOLUME':volume,
        }

        collection.insert_one(journal)
        collection1.insert_one(journaldb)
        success_message = 'Journal added Successfully!'
        return render_template('inventory_journals_add.html', success_message=success_message)
    except Exception as e:
        return render_template('inventory_journals_add.html', success_message=e)

@app.route('/acds')
@login_required
def acds():
    try:
        return render_template('inventory_cds_add.html')
    except Exception as e:
        return render_template("inventory.html", success_message="An error occurred while rendering the add CD's page", totalbooks=tb)

@app.route('/addcd', methods=['POST'])
@login_required
def log_cds():
    try:
        acc_no = request.form.get('acc_no').strip()
        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        year = request.form.get('year').strip()
        book_ava = 'available'

        collection = db['BookData']
        collection1 = db['CDs']
        cds = {
            'ACC': acc_no,
            'TITLE': title,
            'AUTHOR': author,
            'YEAR': year,
            'Status': book_ava,
            'DOCTYPE':'CD'
        }


        cdsdb = {
            'ACC': acc_no,
            'TITLE': title,
            'AUTHOR': author,
            'YEAR': year,
        }

        collection.insert_one(cds)
        collection1.insert_one(cdsdb)
        success_message = 'CD added Successfully!'
        return render_template('inventory_cds_add.html', success_message=success_message)
    except Exception as e:
        return render_template("inventory_cds_add.html", success_message="An error occurred while adding the data")

@app.route('/aeresource')
@login_required
def aeresources():
    try:
        return render_template('inventory_eresource_add.html')
    except Exception as e:
        return render_template("inventory.html",
                               success_message="An error occurred while rendering the add E-Resources page", totalbooks=tb)

@app.route('/adderesource', methods=['POST'])
def log_eresource():
    try:
        acc_no = request.form.get('acc_no').strip()
        link = request.form.get('link').strip()
        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        book_ava = 'available'
        collection = db['BookData']
        collection1 = db['E_Resources']
    
        eresource = {
            'ACC': acc_no,
            'TITLE': title,
            'AUTHOR': author,
            'Status': book_ava,
            'DOCTYPE':'EResource'
        }
        eresourcedb = {
            'ACC': acc_no,
            'TITLE': title,
            'REPOSITORYLINK':link,
            'AUTHOR': author,
        }
    
        collection.insert_one(eresource)
        collection1.insert_one(eresourcedb)
        success_message = 'E-Resource added Successfully!'
        return render_template('inventory_eresource_add.html', success_message=success_message)
    except Exception as e:
        return render_template('inventory_eresource_add.html', success_message=e)

@app.route('/aprojects')
@login_required
def aprojects():
    try:
        return render_template('inventory_projects_add.html')
    except Exception as e:
        return render_template("inventory.html",
                               success_message="An error occurred while rendering the add projects page", totalbooks=tb)

@app.route('/addproject', methods=['POST'])
@login_required
def log_project():
    try:
        acc_no = request.form.get('acc_no').strip()
        title = request.form.get('title').strip()
        author= request.form.get('author').strip()
        department = request.form.get('dept').strip()
        year = request.form.get('year').strip()
        member = request.form.get('rollno').strip()

        book_ava = 'available'

        collection = db['BookData']
        collection1 = db['Projects']

        project = {
            'ACC': acc_no,
            'AUTHOR': author,
            'TITLE': title,
            'YEAR': year,
            'Status': book_ava,
            'DOCTYPE': 'Project'
        }
        projectdb = {
            'ACC': acc_no,
            'AUTHOR': author,
            'TITLE': title,
            'DEPARTMENT': department,
            'MEMBERS': member,
            'YEAR': year,
        }

        collection.insert_one(project)
        collection1.insert_one(projectdb)
        success_message = 'Project added Successfully!'
        return render_template('inventory_projects_add.html', success_message=success_message)
    except Exception as e:
        return render_template('inventory_projects_add.html', success_message=e)

# ----------------------------------------------MISSING ITEMS------------------------------------------------------------------------------------------------

@app.route('/mbook')
@login_required
def mbook():
    try:
        return render_template('inventory_book_missing.html')
    except Exception as e:
        return render_template("inventory.html",
                               success_message="An error occurred while rendering the missing books page", totalbooks=tb)


@app.route('/search_missing', methods=['POST'])
@login_required
def search_missing():
    try:
        global access_number
        db = client['Book']
        access_number = request.form.get('acc_no').strip()
        btn = request.form.get('submit')
        if btn == 'submit':
            collection = db['BookData']
            found = collection.find_one({'ACC': access_number}, {'_id': 0})
            if found:
                success_message = "Successfully retrieved"
                
            else:
                success_message = "Book not found"
            return render_template('inventory_book_missing.html', found=found, acc_no=access_number,
                                   success_message=success_message)

        elif btn == 'missing':
            success_message=mark_unavailable()
            return render_template('inventory_book_missing.html', success_message=success_message)
    except Exception as e:
        return render_template('inventory_book_missing.html')


def mark_unavailable():
    try:
        reason = request.form.get('reason')

        collection = db['BookData']
        found = collection.find_one({'ACC': access_number}, {'_id': 0})
        if reason=='available':
            collection.update_one({'ACC': access_number}, {'$set': {'Status': 'Available'}})
            collection1 = db['Missinglog']
            found1=collection1.find_one({'ACC': access_number}, {'_id': 0})
            collection1.delete_one(found1)
            return 'Marked as Available'

        else:
            collection.update_one({'ACC': access_number}, {'$set': {'Status': 'unavailable'}})
            collection1 = db['Missinglog']
            found['Reason'] = reason
            found['Status']='Unavailable'
            collection1.insert_one(found)
            return 'Marked as Unavailable'

    except Exception as e:
        return render_template("inventory_book_missing.html",
                               success_message="An error occurred while trying to change the status of the book")





# -----------------------------------------------Book Acquisition--------------------------------------------------------------
@app.route('/bookacquisition')
@login_required
def acquisition():
    try:
        return render_template('bookacquisition.html')
    except Exception as e:
        return render_template("dashboard.html",
                               success_message="An error occurred while rendering the book acquisition page", dues_data=dues_data, members_count=members_count)


@app.route('/subbookacquisition')
@login_required
def subacquisition():
    try:
        return render_template('bookacquisitionsub.html')
    except Exception as e:
        return render_template("dashboardsub.html",
                               success_message="An error occurred while rendering the sub book acquisition page", dues_data=dues_data, members_count=members_count)


@app.route('/sublog_book_acq', methods=['POST'])
@login_required
def sublog_book_acq():
    try:
        db = client['Book']
        collection = db['BookAcquisition']

        global title
        global author
        global year
        global page_no
        global call_no
        global author_2
        global publisher
        global price

        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        year = request.form.get('year').strip()
        page_no = request.form.get('page_no').strip()
        call_no = request.form.get('call_no').strip()
        author_2 = request.form.get('author_2').strip()
        publisher = request.form.get('publisher').strip()
        price = request.form.get('price').strip()

        buybook = {
            "CALLNO": call_no,
            "TITLE": title,
            "AUTHOR": author,
            "AUTHOR2": author_2,
            "PUBLISHER": publisher,
            "YEAR": year,
            "PAGENO": page_no,
            "PRICE": price,
        }
        collection.insert_one(buybook)
        success_message = "Successfully Requested"
        return render_template('bookacquisitionsub.html', success_message=success_message)
    except Exception as e:
        return render_template('bookacquisitionsub.html',
                               success_message='An error occurred while trying to handle your request')


@app.route('/log_book_acq', methods=['POST'])
@login_required
def log_book_acq():
    try:

        db = client['Book']
        collection = db['BookAcquisition']

        global title
        global author
        global year
        global page_no
        global call_no
        global author_2
        global publisher
        global price

        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        year = request.form.get('year').strip()
        page_no = request.form.get('page_no').strip()
        call_no = request.form.get('call_no').strip()
        author_2 = request.form.get('author_2').strip()
        publisher = request.form.get('publisher').strip()
        price = request.form.get('price').strip()

        buybook = {
            "CALLNO": call_no,
            "TITLE": title,
            "AUTHOR": author,
            "AUTHOR2": author_2,
            "PUBLISHER": publisher,
            "YEAR": year,
            "PAGENO": page_no,
            "PRICE": price,
        }
        collection.insert_one(buybook)
        success_message = "Successfully Requested"
        return render_template('bookacquisition.html', success_message=success_message)
    except Exception as e:
        return render_template('bookacquisition.html',
                               success_message='An error occurred while trying to handle your request')


# ---------------------------------------------No DUE checker---------------------------------------------------------------

@app.route('/noduechecker')
@login_required
def noduechecker():
    try:
        return render_template('nodueformcheck.html')
    except Exception as e:
        return render_template('dashboard.html',
                               success_message='An error occurred while rendering the no due page')


@app.route('/subnoduechecker')
@login_required
def subnoduechecker():
    try:
        return render_template('nodueformchecksub.html')
    except Exception as e:
        return render_template('dashboardsub.html',
                               success_message='An error occurred while rendering the sub no due page')


@app.route('/subsearch_nodue', methods=['POST'])
@login_required
def subsearch_nodue():
    try:
        db = client['Book']
        global register_number, listdata
        collection1 = db['Members']
        collection2 = db['due_log']
        register_number = request.form.get('reg_no').strip()
        found = collection1.find_one({'REGISTERNO': register_number}, {'_id': 0})
        data = collection2.find({'REGISTERNO':register_number}, {'_id': 0})
        amount = 0
        for i in data:
            d = i['DUEDATE']
            
            due = datetime.strptime(d, '%d-%m-%Y').date()
            
            current = date.today()
            days = abs((due - current).days)
            fine = days * 2
            i['FINE'] = fine
            amount += fine
        if found:
            
            data = collection2.find({'REGISTERNO':register_number}, {'_id': 0})
            listdata = list(data)
            
                
            success_message = "Issue Found"

        else:
            success_message = 'Not Issued'
        return render_template('nodueformchecksub.html', found=found, reg_no=register_number, issued_details=listdata,
                               total=amount, success_message=success_message)
    except Exception as e:
        return render_template('nodueformchecksub.html',
                               success_message='An error occurred while trying to handle your request')


@app.route('/search_nodue', methods=['POST'])
@login_required
def search_nodue():
    global register_number, listdata
    try:
        db = client['Book']
        collection1 = db['Members']
        collection2 = db['due_log']
        register_number = request.form.get('reg_no').strip()
    
        found = collection1.find_one({'REGISTERNO': register_number}, {'_id': 0})
        data = list(collection2.find({'REGISTERNO': register_number}, {'_id': 0}))
    
        amount = 0
        for i in data:
            d = i['DUEDATE']
        
            due = datetime.strptime(d, '%d-%m-%Y').date()
            
            current = date.today()
            days = abs((due - current).days)
            fine = days * 2
            i['FINE'] = fine
            amount += fine
        if found:
            
            data = collection2.find({'REGISTERNO': register_number}, {'_id': 0})
            listdata = list(data)
            
                
            success_message = "Issue Found"
            return render_template('nodueformcheck.html', found=found, reg_no=register_number, issued_details=listdata,
                                   total=amount, success_message=success_message)

        else:
            success_message = 'Not Issued'
            
            return render_template('nodueformcheck.html', success_message=success_message)
    except Exception as e:
        return render_template('nodueformcheck.html',
                               success_message=e)

    # --------------------------------------------------------Fine Manager---------------------------------------------


@app.route('/finemanager', methods=['GET', 'POST'])
@login_required
def finemanager():
    try:
        global total_fines
        global total_amount
        global collected
        db = client['Book']
        collection = db['due_log']

        total_fines = collection.count_documents({})
        data = list(collection.find({}, {'_id': 0}))
        
        total_amount = 0

        for i in data:
            d = i['DUEDATE']
            due = datetime.strptime(d, '%d-%m-%Y').date()
            current = date.today()
            days = abs((due - current).days)
            fine = days * 2
            i['FINE'] = fine
            total_amount += fine

        collection1 = db['CollectedCollection']
        collected=0
        
        collect = list(collection1.aggregate([
            {"$group": {"_id": "", "FINECOLLECTED": {"$sum": "$FINECOLLECTED"}}}]))
        
        for i in collect:
            collected += i['FINECOLLECTED']

        return render_template('finemanager.html', total_fines=total_fines, total_amount=total_amount,
                               collected=collected)
    except Exception as e:
        return render_template('finemanager.html',
                               success_message='An error occurred while trying to handle your request', total_fines=total_fines, total_amount=total_amount,
                               collected=collected)


@app.route('/fine_manager', methods=['POST'])
@login_required
def fine_input():
    try:
        reg_no = request.form.get('reg_no').strip().upper()
        db = client['Book']
        collection = db['due_log']
        data = list(collection.find({'REGISTERNO': reg_no}, {'_id': 0}))
        
        # ------------------------------------- changes made-----------------------------------------------------------------
        if data == []:
            success_message = "No Pending Fine"
            
            return render_template('finemanager.html', total_fines=total_fines, total_amount=total_amount,
                                   collected=collected, success_message=success_message)
        # ------------------------------------------------------------------------------------------------------------------

        amount = 0
        for i in data:
            d = i['DUEDATE']
            
            due = datetime.strptime(d, '%d-%m-%Y').date()
            
            current = date.today()
            days = abs((due - current).days)
            fine = days * 2
            i['FINE'] = fine
            amount += fine

        return render_template('finemanager.html', data=data, total=amount, total_fines=total_fines,
                               total_amount=total_amount, collected=collected)
    except Exception as e:
        return render_template('finemanager.html',
                               success_message='An error occurred while trying to handle your request', total_fines=total_fines, total_amount=total_amount,
                               collected=collected)


if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=False)
