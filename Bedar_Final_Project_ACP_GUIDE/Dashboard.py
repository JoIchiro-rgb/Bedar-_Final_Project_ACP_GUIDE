from tkinter import *
from tkinter import messagebox
import pygame
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageSequence
import mysql.connector
from datetime import datetime


# Initialize the main window
window = Tk()
window.title('Dashboard')
window.geometry('925x600+300+100')

window.configure(bg='#fff')
window.resizable(False, False)


# Initialize pygame mixer for music
pygame.mixer.init()

# Global variables for timers
work_time = 25 * 60  # Default work time (25 minutes)
break_time = 5 * 60  # 5 minutes in seconds
work_timer_running = False
break_timer_running = False

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

# Function to end the page session and record the end time in the database
def end_page_session(user_id):
    """Ends the current page session by updating the end_time in the Page_Session table."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='user_db'
        )
        cursor = connection.cursor()
        
        # Check if there's an active session
        cursor.execute(
            "SELECT session_id FROM Page_Session WHERE user_id = %s AND end_time IS NULL",
            (user_id,)
        )
        session = cursor.fetchone()
        
        if session:
            # If an active session exists, update the end_time
            cursor.execute(
                "UPDATE Page_Session SET end_time = NOW() WHERE session_id = %s",
                (session[0],)
            )
            connection.commit()
            messagebox.showinfo("Session Ended", "The session has been successfully ended.")
        else:
            messagebox.showwarning("No Active Session", "No active session found for this user.")
        
        connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to clear the window for switching sections
def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

# Function to format the time as MM:SS
def format_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02}:{remaining_seconds:02}"

# Music Player Section


def show_music():
    clear_window()
    window.geometry('925x500+300+200')
    window.config(bg="#282828")  # Dark background for a modern look

    # Title with improved styling
    title_label = Label(
        window, 
        text="🎵 Music Player 🎵", 
        font=("Arial", 28, "bold"), 
        bg="#282828", 
        fg="#00FFAB"  # Vibrant green text
    )
    title_label.pack(pady=20)

    # Subtitle or description
    subtitle_label = Label(
        window, 
        text="Enjoy LoFi Beats while working or relaxing", 
        font=("Arial", 16, "italic"), 
        bg="#282828", 
        fg="#AAAAAA"
    )
    subtitle_label.pack(pady=10)

    # Button styles
    button_style = {
        "font": ("Arial", 12, "bold"),
        "width": 12,
        "height": 1,
        "relief": "raised",
        "bd": 2,
        "fg": "white",
        "cursor": "hand2"
    }

    # Music Control Functions
    def play_music():
        try:
            pygame.mixer.music.load("LoFi Beats.mp3")
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except pygame.error:
            messagebox.showerror("Error", "Music file not found or cannot be loaded.")

    def stop_music():
        pygame.mixer.music.stop()

    def mute_music():
        pygame.mixer.music.set_volume(0)

    def unmute_music():
        pygame.mixer.music.set_volume(1)

    # Confirmation when leaving the Music Player
    def confirm_leave():
        if messagebox.askyesno("Confirmation", "Are you sure you want to leave the Music Player?"):
            show_dashboard()

    # Control Buttons with Spacing and Styling
    Button(window, text="▶ Play Music", command=play_music, bg="#4CAF50", **button_style).pack(pady=5)
    Button(window, text="⏹ Stop Music", command=stop_music, bg="#F44336", **button_style).pack(pady=5)
    Button(window, text="🔇 Mute", command=mute_music, bg="#FFC107", **button_style).pack(pady=5)
    Button(window, text="🔊 Unmute", command=unmute_music, bg="#FFC107", **button_style).pack(pady=5)
    Button(window, text="⬅ Go Back", command=confirm_leave, bg="#00BFFF", **button_style).pack(pady=15)

    # Bottom Note
    footer_label = Label(
        window, 
        text="Tip: Adjust your volume to a comfortable level. 🎧", 
        font=("Arial", 12, "italic"), 
        bg="#282828", 
        fg="#AAAAAA"
    )
    footer_label.pack(side=BOTTOM, pady=10)
    
    

# To-Do List Section
def show_todo():
    global work_time, break_time, work_timer_running, break_timer_running
    clear_window()

    # Confirmation when leaving the To-Do List
    def confirm_leave():
        if messagebox.askyesno("Confirmation", "Are you sure you want to leave the To-Do List? Finish your tasks first!"):
            show_dashboard()

    # Adjust window size for the To-Do List section
    window.geometry('925x600+300+100')
        
    # Create a Label widget with the image and place it in the window
    background_label = Label(bg = '#8affb8')
    background_label.place(relwidth=1, relheight=1)  # Fill the entire window
    
    # Left Frame for To-Do List
    todo_frame = Frame(window, bg="#8affb8", width=450, height=600)
    todo_frame.pack(side=LEFT, fill=BOTH, padx=20, pady=10)

    Back = Button(todo_frame, text="Go Back", command=confirm_leave, font=("Arial", 11), bg="#F44336", fg="white")
    Back.grid(row=0, column=0, sticky='w', padx=10, pady=10)

    # Title for To-Do List
    Label(todo_frame, text="To-Do List", font=("Arial", 24, "bold"), bg="#8affb8", fg="#000").grid(row=1, column=0, pady=10, padx=10)

    # Task Entry and Buttons
    task_entry = Entry(todo_frame, width=30, font=("Arial", 14 ), bd=2, relief="solid", border = 1)
    task_entry.grid(row=2, column=0, pady=10, padx=10)

    # Function to add a task
    def add_task(entry, parent_frame):
            task = entry.get().strip()
            if task:
                # Create a frame for the task
                task_frame = Frame(parent_frame, bg="#fff")
                task_frame.pack(fill=X, pady=5, padx=5)

                var = BooleanVar()

                # Function to toggle the task completion
                def toggle_task():
                    if var.get():
                        task_label.config(fg="grey", font=("Arial", 12, "overstrike"))
                    else:
                        task_label.config(fg="black", font=("Arial", 12))

                # Add checkbox for marking tasks
                checkbox = Checkbutton(task_frame, variable=var, command=toggle_task, bg="#fff")
                checkbox.pack(side=LEFT, padx=5)

                # Task label
                task_label = Label(task_frame, text=task, font=("Arial", 12), bg="#fff", anchor="w")
                task_label.pack(side=LEFT, fill=X, expand=True, padx=5)

                # Delete button for removing the task
                delete_button = Button(task_frame, text="Delete", font=("Arial", 10), bg="#F44336", fg="white", 
                                       command=lambda: delete_task(task_frame))
                delete_button.pack(side=RIGHT, padx=5)

                # Clear the task entry after adding
                entry.delete(0, END)

                # Update the scrollbar region
                update_scrollregion()
            else:
                messagebox.showerror("Error", "Task cannot be empty.")
                
    # Function to clear all tasks and show a confirmation
    def clear_all_tasks():
        # Check if there are any tasks to clear
        if not task_canvas_frame.winfo_children():
            messagebox.showinfo("No Tasks", "There are no tasks to be cleared.")
            return  # Exit the function if there are no tasks

        # Ask for confirmation to clear all tasks
        if messagebox.askyesno("Clear All Tasks", "Are you sure you want to clear all tasks?"):
            for child in task_canvas_frame.winfo_children():
                child.destroy()  # Remove all task frames
            update_scrollregion()  # Update the scrollbar's region



    # Function to delete a task and update the scrollbar
    def delete_task(task_frame):
    # Show a confirmation message box before deleting
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            task_frame.destroy()  # Remove the task frame
        update_scrollregion()  # Update the scrollbar's region

        # Update the scrollbar's scrollable region
    def update_scrollregion():
            task_canvas_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

    # Task Entry and Buttons
    task_entry = Entry(todo_frame, width=30, font=("Arial", 14), bd=2, relief="solid")
    task_entry.grid(row=2, column=0, pady=10, padx=10)
    
    # Create a frame to hold the Add Task and Clear Tasks buttons
    button_frame = Frame(todo_frame, bg="#8affb8")
    button_frame.grid(row=3, column=0, pady=10, padx=10, sticky="w")

    # Add Task Button
    add_task_button = Button(button_frame, text="Add Task", command=lambda: add_task(task_entry, task_canvas_frame),
                            font=("Arial", 12), bg="#4CAF50", fg="white", width=12)
    add_task_button.pack(side=LEFT, padx=5)

    # Clear Tasks Button
    clear_task_button = Button(button_frame, text="Clear Tasks", command=clear_all_tasks,
                            font=("Arial", 12), bg="#F44336", fg="white", width=12)
    clear_task_button.pack(side=LEFT, padx=5)

    # Task List Frame with Scrollbar
    task_list_frame = Frame(todo_frame, bg="#fff", bd=2, relief="solid")
    task_list_frame.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")

    # Canvas for scrolling tasks
    canvas = Canvas(task_list_frame, bg="#fff")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    
    # Vertical scrollbar linked to the canvas
    scrollbar = Scrollbar(task_list_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Configure canvas with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside the canvas to hold task frames
    task_canvas_frame = Frame(canvas, bg="#fff")
    canvas.create_window((0, 0), window=task_canvas_frame, anchor="nw")

    # Adjust the scroll region when a new task is added
    task_canvas_frame.bind("<Configure>", lambda e: update_scrollregion())

    # Right Frame for Timers
    timer_frame = Frame(window, bg="#8affb8", width=450, height=600)
    timer_frame.pack(side=RIGHT, fill=BOTH, padx=20, pady=10)

    # Work Timer
    Label(timer_frame, text="Work Timer", font=("Arial", 20, "bold"), bg="#8affb8", fg="#000").pack(pady=10)
    work_timer_label = Label(timer_frame, text=format_time(work_time), font=("Arial", 40), bg="#8affb8")
    work_timer_label.pack(pady=10)

    # Break Timer
    Label(timer_frame, text="Break Timer", font=("Arial", 20, "bold"), bg="#8affb8", fg="#2196F3").pack(pady=10)
    break_timer_label = Label(timer_frame, text=format_time(break_time), font=("Arial", 40), bg="#8affb8")
    break_timer_label.pack(pady=10)

    def start_work_timer():
        global work_timer_running
        if not work_timer_running:
            work_timer_running = True
            update_timer(work_time, work_timer_label, "work")

    def start_break_timer():
        global break_timer_running
        if not break_timer_running:
            break_timer_running = True
            update_timer(break_time, break_timer_label, "break")
                
    def reset_break_timer():
        global break_time, break_timer_running
        break_timer_running = False  # Stop the break timer
        break_time = 5 * 60  # Reset the break time to 5 minutes
        break_timer_label.config(text=format_time(break_time))  # Update the label with the reset time

    def stop_timer():
        global work_timer_running, break_timer_running
        work_timer_running = False
        break_timer_running = False

    def update_timer(seconds, label, mode):
        global work_time, break_time
        if (mode == "work" and work_timer_running) or (mode == "break" and break_timer_running):
            if seconds > 0:
                label.config(text=format_time(seconds))
                window.after(1000, update_timer, seconds - 1, label, mode)
            else:
                label.config(text="Time's Up!")
                stop_timer()
                if mode == "work":
                    messagebox.showinfo("Work Timer", "Work session complete! Take a break.")
                    start_break_timer()
                elif mode == "break":
                    messagebox.showinfo("Break Timer", "Break time is over!")

    def reset_work_timer():
        global work_time
        stop_timer()
        work_time = 25 * 60
        work_timer_label.config(text=format_time(work_time))

    Button(timer_frame, text="Start Work Timer", command=start_work_timer, font=("Arial", 10), bg="#4CAF50", fg="white").pack(pady=10)
    Button(timer_frame, text="Start Break Timer", command=start_break_timer, font=("Arial", 10), bg="#2196F3", fg="white").pack(pady=10)
    Button(timer_frame, text="Stop Timer", command=stop_timer, font=("Arial", 10), bg="#F44336", fg="white").pack(pady=10)
    Button(timer_frame, text="Reset Timer", command=reset_work_timer, font=("Arial", 10), bg="#FFC107", fg="white").pack(pady=10)
    Button(timer_frame, text="Reset Break Timer", command=reset_break_timer, font=("Arial", 10), bg="#FFC107", fg="white").pack(pady=10)
    
        # Music Volume Control Section (added volume slider)
    def adjust_volume(val):
        volume = float(val) / 100  # Convert the scale value to a float between 0.0 and 1.0
        pygame.mixer.music.set_volume(volume)
    
        # Volume control slider
    volume_slider = Scale(window, from_=0, to=100, orient=HORIZONTAL, command=adjust_volume, 
                          length=300, font=("Arial", 12), bg="#8affb8", fg="#000")
    volume_slider.set(100)  # Set the default volume to 100%
    volume_slider.place(x=610, y =540)

    Label(text="Volume Slider", font=("Arial", 12, "bold"), bg="#8affb8", fg="#000").place(x = 490, y = 550)
    
#DashBoard Section

def show_dashboard():
    clear_window()
    window.geometry('925x500+300+200')

    # Create a Label widget with the image or gradient background
    background_label = Label(window, bg="#8affb8")
    background_label.place(relwidth=1, relheight=1)  # Fill the entire window
    
    # Create a beautifully styled "GUIDE" title
    title_label = Label(
        window, 
        text="GUIDE", 
        font=("Arial", 50, "bold"), 
        bg="#8affb8", 
        fg="#4CAF50",  # Vibrant green text color
        relief="flat"
    )
    title_label.place(relx=0.5, rely=0.2, anchor="center")  # Centered horizontally, near the top
    
     # Function to animate GIFs
    def animate_gif(label, gif_path):
        gif = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]
        frame_count = len(frames)

        def update_frame(frame_index):
            label.config(image=frames[frame_index])
            label.image = frames[frame_index]  # Keep a reference to prevent garbage collection
            frame_index = (frame_index + 1) % frame_count
            window.after(100, update_frame, frame_index)  # Update every 100ms (adjust for speed)

        update_frame(0)

    # Create Labels for GIFs
    left_label = Label(window, bg="#8affb8")
    left_label.place(relx=0.1, rely=0.5, anchor="center")

    right_label = Label(window, bg="#8affb8")
    right_label.place(relx=0.9, rely=0.5, anchor="center")

    # Start GIF animations
    animate_gif(left_label, "Dog Study.gif")  # Replace with the actual file path
    animate_gif(right_label, "Cat Study.gif")  # Replace with the actual file path


    # Button Styling with bg included in button_style
    button_style = {
        "font": ("Arial", 16, "bold"),
        "fg": "white",
        "relief": "flat",
        "width": 20,
        "height": 2,
        "bd": 2,
        "bg": "#4CAF50"  # Default bg
    }

    def logout():
        user_id = 1  # Replace with the actual user ID logic
        end_page_session(user_id)  # Record the session end time
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")
        window.quit()  # Close the application after logout

    # Place buttons in the center with spacing
    Button(window, text="To-Do List", command=show_todo, **button_style).place(relx=0.5, rely=0.5, anchor="center", y=-80)
    button_style["bg"] = "#FFC107"
    Button(window, text="Music Player", command=show_music, **button_style).place(relx=0.5, rely=0.5, anchor="center", y=0)
    button_style["bg"] = "#F44336"
    Button(window, text="Logout", command=logout, **button_style).place(relx=0.5, rely=0.5, anchor="center", y=80)

# Start with the dashboard
show_dashboard()

# Main loop
window.mainloop() 