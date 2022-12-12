# BF Admin Site - Design

BF Admin Site incorporates two main components, an SQL database and a Python Flask application.

## Databases
The website employs five databases: 'users', 'members', 'board', 'purchases' and 'earnings'.

#### Members
Responsible for storing the group's members. For each person it stores their name, college, graduation year, if they are in the board and if they are active. It also automatically assigns them an id. 

The structure of the table is the following:
```SQL
CREATE TABLE members (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT NOT NULL,
  college TEXT,
  grad_year TEXT,
  board BOOL,
  active BOOL
);
```
#### Users
Responsible for storing the accounts in the website. For each account, it stores the username, the hashed password, the email, and the member id. It automatically assigns them an id. The member id references the members table and links these two tables together. This way, members can exist inside the members table without having an account in the website, but user accounts are guaranteed to be linked to a member. 

Within the Flask app, the functions 'check_password_hash' and 'generate_password_hash' are used to convert passwords from plain text to more secure forms for storage in the hash column and viceversa.

The structure of the table is the following:
```SQL
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  username TEXT,
  hash TEXT,
  email TEXT,
  member_id INTEGER,
  FOREIGN KEY (member_id) REFERENCES members (id)
);
```
#### Board
Responsible for storing the group members that are part of the board. It stores the member id and the position of the person on the board. The member id references the members table and links these two tables together. This way, members can easily be taken on and off the board without affecting their status as members and board positions can also be easily changed when needed.

The structure of the table is the following:
```SQL
CREATE TABLE board (
  member_id INTEGER,
  position TEXT,
  FOREIGN KEY (member_id) REFERENCES members (id)
);
```

#### Purchases
Responsible for storing the group's purchases. It stores the total, the vendor (place), the description, the member id of the person who registered the purchase using the website, the buyer id of the person who physically paid for the purchase, and the date of the purchase divided into year, month, and day. 

Both the member id and buyer id reference the members column to have access to information about the members. As treasurer, it is important for me to know when someone paid for a purchase using their own money so I know to pay them back. Hence, it is useful to have a column that easily shows when this occurs. Similarly, since this website is intended to be used by multiple people, it is useful to keep track of who records purchases in case they need to be edited.

The structure of the table is the following:
```SQL
CREATE TABLE purchases (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  member_id INTEGER,
  total NUMERIC,
  place TEXT,
  buyer_id INTEGER,
  description TEXT, 
  year INTEGER, 
  month INTEGER, 
  day INTEGER,
  FOREIGN KEY (member_id) REFERENCES members (id),
  FOREIGN KEY (buyer_id) REFERENCES members (id)
);
```

#### Earnings
Responsible for storing the group’s earnings. It stores the total, the source, the description (notes), the member id of the person who registered the earnings using the website, and the date of the purchase divided into year, month, and day.

The member id referencse the members column to have access to information about the members. As with purchases, it is useful to keep track of who registers the group's earnings in case edits have to be made.

The structure of the table is the following:
```SQL
CREATE TABLE earnings (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  total NUMERIC,
  source TEXT,
  notes TEXT,
  member_id INTEGER, 
  year INTEGER, 
  month INTEGER, 
  day INTEGER,
  FOREIGN KEY (member_id) REFERENCES members (id)
);
```

## Flask App (Python)
The website uses Flask to create a responsive web application that is easily accessible in multiple platforms, thus, allowing multiple members from Ballet Folklórico to use it. 

#### Displaying, adding, editing, and deleting data from databases
The web app employs very similar functionalities to display, add, edit and delete data from the five databases outlined above. Hence, I will focus on the 'members' database to explain their basic functionality.

Firstly, the program has a function to obtain data from the database by using the SQL portion of the CS50 library in the following way:
```Python
members = db.execute("SELECT * FROM members")
```
The program then formats the data in a more readable way if it is needed and passes it into the HTML template:
```Python
return render_template("member_list.html", members=members)
```

Secondly, the program uses GET and POST methods to add data to the database. The GET method is used to render the HTML template with a <form> tag similar to the following:
```HTML
<form action="/add_member" method="post">
```
When the form is submitted, the POST method is used to obtain the user's input. The data is formatted correctly for input into SQL if needed and is added to the table in this manner:
```Python
db.execute("INSERT INTO members (name, college, grad_year, active, board) VALUES (?, ?, ?, ?, 0)", name, college, year, active)
```
Throughout the web app, the program uses flash messages to alert the user of an incorrect input and then redirects them to the page they were first at so they can correct their input:
```Python
# ensure a name was submitted
if not request.form.get("name"):
    flash('Type name')
    return redirect('/add_member')
```

Thirdly, the edit functionality works very similar to the add functionality. The one key difference is that there is an additional step before the program can get the inputs users. Each item in a list comes with an edit button that includes the item's id as a value. When the button is hit, a function is run to obtain the current values of the item (for example, name, college, etc). These values are then used to pre-populate an HTML file so it is easier for the user to make changes. Once this is done, the user's inputs go to the backend for processing just as when data is added.

Finally, the delete functionality also employs a button that includes an item's id value, just as the edit functionality. When it is clicked, a warning message is flashed on the HTML using JavaScript:
```HTML
<script>
    function confirmMemberDelete() {
        if (confirm('Are you sure you want to delete this member?')) {
            // The user clicked "OK", so return true to indicate that the form should be submitted
            return true;
        } else {
            // The user clicked "Cancel", so return false to prevent the form from being submitted
            return false; }
    }
</script>
```
When the user hits confirm, the id of the item is obtained from the page and the following SQL command is run:
```Python
db.execute("DELETE FROM members WHERE id = ?", member_id)
```

#### Making interactive graphs with Bokeh
The graphs displaying monthly totals on the 'Finance Analytics' page were created using the [Bokeh Python library](https://docs.bokeh.org/en/latest/). I will exemplify the process using purchases as an example. Firstly, data is obtained from the SQL database. Then a library is initiated to store the totals from each month. Then the program loops through every purchase, formats the month and year, and creates a tuple (month, year) to be used as a key in the dictionary. This way, the graphs differentiate between "november 2022" and "november 2021". Finally, it updates the monthly total by adding the purchase's total or initializes the values if it does not exist in the dictionary:

```Python
# use the key tuple to update the appropriate key-value pair or create a new pair if it doesn't exist
monthly_totals[key] = monthly_totals.get(key, 0) + total
```

After this, two lists are creates, x and y. Year, month pair values are added to the x list with an appropriate format and total values are added to the y list. To ensure that the graph displays the months in order, the following code is used:
```Python
# creates a zip object to pair up appropriate x, y pairs
xy_pairs = zip(x, y)
    
# sort the zip in descending order based on month-year values (i.e. set 2022 september before 2022 november)
xy_pairs = sorted(xy_pairs, key=lambda pair: pair[0], reverse=True)

# unzip the sorted values and send them back to the correct list
x, y = zip(*xy_pairs)

# create a range for the x-axis based on the values from the x list
# this is needed to have non numerical values in the x axis of the Bokeh plot
x_range = FactorRange(factors=x)
```

Finally, the plot is created using the following code:
```Python
# create a new Bokeh plot with a title and axis labels
p = figure(title=None, x_axis_label="month", y_axis_label="total", x_range=x_range, min_border_bottom=0)

# add a bars with colors and a legend
p.vbar(x=x, top=y, legend_label=legend, width=0.2, bottom=0, color=color)
```

Bokeh returns a <div> element and a <script> element to be embedded in the HTML template and provide the correct graph format. These two components are passed along when the template is rendered.

#### Creating and exporting an Excel file
The library Openpyxl is used to access and edit Excel files, and the send_file functionality from Flask is used to send the Excel file to the user. Firstly, the Excel file is opened from a pre-configured path, its contents are deleted and the appropriate headings are added:
```Python
# open a workbook and a worksheet
workbook = load_workbook(path)
sheet =  workbook.active

# delete everything in the worksheet
sheet.delete_rows(1, sheet.max_row+1)

# append the headers to the sheet
headers = ['Date', 'Total', 'Vendor / Source', 'Registered by', 'Description']
sheet.append(headers)
```

After this, the program obtains data from the databases, formats it to be readable in an Excel file, and uses the sheet.append() function to add it to file. Finally, the program saves the workbook back in the pre-configured path.

The program then uses send_file to send the Excel file as an export to the user per the following:
```Python
# send excel as an attachment
try:
    return send_file(path, as_attachment=True)
except Exception as e:
    return str(e)
```

## References
Made with the help of the following resources:
- https://www.youtube.com/watch?v=Rq2G_jfL_4g&ab_channel=TechnoDine
- https://github.com/realpython/flask-bokeh-example/blob/master/tutorial.md
- https://www.geeksforgeeks.org/how-to-iterate-through-excel-rows-in-python/ 
- https://openpyxl.readthedocs.io/en/latest/api/openpyxl.workbook.workbook.html
- https://docs.bokeh.org/en/latest/
- https://tedboy.github.io/flask/generated/flask.send_file.html
- https://www.sqlite.org/docs.html
- https://flask.palletsprojects.com/en/2.2.x/patterns/flashing/
- https://sebhastian.com/javascript-confirmation-yes-no/#:~:text=You%20can%20create%20a%20JavaScript,can%20specify%20as%20its%20argument.
- https://getbootstrap.com/docs/5.2/getting-started/introduction/
- https://www.folkstalk.com/2022/10/how-to-delete-every-row-in-excel-using-openpyxl-with-code-examples.html