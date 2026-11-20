# Smart Calendar Project

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import calendar
import sqlite3
from datetime import datetime

# Database Storage

conn = sqlite3.connect("smart_calendar.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        date TEXT PRIMARY KEY,
        event_name TEXT NOT NULL,
        reminder_time TEXT DEFAULT '',
        reminded INTEGER DEFAULT 0
    )
""")
conn.commit()

months = [
    "January","February","March","April","May","June","July","August","September",
    "October","November","December"
]

# Get Event From Database
def get_event(date_key):
    cursor.execute(
        "SELECT event_name, reminder_time, reminded FROM events WHERE date = ?",
        (date_key,)
    )
    return cursor.fetchone()

# Show Complete Year Calendar
def Calendar_see():
    global get_year

    try:
        get_year = int(year_entry.get())

        if get_year < 1 or get_year > 9999:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid year."
        )
        return

    # Another window for complete year
    window = Toplevel(root)
    window.config(background="light green")
    window.title("Complete Year Calendar")
    window.geometry("650x650")

    window_content = calendar.calendar(get_year)

    year_cal = Label(
        window,
        text=window_content,
        font=("Courier New", 10, "bold"),
        bg="light green",
        justify=LEFT
    )
    year_cal.pack(
        padx=10,
        pady=10
    )

# Show Specific Month
def month_see():
    global get_year

    # First check year
    try:
        get_year = int(year_entry.get())

        if get_year < 1 or get_year > 9999:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid year first."
        )
        return

    # Get selected month
    month_name = box.get()

    if month_name == "":
        messagebox.showerror(
            "Error",
            "Please select a month."
        )
        return

    specific_month = months.index(month_name) + 1

    # Another window for specific month
    window2 = Toplevel(root)
    window2.config(background="light green")
    window2.title("Monthly Calendar")
    window2.geometry("650x500")

    # Month heading
    heading = Label(
        window2,
        text=f"{month_name} {get_year}",
        font=("Arial", 20, "bold"),
        bg="light green"
    )
    heading.pack(
        pady=15
    )

    # Frame for calendar
    calendar_frame = Frame(
        window2,
        bg="light green"
    )
    calendar_frame.pack(
        padx=10,
        pady=10
    )

    # Weekday names
    weekdays = [
        "Mon","Tue","Wed","Thu","Fri","Sat","Sun"
    ]

    for column, day_name in enumerate(weekdays):
        Label(
            calendar_frame,
            text=day_name,
            font=("Arial", 12, "bold"),
            bg="light green",
            width=8
        ).grid(
            row=0,
            column=column,
            padx=2,
            pady=5
        )

    # Get weeks of selected month
    month_data = calendar.monthcalendar(get_year,specific_month)

    # Create buttons for dates
    for row, week in enumerate(month_data, start=1):
        for column, day in enumerate(week):
            # Empty place
            if day == 0:
                Label(
                    calendar_frame,
                    text="",
                    width=8,
                    height=2,
                    bg="light green"
                ).grid(
                    row=row,
                    column=column,
                    padx=2,
                    pady=2
                )
            else:
                # Date format
                date_key = (
                    f"{day:02d}-"
                    f"{specific_month:02d}-"
                    f"{get_year}"
                )

                # Check whether event exists in database
                if get_event(date_key):
                    # Highlight event date
                    day_button = Button(
                        calendar_frame,
                        text=f"{day}\n*",
                        width=8,
                        height=2,
                        bg="yellow",
                        fg="black",
                        font=("Arial", 11, "bold"),
                        command=lambda d=day:
                        show_date_event(d,specific_month,get_year)
                    )
                else:
                    day_button = Button(
                        calendar_frame,
                        text=str(day),
                        width=8,
                        height=2,
                        font=("Arial", 11),
                        command=lambda d=day:
                        show_date_event(d,specific_month,get_year)
                    )

                day_button.grid(
                    row=row,
                    column=column,
                    padx=2,
                    pady=2
                )

# Add Event
def add_event():
    # New window
    event_window = Toplevel(root)
    event_window.title("Add Event")
    event_window.geometry("400x420")
    event_window.config(bg="light green")

    # Heading
    Label(
        event_window,
        text="Add Event",
        font=("Arial", 22, "bold"),
        bg="light green"
    ).pack(pady=15)

    # Date label
    Label(
        event_window,
        text="Enter Date",
        font=("Arial", 13, "bold"),
        bg="light green"
    ).pack(pady=5)

    # Date entry
    date_entry = Entry(
        event_window,
        font=("Arial", 13),
        width=25
    )
    date_entry.pack(pady=5)

    # Date format information
    Label(
        event_window,
        text="Format: DD-MM-YYYY",
        font=("Arial", 10),
        bg="light green"
    ).pack(pady=2)

    # Event name label
    Label(
        event_window,
        text="Enter Event Name",
        font=("Arial", 13, "bold"),
        bg="light green"
    ).pack(pady=5)

    # Event entry
    event_entry = Entry(
        event_window,
        font=("Arial", 13),
        width=25
    )
    event_entry.pack(pady=5)

    # Reminder time label
    Label(
        event_window,
        text="Reminder Time (Optional)",
        font=("Arial", 12, "bold"),
        bg="light green"
    ).pack(pady=5)

    # Reminder time entry
    time_entry = Entry(
        event_window,
        font=("Arial", 13),
        width=25
    )
    time_entry.pack(pady=5)

    Label(
        event_window,
        text="Format: HH:MM (24-hour, e.g. 09:30)",
        font=("Arial", 9),
        bg="light green"
    ).pack(pady=2)

    
    
    # Save function
    def save_event():
        date = date_entry.get().strip()
        event_name = event_entry.get().strip()
        reminder_time = time_entry.get().strip()

        # Empty field checking
        if date == "" or event_name == "":
            messagebox.showerror(
                "Error",
                "Please enter both date and event name.",
                parent=event_window
            )
            return

        # Check date format
        try:
            entered_date = datetime.strptime(date,"%d-%m-%Y")
            date_key = entered_date.strftime("%d-%m-%Y")
        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid date!\nUse DD-MM-YYYY format.",
                parent=event_window
            )
            return

        # Check reminder time format
        if reminder_time != "":
            try:
                datetime.strptime(reminder_time,"%H:%M")
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Invalid reminder time!\nUse HH:MM format, e.g. 09:30.",
                    parent=event_window
                )
                return

        # Check if event already exists
        existing_event = get_event(date_key)

        if existing_event:
            result = messagebox.askyesno(
                "Event Already Exists",
                "An event already exists on this date.\n"
                "Do you want to replace it?",
                parent=event_window
            )
            if not result:
                return

        # Store event in database
        cursor.execute("""
            INSERT OR REPLACE INTO events
            (date, event_name, reminder_time, reminded)
            VALUES (?, ?, ?, 0)
        """, (date_key, event_name, reminder_time))
        conn.commit()

        messagebox.showinfo(
            "Success",
            "Event added successfully!",
            parent=event_window
        )
        # Close window
        event_window.destroy()


    button_add_event=Button(
    event_window,
    text="Add Events",
    fg="white",
    bg="purple",
    font=("Arial", 15, "bold"),
    command=save_event
        ).pack(pady=5)



# Edit Event

def edit_event():
    edit_window = Toplevel(root)
    edit_window.config(bg="light green")
    edit_window.title("Edit Event")
    edit_window.geometry("450x400")

    conn = sqlite3.connect("smart_calendar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, event_name, reminder_time FROM events")
    events = cursor.fetchall()
    conn.close()

    if not events:
        messagebox.showinfo("No Events", "No events available to edit.")
        edit_window.destroy()
        return

    Label(edit_window, text="Select Event",font=("Arial",15,"bold"),fg="black",bg="light green").pack(pady=10)

    event_list = ttk.Combobox(edit_window, state="readonly", width=40)
    event_list["values"] = [
        f"{event[0]} - {event[1]}" for event in events
    ]
    event_list.pack(pady=5)
    event_list.current(0)

    Label(edit_window, text="New Date (DD-MM-YYYY)").pack(pady=5)
    date_entry = Entry(edit_window)
    date_entry.pack(pady=5)

    Label(edit_window, text="New Event Name").pack(pady=5)
    name_entry = Entry(edit_window)
    name_entry.pack(pady=5)

    Label(edit_window, text="Reminder Time (HH:MM, optional)").pack(pady=5)
    reminder_entry = Entry(edit_window)
    reminder_entry.pack(pady=5)

    def load_event(event=None):
        index = event_list.current()
        if index >= 0:
            selected_event = events[index]
            date_entry.delete(0, END)
            date_entry.insert(0, selected_event[0])
            name_entry.delete(0, END)
            name_entry.insert(0, selected_event[1])
            reminder_entry.delete(0, END)
            reminder_entry.insert(0, selected_event[2] or "")

    event_list.bind("<<ComboboxSelected>>", load_event)
    load_event()

    def save_changes():
        index = event_list.current()
        if index < 0:
            messagebox.showerror("Error", "Please select an event.")
            return

        old_date = events[index][0]
        new_date = date_entry.get().strip()
        new_name = name_entry.get().strip()
        reminder_time = reminder_entry.get().strip()

        try:
            datetime.strptime(new_date, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Invalid Date", "Enter date in DD-MM-YYYY format.")
            return

        if not new_name:
            messagebox.showerror("Error", "Event name cannot be empty.")
            return

        if reminder_time:
            try:
                datetime.strptime(reminder_time, "%H:%M")
            except ValueError:
                messagebox.showerror("Invalid Time", "Enter time in HH:MM format.")
                return

        conn = sqlite3.connect("smart_calendar.db")
        cursor = conn.cursor()

        if new_date != old_date:
            cursor.execute("SELECT date FROM events WHERE date=?", (new_date,))
            if cursor.fetchone():
                conn.close()
                messagebox.showerror(
                    "Date Already Exists",
                    "An event already exists on this date."
                )
                return

        cursor.execute(
            """UPDATE events
               SET date=?, event_name=?, reminder_time=?, reminded=0
               WHERE date=?""",
            (new_date, new_name, reminder_time, old_date)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Event updated successfully!")
        edit_window.destroy()

    Button(
        edit_window,
        text="Save Changes",
        font=("Arial",15,"bold"),
        fg="white",
        bg="green",
        command=save_changes
    ).pack(pady=15)

# View All Events
def view_events():
    # New window
    event_window = Toplevel(root)
    event_window.title("View Events")
    event_window.geometry("500x450")
    event_window.config(bg="light green")

    # Heading
    Label(
        event_window,
        text="All Events",
        font=("Arial", 22, "bold"),
        bg="light green"
    ).pack(pady=20)

    # Get events from database
    cursor.execute(
        "SELECT date, event_name, reminder_time FROM events"
    )
    all_events = cursor.fetchall()

    # No events
    if len(all_events) == 0:
        Label(
            event_window,
            text="No events added yet.",
            font=("Arial", 14),
            bg="light green"
        ).pack(pady=30)
        return

    # Frame for events
    event_frame = Frame(
        event_window,
        bg="white",
        bd=3,
        relief=RIDGE
    )
    event_frame.pack(
        padx=20,
        pady=10,
        fill="both",
        expand=True
    )

    # Sort events by date
    sorted_events = sorted(
        all_events,
        key=lambda x: datetime.strptime(x[0],"%d-%m-%Y")
    )

    # Display events
    for date, event_name, reminder_time in sorted_events:
        if reminder_time:
            reminder_text = f" | Reminder: {reminder_time}"
        else:
            reminder_text = " | No reminder"

        Label(
            event_frame,
            text=f"# {date}  -->  {event_name}{reminder_text}",
            font=("Arial", 10, "bold"),
            bg="white",
            anchor="w",
            wraplength=440,
            justify=LEFT
        ).pack(fill="x",padx=10,pady=8)

# Remove Event
def remove_event():
    # Check if events exist
    cursor.execute("SELECT date, event_name FROM events")
    all_events = cursor.fetchall()

    if len(all_events) == 0:
        messagebox.showinfo(
            "Remove Event",
            "There are no events to remove."
        )
        return

    # New window
    remove_window = Toplevel(root)
    remove_window.title("Remove Event")
    remove_window.geometry("450x300")
    remove_window.config(bg="light green")

    # Heading
    Label(
        remove_window,
        text="Remove Event",
        font=("Arial", 22, "bold"),
        bg="light green"
    ).pack(pady=20)

    # Label
    Label(
        remove_window,
        text="Select Event",
        font=("Arial", 13, "bold"),
        bg="light green"
    ).pack(pady=5)

    # Create list for combobox
    event_list = []
    for date, event_name in all_events:
        event_list.append(f"{date} - {event_name}")

    event_box = ttk.Combobox(
        remove_window,
        values=event_list,
        state="readonly",
        font=("Arial", 11),
        width=35
    )
    event_box.pack(pady=15)

    # Select first event
    event_box.current(0)

    # Delete function
    def delete_event():
        selected_event = event_box.get()

        if selected_event == "":
            messagebox.showerror(
                "Error",
                "Please select an event.",
                parent=remove_window
            )
            return

        # Get date from selected event
        date = selected_event.split(" - ",1)[0]

        # Confirmation
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Do you want to remove the event on {date}?",
            parent=remove_window
        )

        if result:
            # Delete event from database
            cursor.execute(
                "DELETE FROM events WHERE date = ?",
                (date,)
            )
            conn.commit()

            messagebox.showinfo(
                "Success",
                "Event removed successfully!",
                parent=remove_window
            )
            remove_window.destroy()

    # Remove button
    Button(
        remove_window,
        text="Remove Event",
        font=("Arial", 13, "bold"),
        bg="red",
        fg="white",
        width=15,
        command=delete_event
    ).pack(pady=20)

# Show Event When Date Is Clicked
def show_date_event(day, month, year):
    date_key = (
        f"{day:02d}-"
        f"{month:02d}-"
        f"{year}"
    )

    event = get_event(date_key)

    if event:
        event_name, reminder_time, reminded = event

        if reminder_time:
            reminder_text = reminder_time
        else:
            reminder_text = "Not set"

        messagebox.showinfo(
            "Event Details",
            f"Date: {date_key}\n\n"
            f"Event: {event_name}\n"
            f"Reminder: {reminder_text}"
        )
    else:
        messagebox.showinfo(
            "Event Details",
            f"No event on {date_key}."
        )

# Automatic Event Reminder
def check_reminders():
    now = datetime.now()

    cursor.execute("""
        SELECT date, event_name, reminder_time
        FROM events
        WHERE reminder_time != ''
        AND reminded = 0
    """)
    pending_events = cursor.fetchall()

    for date, event_name, reminder_time in pending_events:
        try:
            reminder_datetime = datetime.strptime(
                f"{date} {reminder_time}",
                "%d-%m-%Y %H:%M"
            )
        except ValueError:
            continue

        # Show reminder when scheduled time arrives
        if reminder_datetime <= now:
            # Mark as shown before displaying popup
            cursor.execute(
                "UPDATE events SET reminded = 1 WHERE date = ?",
                (date,)
            )
            conn.commit()

            messagebox.showinfo(
                "Event Reminder",
                f"Reminder!\n\n"
                f"Event: {event_name}\n"
                f"Date: {date}\n"
                f"Time: {reminder_time}",
                parent=root
            )

    # Check again after 1 second
    root.after(1000,check_reminders)

# Main Window
root = Tk()
root.config(background="white")
root.title("Smart GUI Calendar")
root.geometry("1000x1000")

# Title
name = Label(
    root,
    text="Smart Calendar",
    font=("calibri", 20, "bold")
)
name.pack(
    pady=10
)

Label(
    root,
    text="Today",
    font=("calibri", 15, "bold")
).pack(pady=5)

# Current Date And Time
datetime_label = Label(
    root,
    font=("calibri", 12, "bold")
)

# Function to update time
def update_time():
    now = datetime.now()
    date = now.strftime("%A, %d %B %Y")
    time = now.strftime("%I:%M:%S %p")
    datetime_label.config(text=date + "\n" + time)
    root.after(1000,update_time)

datetime_label.pack(
    padx=5,
    pady=5
)
update_time()

# Frame Creation
frame = Frame(
    root,
    bg="light green",
    bd=30,
    relief=RIDGE
)
frame.pack(padx=40,pady=20)

# Year
year = Label(
    frame,
    text="Enter the Year",
    bg="light green",
    font=("Arial", 15, "bold")
)
year.pack()

year_entry = Entry(
    frame,
    font=("Arial", 15)
)
year_entry.pack(pady=5)



# Show Year Button
show_button = Button(
    frame,
    text="Show Year",
    fg="white",
    bg="green",
    font=("Arial", 15, "bold"),
    command=Calendar_see
)
show_button.pack(pady=15)

# Month Table
month_label = Label(
    frame,
    text="Select Month",
    bg="light green",
    font=("Arial", 15, "bold")
)
month_label.pack()

# Month Dropdown
box = ttk.Combobox(
    frame,
    values=months,
    font=("calibri", 15),
    state="readonly"
)
box.pack(pady=10)

# Show Month Button
month_button = Button(
    frame,
    text="Show Month",
    fg="white",
    bg="green",
    font=("Arial", 15, "bold"),
    command=month_see
)
month_button.pack(pady=10)

frame_button1 = Frame(
    frame,
    bg="#b47df0",
    bd=5,
    
)
frame_button1.pack(padx=40,pady=50)

# Add Event Button
add_event_button = Button(
    frame_button1,
    text="Add Event",
    fg="white",
    bg="blue",
    font=("Arial", 15, "bold"),
    command=add_event
)
add_event_button.pack(side="left",pady=5,padx=5)

#Edit Event Button

edit_event=Button(
    frame_button1,
    text="Edit Event",
    fg="orange",
    bg="white",
    font=("Arial",15,"bold"),
    command=edit_event
    )
edit_event.pack(side="left",pady=5,padx=5)


# View Event Button
view_event_button = Button(
    frame_button1,
    text="View Events",
    fg="white",
    bg="purple",
    font=("Arial", 15, "bold"),
    command=view_events
)
view_event_button.pack(side="left",padx=5,pady=10)

# Remove Event Button
remove_event_button = Button(
    frame_button1,
    text="Remove Event",
    fg="white",
    bg="orange",
    font=("Arial", 15, "bold"),
    command=remove_event
)
remove_event_button.pack(side="left",pady=5,padx=5)


frame_button2 = Frame(
    frame,
    bg="light green",
    bd=5,
    
)
frame_button2.pack(padx=5,pady=5)


# Exit Button
def exit_calendar():
    conn.close()
    root.destroy()

exit_button = Button(
    frame_button2,
    text="Exit",
    fg="black",
    bg="red",
    font=("Arial", 18, "bold"),
    command=exit_calendar
)
exit_button.pack(side="bottom",pady=5)

# Start reminder checking
check_reminders()

root.mainloop()

print("Done")
