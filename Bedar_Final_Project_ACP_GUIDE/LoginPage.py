import mysql.connector
from tkinter import *
from tkinter import messagebox
import subprocess

def log_user_activity(user_id, page_name, action_type):
    """Logs user activity in the user_activity table."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='user_db'
        )
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user_activity (user_id, page_name, action_type) VALUES (%s, %s, %s)",
            (user_id, page_name, action_type)
        )
        connection.commit()
        connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def start_page_session(user_id):
    """Starts or updates a page session in the Page_Session table."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='user_db'
        )
        cursor = connection.cursor()
        cursor.execute(
            "SELECT session_id FROM Page_Session WHERE user_id = %s AND end_time IS NULL",
            (user_id,)
        )
        session = cursor.fetchone()
        if session:
            cursor.execute(
                "UPDATE Page_Session SET page_count = page_count + 1 WHERE session_id = %s",
                (session[0],)
            )
        else:
            cursor.execute(
                "INSERT INTO Page_Session (user_id, page_count) VALUES (%s, %s)",
                (user_id, 1)
            )
        connection.commit()
        connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


def get_user_credentials(username, password):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='user_db'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM USER_SIGNUP WHERE username = %s AND pw = %s", (username, password))
        user = cursor.fetchone()
        connection.close()
        return user
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def admin_signin():
    username = user.get()
    password = code.get()
    if username == 'Admin' and password == '1234':
        root.destroy()
        subprocess.Popen(['python', 'AdminPage.py'])
    else:
        messagebox.showerror('Invalid', 'Invalid admin username or password.')

def user_signin():
    username = user1.get()
    password = code1.get()
    user_data = get_user_credentials(username, password)
    if user_data:
        user_id, fname, lname, username = user_data[0], user_data[1], user_data[2], user_data[3]  # Adjust based on the columns returned

        log_user_activity(user_id, "Login Page", "Login")
        start_page_session(user_id)
        messagebox.showinfo("Welcome", f"Welcome, {username}!")  # Use username here
        log_user_activity(user_id, "Dashboard", "View")

        root.destroy()
        subprocess.Popen(['python', 'Dashboard.py'])
    else:
        messagebox.showerror('Invalid', 'Invalid username or password. Please try again.')

def go_to_signup():
    root.destroy()
    subprocess.Popen(['python', 'Signup.py'])

def create_login_page():
    global root, user, code, user1, code1
    root = Tk()
    root.title('LoginPage')
    root.geometry('925x500+300+200')
    root.configure(bg='#fff')
    root.resizable(False, False)

    img = PhotoImage(file='Login Page.png')
    background_label = Label(root, image=img)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = img

    frame = Frame(root, width=250, height=200, bg='#fae2d4', bd=2, relief="solid")
    frame.place(x=40, y=150)

    heading = Label(frame, text='Admin', fg='#57a1f8', bg='#fae2d4', font=('Arial', 18, 'bold'))
    heading.place(x=85, y=5)

    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Username')

    user = Entry(frame, width=20, fg='black', border=2, bg='white', font=('Arial', 14))
    user.place(x=10, y=65)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    def on_enter(e):
        code.delete(0, 'end')

    def on_leave(e):
        name = code.get()
        if name == '':
            code.insert(0, 'Password')

    def toggle_password_visibility():
        if code.cget('show') == '':
            code.config(show='*')
            toggle_button.config(text='SHOW')
        else:
            code.config(show='')
            toggle_button.config(text='HIDE')

    code = Entry(frame, width=15, fg='black', border=2, bg='white', font=('Arial', 14), show='*')
    code.place(x=10, y=100)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    toggle_button = Button(frame, text='SHOW', command=toggle_password_visibility, pady=2)
    toggle_button.place(x=190, y=100)

    button = Button(frame, width=15, pady=7, text='Login', bg='#57a1f8', fg='white', border=0, command=admin_signin)
    button.place(x=70, y=150)

    frame1 = Frame(root, width=250, height=200, bg='#fae2d4', bd=2, relief="solid")
    frame1.place(x=635, y=150)

    heading1 = Label(frame1, text='Login', fg='#57a1f8', bg='#fae2d4', font=('Arial', 18, 'bold'))
    heading1.place(x=90, y=5)

    def on_enter(e):
        user1.delete(0, 'end')

    def on_leave(e):
        name = user1.get()
        if name == '':
            user1.insert(0, 'Username')

    user1 = Entry(frame1, width=20, fg='black', border=2, bg='white', font=('Arial', 14))
    user1.place(x=10, y=65)
    user1.insert(0, 'Username')
    user1.bind('<FocusIn>', on_enter)
    user1.bind('<FocusOut>', on_leave)

    def on_enter(e):
        code1.delete(0, 'end')

    def on_leave(e):
        name = code1.get()
        if name == '':
            code1.insert(0, 'Password')

    def toggle_password_visibility_user():
        if code1.cget('show') == '':
            code1.config(show='*')
            toggle_button_user.config(text='SHOW')
        else:
            code1.config(show='')
            toggle_button_user.config(text='HIDE')

    code1 = Entry(frame1, width=15, fg='black', border=2, bg='white', font=('Arial', 14), show='*')
    code1.place(x=10, y=100)
    code1.insert(0, 'Password')
    code1.bind('<FocusIn>', on_enter)
    code1.bind('<FocusOut>', on_leave)

    toggle_button_user = Button(frame1, text='SHOW', command=toggle_password_visibility_user, pady=2)
    toggle_button_user.place(x=190, y=100)

    button1 = Button(frame1, width=15, pady=7, text='Login', bg='#57a1f8', fg='white', border=0, command=user_signin)
    button1.place(x=70, y=150)

    label = Label(text='Don\'t have an account?', fg='black', bg='#fae2d4', font=('Arial', 9))
    label.place(x=655, y=370)

    sign_up = Button(width=6, text='Sign-up', border=0, bg='#fae2d4', cursor='hand2', fg='#57a1f8', command=go_to_signup)
    sign_up.place(x=785, y=370)


    root.mainloop()

if __name__ == "__main__":
    create_login_page()
