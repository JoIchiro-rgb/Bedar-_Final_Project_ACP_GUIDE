import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import subprocess  # Import subprocess to run external Python files

# Create the main window
window = Tk()
window.title('Sign-up')
window.geometry('925x600+300+100')
window.configure(bg='#fff')
window.resizable(False, False)

# Load the background image
img1 = PhotoImage(file='Sign-up Back_Ground_Page.png')  # Load the background image
background_label = Label(window, image=img1)
background_label.place(relwidth=1, relheight=1)  # Fill the window with the background

# Load the logo image
img = PhotoImage(file='LOGO Sign_up.png')  # Load the logo image
logo_label = Label(window, image=img, border=0, bg='white')  # Adjust bg for better visibility
logo_label.place(x=-30, y=75)  # Place the logo in the desired position

# Create a frame for the form
frame = Frame(window, width=400, height=600, bg='#88d7df')
frame.place(x=360, y=45)

heading = Label(frame, text='Sign-up', fg='#57a1f8', bg='#88d7df', font=('Arial', 23, 'bold'))
heading.place(x=100, y=5)

# First Name Entry
def on_enter_fname(e):
    fname.delete(0, 'end')

def on_leave_fname(e):
    if fname.get() == '':
        fname.insert(0, 'First Name')

fname = Entry(frame, width=25, fg='black', border=0, bg='#88d7df', font=('Arial', 12))
fname.place(x=30, y=80)
fname.insert(0, 'First Name')
fname.bind('<FocusIn>', on_enter_fname)
fname.bind('<FocusOut>', on_leave_fname)
Frame(frame, width=320, height=2, bg='black').place(x=30, y=107)

# Last Name Entry
def on_enter_lname(e):
    lname.delete(0, 'end')

def on_leave_lname(e):
    if lname.get() == '':
        lname.insert(0, 'Last Name')

lname = Entry(frame, width=25, fg='black', border=0, bg='#88d7df', font=('Arial', 12))
lname.place(x=30, y=130)
lname.insert(0, 'Last Name')
lname.bind('<FocusIn>', on_enter_lname)
lname.bind('<FocusOut>', on_leave_lname)
Frame(frame, width=320, height=2, bg='black').place(x=30, y=157)

# Username Entry
def on_enter_user(e):
    user.delete(0, 'end')

def on_leave_user(e):
    if user.get() == '':
        user.insert(0, 'Enter Username')
        
user = Entry(frame, width=25, fg='black', border=0, bg='#88d7df', font=('Arial', 12))
user.place(x=30, y=177)
user.insert(0, 'Enter Username')
user.bind('<FocusIn>', on_enter_user)
user.bind('<FocusOut>', on_leave_user)
Frame(frame, width=320, height=2, bg='black').place(x=30, y=207)

# Password and Confirm Password
def toggle_password(entry, btn):
    if entry.cget('show') == '':
        entry.config(show='*')
        btn.config(text='Show')
    else:
        entry.config(show='')
        btn.config(text='Hide')

def on_enter_user(e):
    pw.delete(0, 'end')

def on_leave_user(e):
    if pw.get() == '':
        pw.insert(0, 'Password')

pw = Entry(frame, width=25, fg='black', border=0, bg='#88d7df', font=('Arial', 12), show="*")
pw.place(x=30, y=227)
pw.insert(0, 'Password')
pw.bind('<FocusIn>', on_enter_user)
pw.bind('<FocusOut>', on_leave_user)
Frame(frame, width=320, height=2, bg='black').place(x=30, y=257)

pw_show_btn = Button(frame, text='Show', command=lambda: toggle_password(pw, pw_show_btn), bg='#88d7df', fg='black', border=0, font=('Arial', 10))
pw_show_btn.place(x=350, y=227)

def on_enter_user(e):
    cpw.delete(0, 'end')

def on_leave_user(e):
    if cpw.get() == '':
        cpw.insert(0, 'Confirm Password')

cpw = Entry(frame, width=25, fg='black', border=0, bg='#88d7df', font=('Arial', 12), show="*")
cpw.place(x=30, y=277)
cpw.insert(0, ' Confirm Password')
cpw.bind('<FocusIn>', on_enter_user)
cpw.bind('<FocusOut>', on_leave_user)
Frame(frame, width=320, height=2, bg='black').place(x=30, y=307)

cpw_show_btn = Button(frame, text='Show', command=lambda: toggle_password(cpw, cpw_show_btn), bg='#88d7df', fg='black', border=0, font=('Arial', 10))
cpw_show_btn.place(x=350, y=277)

# Gender Selection
gender_var = StringVar(value="None")
gender_label = Label(frame, text="Gender", fg="black", bg="#88d7df", font=("Arial", 12))
gender_label.place(x=30, y=327)

Radiobutton(frame, text="Male", variable=gender_var, value="Male", bg="#88d7df", font=("Arial", 10)).place(x=30, y=357)
Radiobutton(frame, text="Female", variable=gender_var, value="Female", bg="#88d7df", font=("Arial", 10)).place(x=100, y=357)

# Birthday Input
birthday_label = Label(frame, text="Birthday", fg="black", bg="#88d7df", font=("Arial", 12))
birthday_label.place(x=30, y=387)

day_var = StringVar(value="Day")
month_var = StringVar(value="Month")
year_var = StringVar(value="Year")

day_dropdown = ttk.Combobox(frame, textvariable=day_var, values=[str(i) for i in range(1, 32)], width=5, state="readonly")
day_dropdown.place(x=30, y=417)

month_dropdown = ttk.Combobox(frame, textvariable=month_var, values=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], width=10, state="readonly")
month_dropdown.place(x=90, y=417)

year_dropdown = ttk.Combobox(frame, textvariable=year_var, values=[str(i) for i in range(1900, 2025)], width=8, state="readonly")
year_dropdown.place(x=200, y=417)

# Function to handle Sign Up
def sign_up():
    fname_val = fname.get()
    lname_val = lname.get()
    username_val = user.get()
    pw_val = pw.get()
    cpw_val = cpw.get()
    gender_val = gender_var.get()
    
    # Check if any required fields are empty
    if (fname_val == '' or fname_val == 'First Name' or
        lname_val == '' or lname_val == 'Last Name' or
        username_val == '' or username_val == 'Enter Username' or
        pw_val == '' or cpw_val == '' or
        gender_val == 'None' or
        day_var.get() == 'Day' or month_var.get() == 'Month' or year_var.get() == 'Year'):
        
        messagebox.showwarning("Input Error", "Please fill in all required fields!")
        return
    
    # Map months to numeric values
    month_map = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
        "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }

    # Create DOB string in YYYY-MM-DD format
    dob = f"{year_var.get()}-{month_map.get(month_var.get(), '01')}-{int(day_var.get()):02d}"
    
    if pw_val != cpw_val:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    try:
        connection = mysql.connector.connect(
            host='localhost',  # Adjust with your database host
            user='root',  # Replace with your username
            password='1234',  # Replace with your password
            database='user_db'  # Replace with your database name
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM USER_SIGNUP WHERE username = %s", (username_val,))
        result = cursor.fetchone()
        if result:
            messagebox.showerror("Error", "Username already exists!")
        else:
            cursor.execute("INSERT INTO USER_SIGNUP (fname, lname, username, pw, cpw, gender, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (fname_val, lname_val, username_val, pw_val, cpw_val, gender_val, dob))
            connection.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            open_login_page()  # Open the login page after successful signup
            window.destroy()  # Close the signup window
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Function to open login page
def open_login_page():
    messagebox.showinfo("Redirecting", "Navigating to Login Page...")
    subprocess.Popen(['python', 'LoginPage.py'])
    window.destroy()

# Create Sign Up and Back to Login buttons
sign_up_button = Button(frame, text='Sign Up', fg='white', bg='#57a1f8', font=('Arial', 15), relief=SOLID, command=sign_up)
sign_up_button.place(x=65, y=470)

back_button = Button(frame, text='Back to Login', fg='white', bg='#57a1f8', font=('Arial', 15), relief=SOLID, command=open_login_page)
back_button.place(x=170, y=470)

window.mainloop()
