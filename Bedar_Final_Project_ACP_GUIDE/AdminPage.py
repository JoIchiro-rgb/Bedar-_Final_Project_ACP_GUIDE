import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import subprocess 

# Function to open the Admin Page
def open_AdminPage():
    # Create Admin Page Window
    AdminPage = Tk()
    AdminPage.title("Admin Page")
    AdminPage.geometry('925x500+300+200')
    AdminPage.configure(bg='white')

    # Center the window on the screen
    screen_width = AdminPage.winfo_screenwidth()
    screen_height = AdminPage.winfo_screenheight()
    x = (screen_width // 2) - (925 // 2)  # Window width is 925
    y = (screen_height // 2) - (500 // 2)  # Window height is 500
    AdminPage.geometry(f"925x500+{x}+{y}")

    img = PhotoImage(file='Admin Page.png')  # Load background image
    background_label = Label(AdminPage, image=img)
    background_label.place(relwidth=1, relheight=1)  # Fill the entire window
    background_label.image = img  # Keep reference to the image

    # Generic function to display data from a specified table
    def show_data(table_name, columns, window_title):
        try:
            # Establish connection to the MySQL database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',  # Replace with your MySQL username
                password='1234',  # Replace with your MySQL password
                database='user_db'  # Replace with your database name
            )
            cursor = connection.cursor()

            # Query to fetch data from the specified table
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Create a new window for displaying the data
            data_window = Toplevel(AdminPage)
            data_window.title(window_title)

            # Center the data window on the screen
            data_window.geometry("900x500")
            data_screen_width = data_window.winfo_screenwidth()
            data_screen_height = data_window.winfo_screenheight()
            dx = (data_screen_width // 2) - (900 // 2)  # Window width is 900
            dy = (data_screen_height // 2) - (500 // 2)  # Window height is 500
            data_window.geometry(f"900x500+{dx}+{dy}")

            # Frame to hold the Treeview and Scrollbars
            frame = Frame(data_window)
            frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

            # Create a Treeview widget to display data
            tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
            tree.pack(side=LEFT, fill=BOTH, expand=True)

            # Add vertical and horizontal scrollbars
            y_scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
            y_scrollbar.pack(side=RIGHT, fill=Y)
            x_scrollbar = Scrollbar(data_window, orient=HORIZONTAL, command=tree.xview)
            x_scrollbar.pack(side=BOTTOM, fill=X)

            # Configure the Treeview scrollbars
            tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

            # Define column headings and adjust their width
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor="center")

            # Insert rows into the Treeview
            for row in rows:
                tree.insert("", "end", values=row)

            connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Styling for buttons
    button_style = {
        "font": ("Arial", 14, "bold"),
        "bg": "#4CAF50",  # Green shade
        "fg": "white",
        "activebackground": "#45A049",  # Slightly darker green when active
        "activeforeground": "white",
        "bd": 3,  # Border width
        "relief": "raised",
        "width": 25,  # Button width
    }

    # Create a frame to hold the buttons and center them
    button_frame = Frame(AdminPage, bg="white")
    button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Button to display `user_signup` data
    signup_button = Button(button_frame, text="User Signup Data", **button_style,
                           command=lambda: show_data(
                               "USER_SIGNUP",
                               ["user_id", "fname", "lname", "username", "pw", "cpw", "gender", "date_of_birth"],
                               "User Signup Data"
                           ))
    signup_button.pack(pady=10)

    # Button to display `user_activity` data
    activity_button = Button(button_frame, text="User Activity Data", **button_style,
                              command=lambda: show_data(
                                  "user_activity",
                                  ["activity_id", "user_id", "page_name", "timestamp", "action_type"],
                                  "User Activity Data"
                              ))
    activity_button.pack(pady=10)

    # Button to display `page_session` data
    session_button = Button(button_frame, text="Page Session Data", **button_style,
                             command=lambda: show_data(
                                 "Page_Session",
                                 ["session_id", "user_id", "start_time", "end_time", "page_count"],
                                 "Page Session Data"
                             ))
    session_button.pack(pady=10)


        # Function to confirm before going back to login page
    def go_back():
        result = messagebox.askquestion("Go Back", "Are you sure you want to go back to the login page?")
        if result == 'yes':
            AdminPage.destroy()  # Close the Admin Page
            try:
                subprocess.Popen(['python', 'LoginPage.py'])  # Open LoginPage.py
            except FileNotFoundError:
                messagebox.showerror("Error", "LoginPage.py not found. Ensure the file is in the same directory.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Button to go back to login page
    back_button = Button(AdminPage, text="Go Back", font=("Arial", 14), bg="red", fg="white", command=go_back)
    back_button.place(x=0, y=0)

    AdminPage.mainloop()

# Main code execution check
if __name__ == "__main__":
    open_AdminPage()
