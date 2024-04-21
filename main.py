import mysql.connector
from tkinter import Tk, Label, Entry, Button, messagebox, Frame, LEFT, Scrollbar, Canvas, Y, RIGHT, BOTTOM

# Establish database connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="h_m"
)
cursor = connection.cursor()


def create_record(table_name):
    # Function to create a new record
    # Retrieve data from user input
    data = [entry.get() for entry in entry_fields[table_name]]

    # SQL query to insert data into the table
    query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(data))})"

    try:
        cursor.execute(query, tuple(data))
        connection.commit()
        messagebox.showinfo("Success", f"{table_name} record created successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def retrieve_record(table_name):
    # Function to retrieve a record
    # Retrieve primary key value from user input
    pk_value = entry_fields[table_name][0].get()

    # SQL query to retrieve record data from the table
    query = f"SELECT * FROM {table_name} WHERE {table_name}ID = %s"
    values = (pk_value,)

    try:
        cursor.execute(query, values)
        record = cursor.fetchone()

        if record:
            # Display retrieved record data
            record_data = '\n'.join([f"{field}: {value}" for field, value in zip(field_names[table_name], record)])
            messagebox.showinfo(f"{table_name} Data", record_data)
        else:
            messagebox.showinfo("Info", f"{table_name} not found")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_record(table_name):
    # Function to update a record
    # Retrieve data from user input
    data = [entry.get() for entry in entry_fields[table_name]]
    pk_value = data[0]  # Primary key value

    # Generate SET clause for SQL query
    set_clause = ', '.join([f"{field} = %s" for field in field_names[table_name][1:]])

    # SQL query to update record in the table
    query = f"UPDATE {table_name} SET {set_clause} WHERE {table_name}ID = %s"
    values = tuple(data[1:]) + (pk_value,)

    try:
        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Success", f"{table_name} record updated successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete_record(table_name):
    # Function to delete a record
    # Retrieve primary key value from user input
    pk_value = entry_fields[table_name][0].get()

    # SQL query to delete record from the table
    query = f"DELETE FROM {table_name} WHERE {table_name}ID = %s"
    values = (pk_value,)

    try:
        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Success", f"{table_name} record deleted successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Define table names, field names, and labels
tables = ["Patient", "Doctor", "MedicalRecord", "Nurse", "Appointment"]
field_names = {
    "Patient": ["Patient ID", "First Name", "Last Name", "Date of Birth", "Gender", "Contact Number", "Address", "Room Number", "Department ID"],
    "Doctor": ["Doctor ID", "First Name", "Last Name", "Department ID", "Specialisation", "Contact Number", "Emergency Number"],
    "MedicalRecord": ["Record ID", "Patient ID", "Doctor ID", "Date", "Diagnosis"],
    "Nurse": ["Nurse ID", "First Name", "Last Name", "Department ID", "Contact Number"],
    "Appointment": ["Appointment ID", "Patient ID", "Doctor ID", "Appointment Date", "Status"]
}
labels = {
    table: [f"{field}: " for field in field_names[table]] for table in tables
}

# Create GUI
root = Tk()
root.title("Hospital Management System")

# Create a Canvas widget
canvas = Canvas(root)
canvas.pack(side=LEFT, fill="both", expand=True)

# Add a Scrollbar widget
scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# Configure the Canvas to scroll along the Y-axis
canvas.configure(yscrollcommand=scrollbar.set)


def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


canvas.bind('<Configure>', on_canvas_configure)

# Create a frame to hold the widgets
frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='nw')

# Create labels and entry fields for each table
entry_fields = {}
for table in tables:
    Label(frame, text=table).pack()
    entry_fields[table] = []
    for field, label_text in zip(field_names[table], labels[table]):
        entry_frame = Frame(frame)
        entry_frame.pack()
        Label(entry_frame, text=label_text).pack(side=LEFT)
        entry_field = Entry(entry_frame)
        entry_field.pack(side=LEFT)
        entry_fields[table].append(entry_field)

    # Create buttons for CRUD operations
    Button(frame, text=f"Create {table}", command=lambda t=table: create_record(t)).pack()
    Button(frame, text=f"Retrieve {table}", command=lambda t=table: retrieve_record(t)).pack()
    Button(frame, text=f"Update {table}", command=lambda t=table: update_record(t)).pack()
    Button(frame, text=f"Delete {table}", command=lambda t=table: delete_record(t)).pack()

root.mainloop()
