# BF Admin Site

BF Admin Site is a website made for Ballet Folklórico Mexicano de Yale to easily keep track of group members, board members, purchases, and earnings. 

Usage video found [here](https://youtu.be/zS9xF2WrLho)

## Initialization
Download the zip file and unzip its contents.
Navigate to the unzipped file using the command terminal. It should show something similar to this:
```bash
.../BF_admin_site $
```
Once here, start the application by typing:
```bash
.../BF_admin_site $ Flask run
```
The output should include the following line:
```bash
 * Running on [http address]
```

Copy the http address and access it in a browser (ex. Google Chrome, Safari, etc.)

## Registering for an account
You will need an account to access the functionalities of the website.

If you have never used the program, you will have to sign up for an account. Click on 'Register' on the top right corner. Choose a username and password and type your email. If you are group member, you should choose your name from the dropdown menu. For CS50 purposes, some dummy group member profiles have been created and you should choose one of these unless your name pops up in the dropdown menu.

Once your account is created, you will be redirected to the login page. Type your username and password to log in. 

If you already have an account, click on 'Log In' on the top right and enter your credentials.

## Main Page
Click on the buttons to navigate to some parts of the website or use the navigation bar at the top.

## 'People' section
Click on 'People' in the navigation bar to display a dropdown menu. Use it to navigate between 'Members', 'Board', and 'Accounts'.

#### Members
This page lists all the members in the dance group, their college, their graduation year, and if they are currently active in the group. 

New members can be added by clicking the 'Add member' button at the bottom of the page. When adding a new member, be sure to type in a name and choose a college (there is a None option for non-undergrad people) before hitting the 'Add' button. The 'year' field can be left blank. New members are considered to be active by default. To change this, click on the dropdown menu under 'Active'. Click on 'Cancel' to return to the members list.

Members can be edited by clicking on the 'Edit' button in their row. Be sure to type in a name and choose a college (there is a None option for non-undergrad people) before hitting the 'Save' button. Click on 'Cancel' to return to the members list.

Members can be deleted by clicking on the 'Delete' button in their row. A warning will pop up asking you to confirm the deletion. Click on 'Ok' to proceed or on 'Cancel' to go back.

Every account on the website needs to be associated with a member profile. Hence, if you are new, an existing member will have to create a member profile for you before you can sign up for an account on the website.

#### Board
This page lists the names and positions of the people on the executive board of the group.

New board members can be added by clicking the ‘Add Board Member’ button at the bottom of the page. When adding a new member to the board, be sure to select the member's name from the dropdown menu and type in their position before hitting the ‘Add’ button. Click on ‘Cancel’ to return to the board members list.

Board members can be edited by clicking on the ‘Edit’ button in their row. Be sure to select the member's name from the dropdown menu and type in their position before hitting the ‘Add’ button. Click on ‘Cancel’ to return to the board members list.

Members can be removed from the board by clicking on the ‘Delete’ button in their row. A warning will pop up asking you to confirm the deletion. Click on ‘Ok’ to proceed or on ‘Cancel’ to go back.

A person must be added to the members list before they can be added to the board.

#### Site accounts
This page lists the usernames of the accounts on the website and the group members they belong to. 

New site accounts cannot be added through this interface as new users must complete the registration process on their own.

The website currently supports deletion of site accounts. To delete an account, click on the ‘Delete’ button in their row. A warning will pop up asking you to confirm the deletion. Click on ‘Ok’ to proceed or on ‘Cancel’ to go back.

## 'Finances' section
Click on 'Finances' in the navigation bar to display a dropdown menu. Use it to navigate between 'Purchases', 'Earnings', and 'Analytics'.

#### Purchases
This page shows a list of the group's purchases. It displays a purchase's date, total, vendor, who paid for it (bought by), who registered it on the website (registered by), and its description.

New purchases can be added by clicking the ‘Add Purchase’ button at the bottom of the page. When adding a new purchase, be sure to choose a date from the calendar dropdown, type in a total, and type in the vendor before hitting the ‘Add’ button. The ‘Purchased by’ and 'Description' fields can be left blank. Click on ‘Cancel’ to return to the members list.

Purchases can be edited by clicking on the ‘Edit’ button in their row. choose a date from the calendar dropdown, type in a total, and type in the vendor before hitting the ‘Save’ button. Click on ‘Cancel’ to return to the purchases list.

Purchases can be deleted by clicking on the ‘Delete’ button in their row. A warning will pop up asking you to confirm the deletion. Click on ‘Ok’ to proceed or on ‘Cancel’ to go back.

#### Earnings
This page shows a list of the group’s earnings. It displays their date, total, source, who registered it on the website (registered by), and their description.

New earnings can be added by clicking the ‘Add Earning’ button at the bottom of the page. When adding a new earning, be sure to choose a date from the calendar dropdown, type in a total, and type in the source before hitting the ‘Add’ button. The ‘Description’ field can be left blank. Click on ‘Cancel’ to return to the earnings list.

earnings can be deleted by clicking on the ‘Delete’ button in their row. A warning will pop up asking you to confirm the deletion. Click on ‘Ok’ to proceed or on ‘Cancel’ to go back.

#### Analytics
This page displays two graphs showing the monthly totals for purchases and earnings, and lets you download an Excel file with purchases and earnings records.

The graphs, made with the [Bokeh library](https://docs.bokeh.org/en/latest/), are interactive and let the user zoom in and out, move the graph around, and even download it. To do this, use the tools on the top right of each graph.

Scroll down to view the 'Download Excel file' section. Click 'Download!' to export an Excel with all purchases and earnings that have been recorded. Alternatively, choose a date range using the dropdowns to limit the number of records included in the Excel file. If you select range, be sure to pick both a start date and an end date.



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

## 

## About the Developer
Hi, my name is Ximena Leyva. I am a Class of 2025 Yale College student majoring in Chemistry and considering maybe possibly double majoring in CS. I was born and grew up in Mexico City and I now call Jonathan Edwards my home. 
For anything related to this project (or even life in general), you can contact me at: ximena.leyvaperalta@yale.edu