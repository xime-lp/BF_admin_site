from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///BF_admin_site.db")

admin_access = ['Treasurer', 'President']


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
    template = 'login.html'
    
    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Type a username')
            return render_template(template)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Type a password')
            return render_template(template)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        pw = request.form.get("password")
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], pw):  # type: ignore
            flash("Incorrect username or password")
            return render_template(template)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template(template)


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
    template = 'register.html'
    
    members = db.execute("SELECT name, id FROM members WHERE id NOT IN (SELECT member_id FROM members JOIN users ON members.id = users.member_id);")
    
    
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Type a username')
            return render_template(template, members=members)
        
        # Ensure password was submitted
        elif not request.form.get("email"):
            flash('Type an email')
            return render_template(template, members=members)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Type a password')
            return render_template(template, members=members)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            flash('Retype password')
            return render_template(template, members=members)

        # Ensure password and confirmation match
        elif request.form.get("confirmation") != request.form.get("password"):
            flash("Passwords don't match")
            return render_template(template, members=members)

        # make sure username does not already exist
        username = request.form.get("username")
        look_username = db.execute("SELECT username FROM users WHERE username = ?", username)

        if ' ' in username:  # type: ignore
            flash("Username cannot contain spaces")
            return render_template(template, members=members)

        if look_username:
            flash("Username already exists")
            return render_template(template, members=members)

        # hash the password
        hashed = generate_password_hash(request.form.get("password"))  # type: ignore

        email = request.form.get("email")
        member_id = request.form.get("member")
        
        
        # input new row into users dataset
        db.execute("INSERT INTO users (username, hash, email, member_id) VALUES (?, ?, ?, ?)", username, hashed, email, member_id)

        return redirect("/")
    else:
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
    template = 'add_member.html'
    colleges = ['JE', 'BR', 'SY', 'PC', 'DC', 'GH', 'BK', 'TC', 'ES', 'MC', 'TD', 'SM', 'BF', 'MY']
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("name"):
            flash('Type name')
            return render_template(template, colleges=colleges)
        
        if not request.form.get("college"):
            flash('Choose a college option')
            return render_template(template, colleges=colleges)
        
        name = request.form.get("name")
        college = request.form.get("college")
        year = request.form.get("year")
        active = request.form.get("active")
        board = request.form.get("board")
        
        db.execute("INSERT INTO members (name, college, year, active, board) VALUES (?, ?, ?, ?, ?)", name, college, year, active, board)
        
        return redirect("/members")
    
    else:
        
        return render_template('add_member.html', colleges=colleges)


@app.route("/edit_member", methods=["GET", "POST"])
def edit_member():
    template = 'edit_member.html'
    colleges = ['JE', 'BR', 'SY', 'PC', 'DC', 'GH', 'BK', 'TC', 'ES', 'MC', 'TD', 'SM', 'BF', 'MY']
    if request.method == "POST":
        member_id = request.form.get("member_id")
        member_info = db.execute("SELECT * FROM members WHERE id = ?", member_id)[0]
        return render_template(template, member=member_info, colleges=colleges)
    else:
        return redirect('/members')


@app.route("/editing", methods=["GET", "POST"])
def editing():
    template = 'edit_member.html'
    colleges = ['JE', 'BR', 'SY', 'PC', 'DC', 'GH', 'BK', 'TC', 'ES', 'MC', 'TD', 'SM', 'BF', 'MY']
    
    if request.method == 'POST':
        member_id = request.form.get("member_id")
        
        if not request.form.get('name'):
            flash('Type name')
            member_info = db.execute("SELECT * FROM members WHERE id = ?", member_id)[0]
            return render_template(template, member=member_info, colleges=colleges)

        name = request.form.get("name")
        college = request.form.get("college")
        year = request.form.get("year")
        active = request.form.get("active")
        board = request.form.get("board")
        
        db.execute("UPDATE members SET name = ?, college = ?, year = ?, active = ?, board = ? WHERE id = ?", name, college, year, active, board, member_id)
        
        return redirect('/members')
        
    
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








@app.route("/board", methods=["GET", "POST"])
def board():
    return apology("building")

@app.route("/site_accounts", methods=["GET", "POST"])
def site_accounts():
    return apology("building")

@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    return apology("building")

@app.route("/earnings", methods=["GET", "POST"])
def earnings():
    return apology("building")

@app.route("/finance_analytics", methods=["GET", "POST"])
def finance_analytics():
    return apology("building")

@app.route("/shoes", methods=["GET", "POST"])
def shoes():
    return apology("building")

@app.route("/costumes", methods=["GET", "POST"])
def costumes():
    return apology("building")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    return apology("building")