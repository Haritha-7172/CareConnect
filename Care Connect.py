import tkinter.messagebox
from tkinter import messagebox
from tkinter import  *
import tkinter as tk
from tkcalendar import Calendar
from tkinter import Tk, Frame, Label, Button, BOTH
from PIL import Image, ImageTk
from PIL import Image, ImageTk
import mysql.connector as sqlcon
import random as rd
import re
from datetime import datetime
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password123"
root = None
con = sqlcon.connect(host="localhost", user="root", password="Haritha@07")
cur = con.cursor(buffered=True)

# Check if the connection is successful
if con.is_connected():
    print("Connection successful")
else:
    print("Connection unsuccessful")

# Create database and tables if they do not exist
cur.execute("CREATE DATABASE IF NOT EXISTS Hospital")
cur.execute("USE Hospital")
cur.execute("""
    CREATE TABLE IF NOT EXISTS appointment (
        idno VARCHAR(12) PRIMARY KEY,
        name CHAR(50),
        age CHAR(3),
        gender VARCHAR(20),
        phone VARCHAR(10),
        bg VARCHAR(3)
    )
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS appointment_details (
        appointment_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each appointment
        idno VARCHAR(12),                               -- Aadhaar number, which relates to the appointment table
        department VARCHAR(50),
        doctor VARCHAR(50),
        date DATE,  -- The date of the appointment
        time VARCHAR(20),
        FOREIGN KEY (idno) REFERENCES appointment(idno)  -- Foreign key to reference `appointment` table
    )
""")

# Create prescription table if it does not exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS prescription (
        prescription_id INT AUTO_INCREMENT PRIMARY KEY,
        idno VARCHAR(12),
        date_of_issue DATE,
        tablet_name VARCHAR(100),
        daily_dose VARCHAR(50),
        expiry_date DATE,
        no_of_tablets INT,
        FOREIGN KEY (idno) REFERENCES appointment(idno)
    )
""")


# Function to handle entry submission
def entry(e1, e2, e3, gender_var, e5, e6, confirmation_label, root1):
    # Retrieve input values
    p1 = e1.get()  # Aadhar number
    p2 = e2.get()  # Name
    p3 = e3.get()  # Age
    p4 = gender_var.get()  # Gender
    p5 = e5.get()  # Phone number
    p6 = e6.get()  # Blood group
    if len(p1) != 12 or not p1.isdigit():
        confirmation_label.config(text="Error: Aadhaar must be 12 digits!", fg='red')
        return
    if len(p5) != 10 or not p1.isdigit():
        confirmation_label.config(text="Error: Phone number must be 10 digits!", fg='red')
        return
    try:
        # Prepare the insert query
        query = 'INSERT INTO appointment (idno, name, age, gender, phone, bg) VALUES (%s, %s, %s, %s, %s, %s)'
        values = (p1, p2, p3, p4, p5, p6)

        # Execute the query and commit changes
        cur.execute(query, values)
        con.commit()

        # Update confirmation message
        confirmation_label.config(text="YOU HAVE BEEN REGISTERED", fg='green')
        
        # Optional: Close the registration window after a delay
        root1.after(2000, root1.destroy)  # Closes after 2 seconds
    except sqlcon.Error as err:
        confirmation_label.config(text=f"Error: {err}", fg='red')

# Function to create the registration window
def register():
    root1 = tk.Toplevel()  # Use Toplevel for a new window
    root1.title("Registration")
    
    # Set the window to full screen
    root1.attributes('-fullscreen', True)
    
    # Set the background color
    root1.configure(bg='#d8e2dc')  # Light green background

    # Main title label
    label = tk.Label(root1, text="REGISTER YOURSELF", font='Arial 40 bold', bg='#598392', fg='white')
    label.grid(row=0, column=0, columnspan=2, pady=30, padx=20)

    # Font style for labels and entries
    label_font = ('Arial', 20, 'bold')  # Font style for labels
    entry_width = 30  # Width for entry fields

    # Create a frame for better layout of input fields
    frame = tk.Frame(root1, bg='#f0f0f0')
    frame.grid(row=1, column=0, columnspan=2, pady=20, padx=20)

    # Labels and Entry widgets for registration fields using grid
    l1 = tk.Label(frame, text="AADHAR CARD NO.", bg='#f0f0f0', font=label_font)
    l1.grid(row=0, column=0, padx=10, pady=10, sticky='e')
    e1 = tk.Entry(frame, width=entry_width, font=('Arial', 18, 'bold'), highlightthickness=1, borderwidth=2)
    e1.grid(row=0, column=1, padx=10, pady=10)

    l2 = tk.Label(frame, text="NAME", bg='#f0f0f0', font=label_font)
    l2.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    e2 = tk.Entry(frame, width=entry_width, font=('Arial', 18, 'bold'), highlightthickness=1, borderwidth=2)
    e2.grid(row=1, column=1, padx=10, pady=10)

    l3 = tk.Label(frame, text="AGE", bg='#f0f0f0', font=label_font)
    l3.grid(row=2, column=0, padx=10, pady=10, sticky='e')
    e3 = tk.Entry(frame, width=entry_width, font=('Arial', 18, 'bold'), highlightthickness=1, borderwidth=2)
    e3.grid(row=2, column=1, padx=10, pady=10)

        # Gender Label
    l4 = tk.Label(frame, text="GENDER", bg='#f0f0f0', font=label_font)
    l4.grid(row=3, column=0, padx=10, pady=10, sticky='e')

    # Gender Radio Buttons
    gender_var = tk.StringVar(value="Male")  # Default value is "Male"

    # Frame to group the radio buttons for better alignment
    gender_frame = tk.Frame(frame, bg='#f0f0f0')
    gender_frame.grid(row=3, column=1, padx=10, pady=10, sticky='w')

    r1 = tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male", 
                        font=('Arial', 18), bg='#f0f0f0', padx=10, indicatoron=True)
    r1.pack(side='left', padx=10)

    r2 = tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female", 
                        font=('Arial', 18), bg='#f0f0f0', padx=10, indicatoron=True)
    r2.pack(side='left', padx=10)

    r3 = tk.Radiobutton(gender_frame, text="Other", variable=gender_var, value="Other", 
                        font=('Arial', 18), bg='#f0f0f0', padx=10, indicatoron=True)
    r3.pack(side='left', padx=10)


    l5 = tk.Label(frame, text="PHONE", bg='#f0f0f0', font=label_font)
    l5.grid(row=4, column=0, padx=10, pady=10, sticky='e')
    e5 = tk.Entry(frame, width=entry_width, font=('Arial', 18, 'bold'), highlightthickness=1, borderwidth=2)
    e5.grid(row=4, column=1, padx=10, pady=10)

    from tkinter import ttk  # Import ttk for Combobox

# Replace the blood group Entry widget
    l6 = tk.Label(frame, text="BLOOD GROUP", bg='#f0f0f0', font=label_font)
    l6.grid(row=5, column=0, padx=10, pady=10, sticky='e')

    # Dropdown for blood group
    blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    e6 = ttk.Combobox(frame, values=blood_groups, width=28, font=('Arial', 18, 'bold'))
    e6.grid(row=5, column=1, padx=10, pady=10)
    e6.set("Select")  # Set default placeholder value


    # Confirmation message label
    confirmation_label = tk.Label(root1, text="", font=('Arial', 18, 'bold'), bg='#d8e2dc', fg='green')
    confirmation_label.grid(row=3, column=0, columnspan=2, pady=10)

    # Submit button
    b1 = tk.Button(root1, text="SUBMIT", command=lambda: entry(e1, e2, e3, gender_var, e5, e6, confirmation_label, root1), 
                   font=('Arial', 18, 'bold'), width=15, bg='#4CAF50', fg='white')
    b1.grid(row=2, column=0, padx=10, pady=20)

    # Close button
    b2 = tk.Button(root1, text="CLOSE", command=root1.destroy, font=('Arial', 18, 'bold'), width=15, bg='#f44336', fg='white')
    b2.grid(row=2, column=1, padx=10, pady=20)

    # Centering buttons in the grid
    root1.grid_columnconfigure(0, weight=1)
    root1.grid_columnconfigure(1, weight=1)

    root1.resizable(False, False)
    root1.mainloop()


    
#  Message for appointment

def apo_details():
    global x2, selected_date_field, x4
    department = x2.get()  # Department input
    selected_date = selected_date_field.get()  # Selected date
    time_slot = x4.get()  # Entered time

    # Input validation
    if not department or not selected_date or not time_slot:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        department = int(department)  # Ensure department is a number
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid department input! Please enter a number.")
        return

    # Assign doctors based on department
    doctors = {
        1: [("Dr. Sharma", "Room 10"), ("Dr. Verma", "Room 11")],
        2: [("Dr. Kumar", "Room 12"), ("Dr. Khan", "Room 13")],
        3: [("Dr. Anush", "Room 14"), ("Dr. Singh", "Room 15")],
        4: [("Dr. Siddharth", "Room 16"), ("Dr.Yuv", "Room 17")],
        5: [("Dr. Virat", "Room 18"), ("Dr. Leo", "Room 19")],
        6: [("Dr. Irfan", "Room 20"), ("Dr. Srividya", "Room 21")],
        7: [("Dr. Anjali", "Room 22"), ("Dr. Eesha", "Room 23")]
        # Add other departments here...
    }

    if department not in doctors:
        messagebox.showwarning("Input Error", "Invalid department number!")
        return

    # Randomly assign a doctor
    doctor, room = rd.choice(doctors[department])

    try:
        # Insert appointment details into the database
        query = """
            INSERT INTO appointment_details (department, doctor, date, time)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (department, doctor, selected_date, time_slot))
        con.commit()

        # Retrieve the unique ordered appointment number
        cur.execute("SELECT LAST_INSERT_ID()")
        appointment_no = cur.fetchone()[0]

        # Display success message with appointment details
        messagebox.showinfo(
            "Appointment Scheduled",
            f"Appointment Scheduled Successfully!\n\n"
            f"Appointment Number: {appointment_no}\n"
            f"Doctor: {doctor}\n"
            f"Room: {room}\n"
            f"Date: {selected_date}\n"
            f"Time: {time_slot}"
        )
    except sqlcon.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def get_apoint(aadhaar_number):
    global x2, selected_date_field, x4
    
    cur.execute('SELECT * FROM appointment WHERE idno = %s', (aadhaar_number,))
    dat = cur.fetchall()
    if not dat:
        messagebox.showwarning("ERROR", "NO DATA FOUND!!")
        return

    root3 = tk.Toplevel()  # Using Toplevel for dialog behavior
    root3.title("Appointment Details")
    root3.configure(bg='#d8e2dc')
    root3.attributes('-fullscreen', True)

    label = tk.Label(root3, text="APPOINTMENT DETAILS", font='Arial 30 bold', bg='#598392', fg='white')
    label.grid(row=0, column=0, columnspan=2, pady=20)  # Moved up from previous position

    data_frame = tk.Frame(root3, bg='#d8e2dc')
    data_frame.grid(row=1, column=0, columnspan=2, pady=20)  # Moved up from previous position

    for i in dat:
        title = "Mr." if i[3].upper() == 'M' else "Mrs/Ms."
        tk.Label(data_frame, text=f'WELCOME {title} {i[1]}', font='Arial 18', bg='#d8e2dc').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(data_frame, text=f'AGE: {i[2]}', font='Arial 14', bg='#d8e2dc').grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Label(data_frame, text=f'PHONE: {i[4]}', font='Arial 14', bg='#d8e2dc').grid(row=2, column=0, padx=10, pady=5, sticky='w')
        tk.Label(data_frame, text=f'BLOOD GROUP: {i[5]}', font='Arial 14', bg='#d8e2dc').grid(row=3, column=0, padx=10, pady=5, sticky='w')

    # Moved departments section higher
    tk.Label(data_frame, text='DEPARTMENTS', font='Arial 26 bold', bg='#598392', fg='white').grid(row=4, column=0, padx=10, pady=10, sticky='w')
    departments = ["1. Orthopaedic Surgeon", "2. Physician", "3. Nephrologist", 
                   "4. Neurologist", "5. Gynaecologist","6. Cardiologist","7. ENT Specialist"]
    for index, dept in enumerate(departments):
        tk.Label(data_frame, text=dept, font='Arial 14', bg='#d8e2dc').grid(row=5 + index, column=0, padx=10, pady=5, sticky='w')

    input_frame = tk.Frame(data_frame, bg='#d8e2dc')
    input_frame.grid(row=0, column=1, padx=20, pady=10, sticky='n')

    tk.Label(input_frame, text='Enter your choice', font='Arial 16 bold', bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=10, sticky='w')
    x2 = tk.Entry(input_frame, font='Arial 14', bd=2, relief='solid', width=20)
    x2.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(input_frame, text='Choose date', font='Arial 16 bold', bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=10, sticky='w')
    selected_date_field = tk.Entry(input_frame, font='Arial 14', bd=2, relief='solid', width=20)
    selected_date_field.grid(row=1, column=1, padx=10, pady=10)
    
    # Calendar Frame (placed directly below the input field)
    calendar_frame = tk.Frame(input_frame, bg='#f0f0f0')
    today = datetime.date.today()

    # Calculate the date 6 months from today
    six_months_later = today + datetime.timedelta(days=180)  # Approx. 6 months (may vary slightly depending on the months)

    calendar = Calendar(calendar_frame, font='Arial 10', selectmode='day', year=today.year, month=today.month, day=today.day, mindate=today, maxdate=six_months_later)
    calendar.pack(padx=5, pady=5)
    calendar_frame.grid_remove()  # Initially hide the calendar

    def toggle_calendar():
        if calendar_frame.winfo_viewable():
            calendar_frame.grid_remove()
        else:
            calendar_frame.grid(row=2, column=1, padx=10, pady=10)  # Place the calendar below the Select Date input field

    def get_selected_date():
        selected_date_field.config(state='normal')  # Enable writing
        selected_date_field.delete(0, tk.END)  # Clear current content
        selected_date_field.insert(0, calendar.get_date())  # Add the selected date
        selected_date_field.config(state='readonly')  # Disable editing
        calendar_frame.grid_remove()  # Hide the calendar after selection

    tk.Button(input_frame, text='Select Date', command=toggle_calendar, font='Arial 14 bold', bg='#007ACC', fg='white').grid(row=1, column=2, padx=10, pady=10)
    tk.Button(calendar_frame, text='OK', command=get_selected_date, font='Arial 12', bg='green', fg='white').pack(pady=5)

    # Time Input Field
    tk.Label(input_frame, text='Enter time (24-hour format)', font='Arial 16 bold', bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=10, sticky='w')
    x4 = tk.Entry(input_frame, font='Arial 14', bd=2, relief='solid', width=20)
    x4.grid(row=3, column=1, padx=10, pady=10)

    button_frame = tk.Frame(root3, bg='#d8e2dc')
    button_frame.grid(row=3, column=0, columnspan=2, pady=20)  # Placed below the form input

    tk.Button(button_frame, text='Submit', command=apo_details, font='Arial 14 bold', bg='green', fg='white').pack(side='left', padx=7)
    tk.Button(button_frame, text='Close', command=root3.destroy, font='Arial 14 bold', bg='red', fg='white').pack(side='right', padx=7)

    root3.mainloop()
def submit_and_close():
    aadhaar_number = x1.get()
    root2.destroy()
    get_apoint(aadhaar_number)

def apoint():
    global x1, root2
    root2 = tk.Tk()
    root2.title("Appointment")
    root2.configure(bg='#d8e2dc')

    screen_width = root2.winfo_screenwidth()
    screen_height = root2.winfo_screenheight()
    window_width, window_height = 400, 300
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root2.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(root2, text="APPOINTMENT", font='Arial 30 bold', bg='#598392', fg='white').pack(pady=10)

    box_frame = tk.Frame(root2, bg='#ffffff', bd=2, relief='groove', padx=20, pady=20)
    box_frame.pack(padx=20, pady=10, fill='both', expand=True)

    tk.Label(box_frame, text="AADHAAR NO.", font='Arial 14 bold', bg='#ffffff').grid(row=0, column=0, padx=10, pady=10, sticky='e')
    x1 = tk.Entry(box_frame, font='Arial 14', width=14, bd=2, relief='solid')
    x1.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(box_frame, text='Submit', command=submit_and_close, font='Arial 14 bold', bg='green', fg='white', bd=2, relief='solid').grid(row=1, column=0, columnspan=2, pady=10)

    root2.resizable(False, False)
    root2.mainloop()

#  List of doctors
def lst_doc():
    root4 = Toplevel()  # Use Toplevel if this is opened from another main window
    root4.attributes("-fullscreen", True)  # Set fullscreen mode
    root4.configure(bg="#d8e2dc")  # Set background color

    # Doctor details
    l = ["Dr. Sharma", "Dr. Verma", "Dr.Kumar","Dr. Khan", "Dr. Anusha", "Dr. Singh", "Dr. Siddharth", 
         "Dr. Yuv", "Dr. Virat", "Dr.Leo", "Dr. Irfan", 
         "Dr. Srividya", "Dr. Anjali", "Dr. Eesha", "Dr. Shahid"]
    m = ["Orthopaedic surgeon", "Orthopaedic surgeon", "Nephrologist", "Nephrologist", 
         "Gynaecologist", "Gynaecologist", "Physician", "Physician", "Neurologist", 
         "Neurologist", "Cardiologist", "Cardiologist", "ENT Specialist", "ENT Specialist"]
    n = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    # Create a Frame for the content
    frame = Frame(root4, bg="#d8e2dc")
    frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

    # Configure grid columns
    frame.columnconfigure(0, weight=1, minsize=200)  # Name column
    frame.columnconfigure(1, weight=1, minsize=200)  # Department column
    frame.columnconfigure(2, weight=1, minsize=200)  # Room No column

    # Column headings with increased font size and colors
    heading_font = "Arial 20 bold"
    header_bg_color = "#598392"
    header_height = 2  # Height of header boxes (in terms of grid rows)

    # Create headers with borders
    Label(frame, text='NAME OF DOCTORS', font=heading_font, bg=header_bg_color, fg="white", 
          borderwidth=2, relief="groove", height=header_height, padx=10, pady=10).grid(row=0, column=0, padx=15, pady=10, sticky='nsew')
    Label(frame, text='DEPARTMENT', font=heading_font, bg=header_bg_color, fg="white", 
          borderwidth=2, relief="groove", height=header_height, padx=10, pady=10).grid(row=0, column=1, padx=15, pady=10, sticky='nsew')
    Label(frame, text='ROOM NO', font=heading_font, bg=header_bg_color, fg="white", 
          borderwidth=2, relief="groove", height=header_height, padx=10, pady=10).grid(row=0, column=2, padx=15, pady=10, sticky='nsew')

    # Doctor information list with increased font size
    info_font = "Arial 16"
    for i, (name, dept, room) in enumerate(zip(l, m, n), start=1):
        Label(frame, text=name, font=info_font, bg="#d8e2dc", borderwidth=2, relief="groove").grid(row=i, column=0, padx=10, pady=5, sticky='nsew')
        Label(frame, text=dept, font=info_font, bg="#d8e2dc", borderwidth=2, relief="groove").grid(row=i, column=1, padx=10, pady=5, sticky='nsew')
        Label(frame, text=room, font=info_font, bg="#d8e2dc", borderwidth=2, relief="groove").grid(row=i, column=2, padx=10, pady=5, sticky='nsew')

    # Add a "Close" button to close the window, centered below the table
    close_button = Button(root4, text="Close", command=root4.destroy, font="Arial 16", bg="red", fg="white")
    close_button.place(relx=0.5, rely=0.95, anchor='center')  # Center button below the table

    root4.resizable(False, False)
    root4.mainloop()


def ser_avail():
    root5 = Toplevel()  # Use Toplevel to create a new window
    root5.attributes("-fullscreen", True)  # Set fullscreen mode
    root5.configure(bg="#d8e2dc")  # Set background color

    # Create a Frame for the content
    frame = Frame(root5, bg="#d8e2dc")
    frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

    # Configure grid columns
    frame.columnconfigure(0, weight=1, minsize=200)  # Services column
    frame.columnconfigure(1, weight=1, minsize=200)  # Room No column

    # Title label with a box around it
    title_font = "Arial 30 bold"  # Increased font size
    title_bg_color = "#598392"  # Box background color
    title_label = Label(frame, text='SERVICES AVAILABLE', font=title_font, bg=title_bg_color, fg="white", 
                        borderwidth=2, relief="groove", width=30, height=2)  # Increased width and height
    title_label.grid(row=0, column=0, columnspan=2, padx=15, pady=10)

    # Services list
    services = ["ULTRASOUND", "X-RAY", "CT Scan", "MRI", "BLOOD COLLECTION", 
                "DIALYSIS", "ECG", "CHEMIST", "LAB"]
    
    # Room numbers
    room_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Populate the services and room numbers
    for i, service in enumerate(services):
        Label(frame, text=service, font="Arial 16", bg="#d8e2dc", borderwidth=2, relief="groove").grid(row=i + 1, column=0, padx=10, pady=5, sticky='nsew')
        Label(frame, text=room_numbers[i], font="Arial 16", bg="#d8e2dc", borderwidth=2, relief="groove").grid(row=i + 1, column=1, padx=10, pady=5, sticky='nsew')

    # Contact information label
    contact_label = Label(frame, text='To avail any of these please contact on our no.:- 7042****55', 
                          font="Arial 14", bg="#d8e2dc")
    contact_label.grid(row=len(services) + 1, column=0, columnspan=2, padx=15, pady=20)

    # Add a "Close" button to close the window, centered below the table
    close_button = Button(root5, text="Close", command=root5.destroy, font="Arial 16", bg="red", fg="white")
    close_button.place(relx=0.5, rely=0.9, anchor='center')  # Center button below the content

    root5.resizable(False, False)
    root5.mainloop()

def modify(aadhaar_no):
    global x4, x5, choice, root6, success_label
    p1 = aadhaar_no
    cur.execute('select * from appointment where idno=(%s)', (p1,))
    dat = cur.fetchall()
    a = [i for i in dat]

    if len(a) == 0:
        messagebox.showwarning("ERROR", "NO DATA FOUND!!")
    else:
        # Open the modification window in fullscreen
        root6 = tk.Toplevel(root)
        root6.title("Modify Details")
        root6.attributes('-fullscreen', True)
        root6.configure(bg='#d8e2dc')

        # Title styling to match "Modify Appointment Details"
        title_label = tk.Label(root6, text='MODIFY DETAILS', font="Arial 25 bold", bg='#598392', fg='white')
        title_label.pack(pady=20)

        # Current Details frame
        details_frame = tk.Frame(root6, bg='#ffffff', bd=2, relief='groove', padx=20, pady=20)
        details_frame.pack(padx=20, pady=10, fill='both', expand=True)

        # Display current details
        for i in dat:
            labels = {
                'NAME': i[1],
                'AGE': i[2],
                'GENDER': i[3],
                'PHONE': i[4],
                'BLOOD GROUP': i[5]
            }
            y_pos = 20
            for key, value in labels.items():
                tk.Label(details_frame, text=f'{key}:', font="Arial 14 bold", bg='#ffffff').grid(row=y_pos, column=0, padx=10, pady=5, sticky='w')
                tk.Label(details_frame, text=value, font="Arial 14", bg='#ffffff').grid(row=y_pos, column=1, padx=10, pady=5, sticky='w')
                y_pos += 1

        # Modify options
        options = ["1. NAME", "2. AGE", "3. GENDER", "4. PHONE", "5. BLOOD GROUP"]
        y_pos += 2
        for option in options:
            tk.Label(details_frame, text=option, font="Arial 14", bg='#ffffff').grid(row=y_pos, column=0, sticky='w')
            y_pos += 1

        # Choice input
        tk.Label(details_frame, text='Enter Choice:', font="Arial 14 bold", bg='#ffffff').grid(row=y_pos, column=0, pady=10, sticky='w')
        x4 = tk.Entry(details_frame, font="Arial 14", bd=2, relief='solid')
        x4.grid(row=y_pos, column=1, padx=10, pady=10)

        # New value input
        tk.Label(details_frame, text='Enter New Detail:', font="Arial 14 bold", bg='#ffffff').grid(row=y_pos + 1, column=0, pady=10, sticky='w')
        x5 = tk.Entry(details_frame, font="Arial 14", bd=2, relief='solid')
        x5.grid(row=y_pos + 1, column=1, padx=10, pady=10)

        # Success message label
        success_label = tk.Label(root6, text="", font="Arial 14", bg='#d8e2dc', fg='green')
        success_label.pack(pady=20)

        # Submit and Close buttons
        button_frame = tk.Frame(root6, bg='#d8e2dc')
        button_frame.pack(pady=10)

        tk.Button(button_frame, text='Submit', command=do_modify, font='Arial 14 bold', bg='green', fg='white').pack(side='left', padx=10)
        tk.Button(button_frame, text='Close', command=root6.destroy, font='Arial 14 bold', bg='red', fg='white').pack(side='left')

        root6.mainloop()
def do_modify():
    ad = x3.get()
    choice = x4.get()
    new = x5.get()

    # Update the database based on the choice
    field_mapping = {
        '1': 'name',
        '2': 'age',
        '3': 'gender',
        '4': 'phone',
        '5': 'bg'
    }

    if choice in field_mapping:
        cur.execute(f'UPDATE appointment SET {field_mapping[choice]} = %s WHERE idno = %s', (new, ad))
        con.commit()
        # Update the success message in the same window
        success_label.config(text="The data got modified successfully!")
    else:
        success_label.config(text="Invalid choice. Please try again.", fg='red')

def mod_sub():
    global x3,root
    root7 = tk.Toplevel(root)
    root7.title("Modification - Aadhaar Entry")
    root7.configure(bg='#d8e2dc')  # Match the background color

    # Center window on screen
    screen_width = root7.winfo_screenwidth()
    screen_height = root7.winfo_screenheight()
    window_width, window_height = 400, 300
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root7.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Title with similar styling as the appointment Aadhaar window
    tk.Label(root7, text="MODIFY DETAILS", font='Arial 30 bold', bg='#598392', fg='white').pack(pady=10)

    # Input frame styled like appointment Aadhaar entry
    box_frame = tk.Frame(root7, bg='#ffffff', bd=2, relief='groove', padx=20, pady=20)
    box_frame.pack(padx=20, pady=10, fill='both', expand=True)

    # Aadhaar input label and entry
    tk.Label(box_frame, text="AADHAAR NO.", font='Arial 14 bold', bg='#ffffff').grid(row=0, column=0, padx=10, pady=10, sticky='e')
    x3 = tk.Entry(box_frame, font='Arial 14', width=14, bd=2, relief='solid')
    x3.grid(row=0, column=1, padx=10, pady=10)

    # Submit button with lambda to close root7 and open modify function in fullscreen
    tk.Button(box_frame, text='Submit', command=lambda: submit_aadhaar(root7), font='Arial 14 bold', bg='green', fg='white', bd=2, relief='solid').grid(row=1, column=0, columnspan=2, pady=10)

    root7.resizable(False, False)
    root7.mainloop()

def submit_aadhaar(window):
    aadhaar_number = x3.get()  # Get Aadhaar number
    if aadhaar_number:  # Ensure the Aadhaar number is not empty
        modify(aadhaar_number)  # Call modify function with Aadhaar number
        window.destroy()  # Close the Aadhaar entry window
    else:
        messagebox.showwarning("Input Error", "Please enter a valid Aadhaar number.")  # Show a warning if empty

def search_data():
    global x3,root7,root
    root7 = tk.Toplevel(root)
    root7.title("Search Data")
    root7.configure(bg='#d8e2dc')  # Set background color

    # Center window on screen
    screen_width = root7.winfo_screenwidth()
    screen_height = root7.winfo_screenheight()
    window_width, window_height = 400, 300
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root7.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Title with adjusted styling
    tk.Label(root7, text="SEARCH DATA", font='Arial 30 bold', bg='#598392', fg='white').pack(pady=10)

    # Input frame
    box_frame = tk.Frame(root7, bg='#ffffff', bd=2, relief='groove', padx=20, pady=20)
    box_frame.pack(padx=20, pady=10, fill='both', expand=True)

    # Aadhaar input label and entry
    tk.Label(box_frame, text="AADHAAR NO.", font='Arial 14 bold', bg='#ffffff').grid(row=0, column=0, padx=10, pady=10, sticky='e')
    x3 = tk.Entry(box_frame, font='Arial 14', width=14, bd=2, relief='solid')
    x3.grid(row=0, column=1, padx=10, pady=10)

    # Submit button
    tk.Button(box_frame, text='Submit', command=view_data, font='Arial 14 bold', bg='green', fg='white', bd=2, relief='solid').grid(row=1, column=0, columnspan=2, pady=10)

    root7.resizable(False, False)
    root7.mainloop()

def view_data():
    global p1,root
    p1 = x3.get()
    cur.execute('SELECT * FROM appointment WHERE idno = %s', (p1,))
    
    dat = cur.fetchall()
    
    if not dat:
        tkinter.messagebox.showwarning("ERROR", "NO DATA FOUND!!")
    else:
        # Open a fullscreen window to display the details
        root_fullscreen = tk.Toplevel(root)
        root_fullscreen.title("Patient Details")
        root_fullscreen.attributes('-fullscreen', True)
        root_fullscreen.configure(bg='#d8e2dc')

        # Title label
        tk.Label(root_fullscreen, text="PATIENT DETAILS", font='Arial 30 bold', bg='#598392', fg='white').pack(pady=20)

        # Create a frame for patient details
        detail_frame = tk.Frame(root_fullscreen, bg='#d8e2dc')
        detail_frame.pack(pady=20)

        # Create labels for patient details with boxes
        details = [('NAME OF THE PATIENT', f'Mr. {dat[0][1]}' if dat[0][3].upper() == 'M' else f'Mrs/Ms. {dat[0][1]}'),
                   ('AGE', dat[0][2]),
                   ('PHONE', dat[0][4]),
                   ('BLOOD GROUP', dat[0][5])]

        for index, (heading, value) in enumerate(details):
            # Heading label
            tk.Label(detail_frame, text=heading, font='Arial 14 bold', bg='#d8e2dc').grid(row=index, column=0, padx=10, pady=5, sticky='w')
            # Value label inside a box
            value_label = tk.Label(detail_frame, text=value, font='Arial 14', bg='white', bd=2, relief='solid', width=30)
            value_label.grid(row=index, column=1, padx=10, pady=5, sticky='w')

        # Close button for the fullscreen window
        close_button = tk.Button(root_fullscreen, text='Close', command=root_fullscreen.destroy, font='Arial 14 bold', bg='red', fg='white')
        close_button.pack(pady=20)

    root7.destroy()  # Close the search window after submission

# Main window setup

def prescription_details():
    global root
    global x_aadhaar  # Global variable for Aadhaar input
    prescription_window = tk.Toplevel(root)
    prescription_window.title("Prescription Details")
    prescription_window.configure(bg='#d8e2dc')

    # Set window size (same size as Modify Details)
    window_width, window_height = 400, 300
    screen_width = prescription_window.winfo_screenwidth()
    screen_height = prescription_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    prescription_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Title with similar styling as the Modify Details Aadhaar window
    tk.Label(prescription_window, text="PRESCRIPTION DETAILS", font='Arial 23 bold', bg='#598392', fg='white').pack(pady=10)

    # Input frame styled like Modify Details Aadhaar entry
    box_frame = tk.Frame(prescription_window, bg='#ffffff', bd=2, relief='groove', padx=20, pady=20)
    box_frame.pack(padx=20, pady=10, fill='both', expand=True)

    # Aadhaar input label and entry (same as Modify Details)
    tk.Label(box_frame, text="AADHAAR NO.", font='Arial 14 bold', bg='#ffffff').grid(row=0, column=0, padx=10, pady=10, sticky='e')
    
    # Aadhaar Entry box with the same style as Modify Details
    x_aadhaar = tk.Entry(box_frame, font='Arial 14', width=14, bd=2, relief='solid')
    x_aadhaar.grid(row=0, column=1, padx=10, pady=10)

    # Label for displaying messages
    message_label = tk.Label(box_frame, text="", font='Arial 12', bg='#ffffff', fg='red')
    message_label.grid(row=2, column=0, columnspan=2, pady=10)

    # Submit button that calls the submit_aadhaar function and updates the message label
    tk.Button(prescription_window, text='Submit', command=lambda: open_prescription_window(prescription_window), font='Arial 14 bold', bg='green', fg='white').pack(pady=10)
    prescription_window.resizable(False, False)
    prescription_window.mainloop()


# Function to open the prescription details window
def open_prescription_window(aadhaar_window):
    aadhaar_number = x_aadhaar.get()
    if not aadhaar_number:
        messagebox.showwarning("Input Error", "Please enter an Aadhaar ID.")
        return

    # Fetch patient details from the database
    cur.execute('SELECT * FROM appointment WHERE idno = %s', (aadhaar_number,))
    patient_data = cur.fetchall()

    if not patient_data:
        messagebox.showwarning("Error", "No patient data found for this Aadhaar ID.")
        return

    # Close the Aadhaar window before opening the prescription details window
    aadhaar_window.destroy()

    # Create the fullscreen window for prescription
    prescription_window = tk.Tk()
    prescription_window.title("Prescription Details")
    prescription_window.attributes('-fullscreen', True)

    tk.Label(prescription_window, text="Prescription Details", font='Arial 30 bold', bg='#598392', fg='white').pack(pady=20)

    patient_frame = tk.Frame(prescription_window, bg='#d8e2dc')
    patient_frame.pack(pady=20)

    for patient in patient_data:
        title = "Mr." if patient[3].upper() == 'M' else "Mrs/Ms."
        tk.Label(patient_frame, text=f'WELCOME {title} {patient[1]}', font='Arial 18', bg='#d8e2dc').pack()

    # Input fields for prescription
    input_frame = tk.Frame(prescription_window, bg='#d8e2dc')
    input_frame.pack(pady=20)

    # Date of Issue Label and Entry aligned left and right
    tk.Label(input_frame, text='Date of Issue', font='Arial 16 bold', bg='#d8e2dc').grid(row=0, column=0, padx=10, pady=10, sticky="w")
    date_of_issue_entry = tk.Entry(input_frame, font='Arial 14', bd=2, relief='solid', width=30)
    date_of_issue_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

    # Select button to toggle calendar visibility
    def toggle_calendar(calendar_frame):
        # Toggle visibility of the calendar frame
        if calendar_frame.winfo_ismapped():
            calendar_frame.grid_forget()
        else:
            calendar_frame.grid(row=1, column=0, columnspan=2, pady=10)

    # Button to show the calendar
    select_button = tk.Button(input_frame, text="Select", font='Arial 14', bg='#7cb5e0', fg='white', command=lambda: toggle_calendar(calendar_frame))
    select_button.grid(row=0, column=2, padx=10, pady=10)

    # Calendar frame (initially hidden)
    calendar_frame = tk.Frame(input_frame, bg='#ffffff')

    cal = Calendar(calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=10)
    cal.bind('<<CalendarSelected>>', lambda event: date_of_issue_entry.insert(0, cal.get_date()) or toggle_calendar(calendar_frame))  # Insert selected date and hide calendar

    # List to hold tablet entries
    tablet_entries = []

    def add_tablet_entry():
        row = len(tablet_entries) + 1  # Start from row 1 for tablets

        # Set equal column weight to make sure everything stretches evenly
        for col in range(8):  # Adjust the number of columns if necessary
            input_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        # Label for Tablet Name
        tk.Label(input_frame, text='Tablet Name', font='Arial 16 bold', bg='#d8e2dc').grid(row=row, column=0, padx=10, pady=10, sticky='w')

        # Tablet Name Entry
        tablet_name_entry = tk.Entry(input_frame, font='Arial 12', bd=2, relief='solid', width=25)
        tablet_name_entry.grid(row=row, column=1, padx=10, pady=10, sticky='w')

        # Label for Daily Dose
        tk.Label(input_frame, text='Daily Dose', font='Arial 16 bold', bg='#d8e2dc').grid(row=row, column=2, padx=10, pady=10, sticky='w')

        # Daily Dose Entry
        daily_dose_entry = tk.Entry(input_frame, font='Arial 14', bd=2, relief='solid', width=25)
        daily_dose_entry.grid(row=row, column=3, padx=10, pady=10, sticky='w')

        # Label for Expiry Date
        tk.Label(input_frame, text='Expiry Date', font='Arial 16 bold', bg='#d8e2dc').grid(row=row, column=4, padx=10, pady=10, sticky='w')

        # Expiry Date Entry
        expiry_date_entry = tk.Entry(input_frame, font='Arial 14', bd=2, relief='solid', width=25)
        expiry_date_entry.grid(row=row, column=5, padx=10, pady=10, sticky='w')

        # Label for No of Tablets
        tk.Label(input_frame, text='No of Tablets', font='Arial 16 bold', bg='#d8e2dc').grid(row=row, column=6, padx=10, pady=10, sticky='w')

        # No of Tablets Entry
        no_of_tablets_entry = tk.Entry(input_frame, font='Arial 14', bd=2, relief='solid', width=25)
        no_of_tablets_entry.grid(row=row, column=7, padx=10, pady=10, sticky='w')

        # Add the entries to the list for saving later
        tablet_entries.append((tablet_name_entry, daily_dose_entry, expiry_date_entry, no_of_tablets_entry))

    # Button to add tablet entries
    tk.Button(prescription_window, text='Add Tablet', command=add_tablet_entry, font='Arial 14 bold', bg='blue', fg='white').pack(pady=10)

    # Save prescription button
    tk.Button(prescription_window, text='Save Prescription', command=lambda: save_prescription(aadhaar_number, date_of_issue_entry.get(), tablet_entries, prescription_window), font='Arial 14 bold', bg='green', fg='white').pack(pady=20)

    # Close button to exit the fullscreen window
    tk.Button(prescription_window, text='Close', command=prescription_window.destroy, font='Arial 14 bold', bg='red', fg='white').pack(pady=20)

    prescription_window.resizable(False, False)
    prescription_window.mainloop()

import datetime
    # Display the success message in the prescription window
def save_prescription(aadhaar_number, date_of_issue, tablet_entries, prescription_window):
    # Validate that the date_of_issue is in the correct string format (YYYY-MM-DD)
    try:
        datetime.datetime.strptime(date_of_issue, '%Y-%m-%d')
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter the Date of Issue in the correct format (YYYY-MM-DD).")
        return

    # Validate all tablet fields
    for tablet in tablet_entries:
        tablet_name, daily_dose, expiry_date, no_of_tablets = tablet

        if not (tablet_name.get() and daily_dose.get() and expiry_date.get() and no_of_tablets.get()):
            messagebox.showwarning("Input Error", "Please fill in all fields for each tablet.")
            return

        # Validate expiry date format
        try:
            # Attempt to parse the expiry date to ensure it's in the correct format
            datetime.datetime.strptime(expiry_date.get(), '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter the Expiry Date in the correct format (YYYY-MM-DD).")
            return

        # Insert prescription details into the database
        query = '''INSERT INTO prescription (idno, date_of_issue, tablet_name, daily_dose, expiry_date, no_of_tablets) 
                   VALUES (%s, %s, %s, %s, %s, %s)'''
        values = (aadhaar_number, date_of_issue, tablet_name.get(), daily_dose.get(), expiry_date.get(), no_of_tablets.get())
        
        try:
            cur.execute(query, values)
            con.commit()  # Commit the transaction

        except sqlcon.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return

    # If everything is successful, show the success message in the prescription window
    success_label = tk.Label(
        prescription_window,  # Use prescription_window for displaying the success message
        text="Prescription saved successfully!",
        font='Arial 16 bold',
        bg='#d8e2dc',
        fg='green'
    )
    success_label.pack(pady=10)
    
def view_prescription():
    global root
    global x_aadhaar  # Global variable for Aadhaar input
    view_window = tk.Toplevel(root)
    view_window.title("View Prescription")
    view_window.configure(bg='#d8e2dc')

    # Set window size (same size as Modify Details)
    window_width, window_height = 400, 300
    screen_width = view_window.winfo_screenwidth()
    screen_height = view_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    view_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Title with similar styling as the Modify Details Aadhaar window
    tk.Label(view_window, text="VIEW PRESCRIPTION", font='Arial 23 bold', bg='#598392', fg='white').pack(pady=10)

    # Input frame styled like Modify Details Aadhaar entry
    box_frame = tk.Frame(view_window, bg='#ffffff', bd=2, relief='groove', padx=20, pady=20)
    box_frame.pack(padx=20, pady=10, fill='both', expand=True)

    # Aadhaar input label and entry (same as Modify Details)
    tk.Label(box_frame, text="AADHAAR NO.", font='Arial 14 bold', bg='#ffffff').grid(row=0, column=0, padx=10, pady=10, sticky='e')
    
    # Aadhaar Entry box with the same style as Modify Details
    x_aadhaar = tk.Entry(box_frame, font='Arial 14', width=14, bd=2, relief='solid')
    x_aadhaar.grid(row=0, column=1, padx=10, pady=10)

    # Label for displaying messages
    message_label = tk.Label(box_frame, text="", font='Arial 12', bg='#ffffff', fg='red')
    message_label.grid(row=2, column=0, columnspan=2, pady=10)

    # Submit button that calls the submit_aadhaar function and updates the message label
    tk.Button(view_window, text='Submit', command=lambda: open_view_prescription_window(view_window), font='Arial 14 bold', bg='green', fg='white').pack(pady=10)

    view_window.resizable(False, False)
    view_window.mainloop()
# Function to open the prescription details window and fetch prescription data
def open_view_prescription_window(aadhaar_window):
    aadhaar_number = x_aadhaar.get()
    if not aadhaar_number:
        messagebox.showwarning("Input Error", "Please enter an Aadhaar ID.")
        return

    # Fetch prescription details from the database
    cur.execute('''SELECT tablet_name, daily_dose, expiry_date, no_of_tablets 
                   FROM prescription 
                   WHERE idno = %s
                   ORDER BY modification_date DESC LIMIT 1''', (aadhaar_number,))
    prescription_data = cur.fetchall()

    if not prescription_data:
        messagebox.showwarning("Error", "No prescription data found for this Aadhaar ID.")
        return

    # Close the Aadhaar window before opening the prescription details window
    aadhaar_window.destroy()

    # Create the fullscreen window for prescription
    prescription_window = tk.Tk()
    prescription_window.title("Prescription Details")
    prescription_window.attributes('-fullscreen', True)

    tk.Label(prescription_window, text="Prescription Details", font='Arial 30 bold', bg='#598392', fg='white').pack(pady=20)

    # Prescription display frame
    prescription_frame = tk.Frame(prescription_window, bg='#d8e2dc')
    prescription_frame.pack(pady=20)

    # Headers for the prescription details
    tk.Label(prescription_frame, text="Tablet Name", font='Arial 14 bold', bg='#d8e2dc', relief="solid", width=20, height=2).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(prescription_frame, text="Daily Dose", font='Arial 14 bold', bg='#d8e2dc', relief="solid", width=20, height=2).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(prescription_frame, text="Expiry Date", font='Arial 14 bold', bg='#d8e2dc', relief="solid", width=20, height=2).grid(row=0, column=2, padx=5, pady=5)
    tk.Label(prescription_frame, text="No of Tablets", font='Arial 14 bold', bg='#d8e2dc', relief="solid", width=20, height=2).grid(row=0, column=3, padx=5, pady=5)

    # Display the prescription details in the rows
    row = 1
    for tablet in prescription_data:
        tk.Label(prescription_frame, text=tablet[0], font='Arial 12', bg='#d8e2dc', relief="solid", width=20, height=2).grid(row=row, column=0, padx=5, pady=5)
        tk.Label(prescription_frame, text=tablet[1], font='Arial 12', bg='#d8e2dc', relief="solid", width=20, height=2).grid(row=row, column=1, padx=5, pady=5)
        tk.Label(prescription_frame, text=tablet[2], font='Arial 12', bg='#d8e2dc', relief="solid", width=20, height=2).grid(row=row, column=2, padx=5, pady=5)
        tk.Label(prescription_frame, text=tablet[3], font='Arial 12', bg='#d8e2dc', relief="solid", width=20, height=2).grid(row=row, column=3, padx=5, pady=5)
        row += 1

    # Close button to exit the fullscreen window
    tk.Button(prescription_window, text='Close', command=prescription_window.destroy, font='Arial 14 bold', bg='red', fg='white').pack(pady=20)

    prescription_window.resizable(False, False)



# Main window code
# Initialize the main window
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password123"
root = None
def show_main_window():
    global root
    # Validate username and password
    username = username_entry.get()
    password = password_entry.get()

    if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
        login_window.destroy()  # Close the login window

        root = Tk()
        root.attributes('-fullscreen', True)  # Set the window to fullscreen mode
        root.title("Care Connect")

        # Create a frame for the background color
        background_frame = Frame(root, bg='#e3f2fd')  # Light blue background
        background_frame.pack(fill=BOTH, expand=True)

        # Load the image
        image_path = "C:\\Users\\Dell\\Downloads\\Screenshot 2024-11-03 202101.png"  # Update this path if necessary
        header_image = Image.open(image_path)
        header_image = header_image.resize((800, 200), Image.LANCZOS)  # Resize if needed
        header_photo = ImageTk.PhotoImage(header_image)

        # Display the image as a label
        header_label = Label(background_frame, image=header_photo, bg='#e3f2fd')  # Set the same background color
        header_label.image = header_photo  # Keep a reference to avoid garbage collection
        header_label.pack(pady=20)

        # Create a frame for buttons with the same background color
        button_frame = Frame(background_frame, bg='#e3f2fd')  # Ensure the button frame matches the background
        button_frame.pack(pady=20, fill=BOTH, expand=True)

        # Button setup
        buttons = [
            ("Registration", register),
            ("Appointment", apoint),
            ("List of Doctors", lst_doc),
            ("Services Available", ser_avail),
            ("Modify Existing Data", mod_sub),
            ("View Data", search_data),
            ("Prescription Details", prescription_details),
            ("View Prescription", view_prescription),
            ("Exit", root.destroy)
        ]

        layout = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]

        for (i, (text, command)) in enumerate(buttons):
            row, col = layout[i]
            button = Button(
                button_frame,
                text=text,
                font="arial 22 bold",
                bg='#ffe5ec',
                fg='#000000',
                width=18,
                height=2,
                command=command,
                bd=4,
                highlightbackground='#a40182',
                highlightthickness=2
            )
            button.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

        for i in range(3):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            button_frame.grid_columnconfigure(j, weight=1)

        root.resizable(False, False)
        root.mainloop()
    else:
        # Show error message
        error_label.config(text="Invalid username or password!", fg="red")

# Create the login window
login_window = Tk()
login_window.attributes('-fullscreen', True)  # Set to fullscreen
login_window.title("Login - Care Connect")
login_window.configure(bg='#e3f2fd')  # Match the main window background

# Login frame
login_frame = Frame(login_window, bg='#e3f2fd')
login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Username label and entry
username_label = Label(login_frame, text="Username", font="arial 16", bg='#e3f2fd', fg='black')
username_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
username_entry = Entry(login_frame, font="arial 16", width=25)
username_entry.grid(row=0, column=1, pady=10, padx=10)

# Password label and entry
password_label = Label(login_frame, text="Password", font="arial 16", bg='#e3f2fd', fg='black')
password_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
password_entry = Entry(login_frame, font="arial 16", width=25, show="*")
password_entry.grid(row=1, column=1, pady=10, padx=10)

# Error message label
error_label = Label(login_frame, text="", font="arial 12", bg='#e3f2fd', fg='red')
error_label.grid(row=2, column=0, columnspan=2)

# Buttons frame
buttons_frame = Frame(login_frame, bg='#e3f2fd')
buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)

# Login button
login_button = Button(
    buttons_frame,
    text="Login",
    font="arial 16 bold",
    bg='#a40182',
    fg='white',
    command=show_main_window  # Trigger the main window
)
login_button.pack(side=LEFT, padx=10)

# Close button
close_button = Button(
    buttons_frame,
    text="Close",
    font="arial 16 bold",
    bg='red',
    fg='white',
    command=login_window.destroy  # Close the login window
)
close_button.pack(side=LEFT, padx=10)

login_window.mainloop()