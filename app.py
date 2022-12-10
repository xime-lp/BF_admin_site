from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, send_file
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from openpyxl import Workbook, load_workbook

from helpers import apology, login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///BF_admin_site.db")

admin_access = ['Treasurer', 'President']

path = './finances_BF.xlsx'


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response






@app.route("/")
@login_required
def index():
    return apology("building")







@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Type a username')
            return redirect('/login')

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Type a password')
            return redirect('/login')

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        pw = request.form.get("password")
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], pw):  # type: ignore
            flash("Incorrect username or password")
            return redirect('/login')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Type a username')
            return redirect('/register')
        
        # Ensure password was submitted
        elif not request.form.get("email"):
            flash('Type an email')
            return redirect('/register')

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Type a password')
            return redirect('/register')

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            flash('Retype password')
            return redirect('/register')

        # Ensure password and confirmation match
        elif request.form.get("confirmation") != request.form.get("password"):
            flash("Passwords don't match")
            return redirect('/register')

        # make sure username does not already exist
        username = request.form.get("username")
        look_username = db.execute("SELECT username FROM users WHERE username = ?", username)

        if ' ' in username:  # type: ignore
            flash("Username cannot contain spaces")
            return redirect('/register')

        if look_username:
            flash("Username already exists")
            return redirect('/register')

        # hash the password
        hashed = generate_password_hash(request.form.get("password"))  # type: ignore

        email = request.form.get("email")
        member_id = request.form.get("member")
        
        
        # input new row into users dataset
        db.execute("INSERT INTO users (username, hash, email, member_id) VALUES (?, ?, ?, ?)", username, hashed, email, member_id)

        return redirect("/")
    
    
    else:
        members = db.execute("SELECT name, id FROM members WHERE id NOT IN (SELECT member_id FROM members JOIN users ON members.id = users.member_id);")
        return render_template("register.html", members=members)
    





@app.route("/members")
def members():
        
    members = db.execute("SELECT * FROM members")
    for member in members:
        if member["active"]:
            member["active"] = 'Yes'
        else:
            member["active"] = 'No'
    
    return render_template("member_list.html", members=members)

@app.route("/add_member", methods=["GET", "POST"])
def add_member():
    
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("name"):
            flash('Type name')
            return redirect('/add_member')
        
        if not request.form.get("college"):
            flash('Choose a college option')
            return redirect('/add_member')
        
        name = request.form.get("name")
        college = request.form.get("college")
        year = request.form.get("year")
        active = request.form.get("active")
        
        db.execute("INSERT INTO members (name, college, year, active, board) VALUES (?, ?, ?, ?, 0)", name, college, year, active)
        
        return redirect("/members")
    
    else:
        colleges = ['JE', 'BR', 'SY', 'PC', 'DC', 'GH', 'BK', 'TC', 'ES', 'MC', 'TD', 'SM', 'BF', 'MY']
        return render_template('add_member.html', colleges=colleges)


@app.route("/edit_member", methods=["GET", "POST"])
def edit_member():
    if request.method == "POST":
        member_id = request.form.get("member_id")
        member_info = db.execute("SELECT * FROM members WHERE id = ?", member_id)[0]
        colleges = ['JE', 'BR', 'SY', 'PC', 'DC', 'GH', 'BK', 'TC', 'ES', 'MC', 'TD', 'SM', 'BF', 'MY']
        return render_template('edit_member.html', member=member_info, colleges=colleges)
    else:
        return redirect('/members')


@app.route("/editing_member", methods=["GET", "POST"])
def editing_member():
    
    
    if request.method == 'POST':
        member_id = request.form.get("member_id")
        
        if not request.form.get('name'):
            flash('Type name')
            member_info = db.execute("SELECT * FROM members WHERE id = ?", member_id)[0]
            colleges = ['JE', 'BR', 'SY', 'PC', 'DC', 'GH', 'BK', 'TC', 'ES', 'MC', 'TD', 'SM', 'BF', 'MY']
            return render_template('edit_member.html', member=member_info, colleges=colleges)

        name = request.form.get("name")
        college = request.form.get("college")
        year = request.form.get("year")
        active = request.form.get("active")
        
        db.execute("UPDATE members SET name = ?, college = ?, year = ?, active = ? WHERE id = ?", name, college, year, active, member_id)        
    
    return redirect('/members')

'''
ADD A WARNING TO A DELETION
@app.route("/warning_delete", methods=["GET", "POST"])
def delete_member():
'''

@app.route("/delete_member", methods=["GET", "POST"])
def delete_member():
    
    if request.method == 'POST':
        member_id = request.form.get("member_id")
        db.execute("DELETE FROM members WHERE id = ?", member_id)
    
    return redirect('/members')








@app.route("/board")
def board():
    template = 'board_list.html'
    board = db.execute('SELECT member_id, name, position FROM board JOIN members ON board.member_id = members.id')
    return render_template(template, board=board)



@app.route("/add_board", methods=["GET", "POST"])
def add_board():
    
    if request.method == 'POST':
        
        member_id = request.form.get('member')
        position = request.form.get('position')
        
        if not member_id:
            flash('Choose a new board member')
            return redirect('/add_board')
        
        elif not position:
            flash('Type a board position')
            return redirect('/add_board')
        
        db.execute("INSERT INTO board (member_id, position) VALUES (?, ?)", member_id, position)
        
        return redirect('/board')
    else:
        members = db.execute("SELECT name, id FROM members WHERE id NOT IN (SELECT member_id FROM board JOIN members ON board.member_id = members.id)")
        return render_template('add_board.html', members=members)


@app.route("/delete_board", methods=["GET", "POST"])
def delete_board():
    
    if request.method == 'POST':
        member_id = request.form.get("member_id")
        db.execute("DELETE FROM board WHERE member_id = ?", member_id)
    
    return redirect('/board')


@app.route("/edit_board", methods=["GET", "POST"])
def edit_board():
    
    template = 'edit_board.html'
    
    if request.method == 'POST':
        member_id = request.form.get("member_id")
        person = db.execute("SELECT name, position, member_id FROM board JOIN members ON board.member_id = members.id WHERE member_id = ?", member_id)[0]
        return render_template(template, person=person)
    else:
        return redirect('/board')



@app.route("/editing_board", methods=["GET", "POST"])
def editing_board():
    
    if request.method == 'POST':
        member_id = request.form.get("member_id")
        print(member_id)
        position = request.form.get('position')
        
        if not position:
            flash('Type a board position')
            person = db.execute("SELECT name, position, member_id FROM board JOIN members ON board.member_id = members.id WHERE member_id = ?", member_id)[0]
            return render_template('edit_board.html', person=person)
        
        db.execute("UPDATE board SET position = ? WHERE member_id = ?", position, member_id)
        
    return redirect('/board')





@app.route("/site_accounts")
def site_accounts():
    accounts = db.execute("SELECT id, username, member_id FROM users")
    for account in accounts:
        if account['member_id']:
            name = db.execute("SELECT name FROM members WHERE id = ?", account['member_id'])[0]['name']
            account['name'] = name
        else:
            account['name'] = '-'
    return render_template('site_accounts.html', accounts=accounts)



@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if request.method == 'POST':
        account_id = request.form.get('id')
        db.execute("DELETE FROM users WHERE id = ?", account_id)
    return redirect('/site_accounts')
    



@app.route("/purchases")
def purchases():
    purchases = db.execute("SELECT * FROM purchases")
    for purchase in purchases:
        if purchase['covered']:
            purchase['covered'] = 'Yes'
        else:
            purchase['covered'] = 'No'
    return render_template('purchases.html', purchases=purchases)


@app.route("/add_purchase", methods=["GET", "POST"])
def add_purchase():
    
    if request.method == 'POST':
        
        date = request.form.get('date')
        total = request.form.get('total')
        vendor = request.form.get('vendor')
        
        if not date:
            flash('Select a date')
            redirect('/add_purchase')
        
        elif not total:
            flash('Type in total')
            return redirect('/add_purchase')
        
        elif not vendor:
            flash('Type in vendor')
            return redirect('/add_purchase')
        
        buyer_id = request.form.get('buyer_id')
        description = request.form.get('desc')
        covered = request.form.get('covered')
        payment_type = request.form.get('payment_type')
        
        date_values = str(date).split('-')
        year = date_values[0]
        month = date_values[1]
        day = date_values[2]
        
        user_id = session["user_id"]
        if db.execute('SELECT member_id FROM users WHERE id = ?', user_id):
            member_id = db.execute('SELECT member_id FROM users WHERE id = ?', user_id)[0]['member_id']
        else:
            member_id = None
        
        db.execute('INSERT INTO purchases (member_id, total, place, payment_type, buyer_id, covered, year, month, day, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', member_id, total, vendor, payment_type, buyer_id, covered, year, month, day, description)

        return redirect('/purchases')
    
    else:
        members = db.execute("SELECT name, id FROM members")
        return render_template('add_purchase.html', members=members)







@app.route("/earnings", methods=["GET", "POST"])
def earnings():
    return apology("building")



@app.route("/finance_analytics", methods=["GET", "POST"])
def finance_analytics():
    return render_template('finance_analytics.html')

@app.route('/return-files/', methods=["GET", "POST"])
def return_files_tut():
    
    if request.method == 'POST':
        update_finances_excel()
        
        # REFERENCE
        try:
            return send_file(path, as_attachment=True)
        except Exception as e:
            return str(e)
    else:
        return redirect('/finance_analytics')
    
    

def update_finances_excel():
    
    '''
    Saves all the current earnings and purchases to Excel file
        sources:
        https://www.geeksforgeeks.org/how-to-iterate-through-excel-rows-in-python/ 
        https://openpyxl.readthedocs.io/en/latest/api/openpyxl.workbook.workbook.html
    '''
    workbook = load_workbook(path)
    sheet =  workbook.active
    
    #https://www.folkstalk.com/2022/10/how-to-delete-every-row-in-excel-using-openpyxl-with-code-examples.html
    sheet.delete_rows(1, sheet.max_row+1)
    
    headers = ['Date', 'Total', 'Vendor / Source', 'Registered by', 'Description']
    sheet.append(headers)
    
    purchases = db.execute('SELECT year, month, day, name, total, place, description FROM purchases JOIN members ON purchases.member_id = members.id')
    earnings = db.execute('SELECT year, month, day, name, total, source, notes FROM earnings JOIN members ON earnings.member_id = members.id')
    
    purchases_formatted = []
    earnings_formatted = []
    
    # tutorialspoint.com/How-to-convert-Python-Dictionary-to-a-list
    for purchase in purchases:
        purchase['total'] = "-${0}".format(purchase['total'])
        purchase['date'] = "{0}/{1}/{2}".format(purchase['month'], purchase['day'], purchase['year'])
        purchases_formatted.append([purchase['date'], purchase['total'], purchase['place'], purchase['name'], purchase['description']])
        #sheet.append(purchase.values())
    
    for earning in earnings:
        earning['total'] = "+${0}".format(earning['total'])
        earning['date'] = "{0}/{1}/{2}".format(earning['month'], earning['day'], earning['year'])
        earnings_formatted.append([earning['date'], earning['total'], earning['source'], earning['name'], earning['notes']])
    
    for purchase in purchases_formatted:
        sheet.append(purchase)
    
    for earning in earnings_formatted:
        sheet.append(earning)
    
    workbook.save(path)




@app.route("/shoes", methods=["GET", "POST"])
def shoes():
    return apology("building")

@app.route("/costumes", methods=["GET", "POST"])
def costumes():
    return apology("building")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    return apology("building")