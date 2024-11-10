import tkinter as tk
from tkinter import messagebox
import pymysql
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tkinter import messagebox, scrolledtext, ttk
from datetime import datetime
from dateutil.relativedelta import relativedelta

import sys
print(sys.executable)

class SmartHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home Automation System")

        # Main menu
        self.main_menu()

    def create_connection(self):
        """Create a connection to the MySQL database."""
        try:
            connection = pymysql.connect(
                host='localhost',  # Your MySQL server host
                user='newuser',  # Your MySQL username
                password='your_password',  # Your MySQL password
                database='smart_home'  # Your MySQL database name
            )
            return connection
        except pymysql.MySQLError as e:
            print(f"Error code: {e.args[0]}, Error message: {e.args[1]}")
            messagebox.showerror("Database Error", str(e))
            return None

    def main_menu(self):
        """Display the main menu."""
        self.clear_screen()
        
        tk.Label(self.root, text="Welcome to Smart Home Automation System", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Log In", command=self.login, width=20).pack(pady=10)
        tk.Button(self.root, text="Sign Up", command=self.sign_up, width=20).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20).pack(pady=10)

    def login(self):
        """User login screen."""
        self.clear_screen()
        
        tk.Label(self.root, text="Log In", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="User ID:").pack(pady=5)
        self.user_id = tk.Entry(self.root)
        self.user_id.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.user_password = tk.Entry(self.root, show='*')
        self.user_password.pack(pady=5)

        tk.Button(self.root, text="Log In", command=self.authenticate_user, width=20).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20).pack(pady=10)

    def sign_up(self):
        """User sign up screen."""
        self.clear_screen()
        
        tk.Label(self.root, text="Sign Up", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="User ID:").pack(pady=5)
        self.new_user_id = tk.Entry(self.root)
        self.new_user_id.pack(pady=5)

        tk.Label(self.root, text="Name:").pack(pady=5)
        self.new_user_name = tk.Entry(self.root)
        self.new_user_name.pack(pady=5)

        tk.Label(self.root, text="Mobile:").pack(pady=5)
        self.new_user_mobile = tk.Entry(self.root)
        self.new_user_mobile.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.new_user_password = tk.Entry(self.root, show='*')
        self.new_user_password.pack(pady=5)

        tk.Label(self.root, text="Role (user/admin):").pack(pady=5)
        self.new_user_role = tk.Entry(self.root)
        self.new_user_role.pack(pady=5)

        tk.Label(self.root, text="Date of Birth (YYYY-MM-DD):").pack(pady=5)
        self.new_user_dob = tk.Entry(self.root)
        self.new_user_dob.pack(pady=5)

        tk.Button(self.root, text="Sign Up", command=self.register_user, width=20).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, width=20).pack(pady=10)

    def authenticate_user(self):
        """Authenticate user based on ID and password."""
        user_id = self.user_id.get()
        password = self.user_password.get()

        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                # Call the SQL function to authenticate user
                cursor.execute("SELECT authenticate_user(%s, %s)", (user_id, password))
                result = cursor.fetchone()
                
                if result and result[0]:  # Check if a role is returned
                    self.user_role = result[0]  # Store the user role for later use
                    self.show_common_options()
                else:
                    messagebox.showerror("Login Error", "Invalid User ID or Password.")


    def register_user(self):
        """Register a new user in the database."""
        user_id = self.new_user_id.get()
        name = self.new_user_name.get()
        mobile = self.new_user_mobile.get()
        password = self.new_user_password.get()
        role = self.new_user_role.get()
        dob = self.new_user_dob.get()

        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                # Insert new user into the database
                try:
                    cursor.execute("INSERT INTO User (user_ID, name, mobile, password, role, dob) VALUES (%s, %s, %s, %s, %s, %s)", 
                                   (user_id, name, mobile, password, role, dob))
                    connection.commit()
                    messagebox.showinfo("Success", "User registered successfully!")
                    self.clear_screen()
                    self.main_menu()
                except pymysql.IntegrityError:
                    messagebox.showerror("Registration Error", "User ID already exists.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            connection.close()

    def show_common_options(self):
        """Display common options after login."""
        self.clear_screen()

        tk.Label(self.root, text="Home Page", font=("Arial", 16)).pack(pady=20)
        
        

        tk.Button(self.root, text="Show Device Stats", command=self.show_device_stats, width=20).pack(pady=10)

        # Show user or admin specific options
        if self.user_role == "Admin":
            self.show_admin_options()
        else:
            self.show_user_options()

    def show_admin_options(self):
        """Display admin options."""
        tk.Button(self.root, text="Manage Automation", command=self.show_automation, width=20).pack(pady=10)
        tk.Button(self.root, text="View Maintenance Logs", command=self.show_maintenance, width=20).pack(pady=10)
        tk.Button(self.root, text="View Logs", command=self.display_logs, width=20).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.main_menu, width=20).pack(pady=10)

    def show_user_options(self):
        """Display user options."""
        tk.Button(self.root, text="Logout", command=self.main_menu, width=20).pack(pady=10)
        



#--------------------------------------------------------------------
#AUTOMATION PART

    import tkinter as tk
    from tkinter import messagebox

    def show_automation(self):
        """Display current automation settings and options to create or update."""
        self.clear_screen()

        tk.Label(self.root, text="Current Automation Settings", font=("Arial", 16)).pack(pady=20)

        # Fetch and display automation settings from the database
        automation_data = self.get_automation_data()
        if automation_data:
            for automation in automation_data:
                # Display each automation setting and add a 'Delete' button next to it
                automation_label = tk.Label(self.root, text=automation['display'], font=("Arial", 12))
                automation_label.pack(pady=5)

                delete_button = tk.Button(self.root, text="Delete", command=lambda id=automation['id']: self.delete_automation(id), width=20)
                delete_button.pack(pady=5)
        else:
            tk.Label(self.root, text="No automation settings available.", font=("Arial", 12)).pack(pady=20)

        # Buttons for creating and updating automation
        tk.Button(self.root, text="Create New Automation", command=self.show_create_automation, width=20).pack(pady=10)
        tk.Button(self.root, text="Update Existing Automation", command=self.show_update_automation, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_common_options, width=20).pack(pady=10)


    def get_automation_data(self):
        """Fetch automation data from the database."""
        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT automation_ID, device_ID, user_ID, start_time, end_time FROM Automation")
                data = cursor.fetchall()
            connection.close()
            
            # Formatting the output for display
            if data:
                automation_list = []
                for d in data:
                    automation_list.append({
                        'id': d[0],
                        'display': f"Automation ID: {d[0]}, Device ID: {d[1]}, User ID: {d[2]}, Start Time: {d[3]}, End Time: {d[4]}"
                    })
                return automation_list
            else:
                return []
        
        return "Database connection error."

    def delete_automation(self, automation_id):
        """Delete the automation setting from the database."""
        connection = self.create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Delete the automation setting by ID
                    cursor.execute("DELETE FROM Automation WHERE automation_ID = %s", (automation_id,))
                    connection.commit()

                # Show success message and refresh the screen
                messagebox.showinfo("Success", f"Automation {automation_id} deleted successfully.")
                self.show_automation()  # Refresh the display
            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Failed to delete automation: {str(e)}")
            finally:
                connection.close()
        else:
            messagebox.showerror("Error", "Database connection error.")

    
    def show_create_automation(self):
        """Display the screen to create new automation settings."""
        self.clear_screen()

        tk.Label(self.root, text="Create New Automation", font=("Arial", 16)).pack(pady=20)

        # Entry for new device ID
        tk.Label(self.root, text="Device ID:", font=("Arial", 12)).pack(pady=5)
        self.new_device_id_entry = tk.Entry(self.root, width=30)
        self.new_device_id_entry.pack(pady=5)

        # Entry for new user ID
        tk.Label(self.root, text="User ID:", font=("Arial", 12)).pack(pady=5)
        self.new_user_id_entry = tk.Entry(self.root, width=30)
        self.new_user_id_entry.pack(pady=5)

        # Entry for start time
        tk.Label(self.root, text="Start Time (HH:MM:SS):", font=("Arial", 12)).pack(pady=5)
        self.start_time_entry = tk.Entry(self.root, width=30)
        self.start_time_entry.pack(pady=5)

        # Entry for end time
        tk.Label(self.root, text="End Time (HH:MM:SS):", font=("Arial", 12)).pack(pady=5)
        self.end_time_entry = tk.Entry(self.root, width=30)
        self.end_time_entry.pack(pady=5)

        # Button to create new automation
        tk.Button(self.root, text="Create Automation", command=self.create_automation, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_common_options, width=20).pack(pady=10)


    def show_update_automation(self):
        """Display the screen to update existing automation settings."""
        self.clear_screen()

        tk.Label(self.root, text="Update Existing Automation", font=("Arial", 16)).pack(pady=20)

        # Entry for automation ID (for updating existing automation)
        tk.Label(self.root, text="Automation ID (Existing):", font=("Arial", 12)).pack(pady=5)
        self.automation_id_entry = tk.Entry(self.root, width=30)
        self.automation_id_entry.pack(pady=5)

        # Entry for new device ID
        tk.Label(self.root, text="New Device ID:", font=("Arial", 12)).pack(pady=5)
        self.new_device_id_entry = tk.Entry(self.root, width=30)
        self.new_device_id_entry.pack(pady=5)

        # Entry for new user ID
        tk.Label(self.root, text="New User ID:", font=("Arial", 12)).pack(pady=5)
        self.new_user_id_entry = tk.Entry(self.root, width=30)
        self.new_user_id_entry.pack(pady=5)

        # Entry for start time
        tk.Label(self.root, text="Start Time (HH:MM:SS):", font=("Arial", 12)).pack(pady=5)
        self.start_time_entry = tk.Entry(self.root, width=30)
        self.start_time_entry.pack(pady=5)

        # Entry for end time
        tk.Label(self.root, text="End Time (HH:MM:SS):", font=("Arial", 12)).pack(pady=5)
        self.end_time_entry = tk.Entry(self.root, width=30)
        self.end_time_entry.pack(pady=5)

        # Button to update automation
        tk.Button(self.root, text="Update Automation", command=self.update_automation, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_common_options, width=20).pack(pady=10)

    def create_automation(self):
        """Create a new automation setting."""
        new_device_id = self.new_device_id_entry.get()
        new_user_id = self.new_user_id_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()

        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                try:
                    # Generate a new automation ID in the format A0__
                    new_automation_id = self.generate_new_automation_id()

                    # Insert into Automation only if device_ID and user_ID exist
                    cursor.execute("""
                        INSERT INTO Automation (automation_ID, device_ID, user_ID, start_time, end_time)
                        SELECT %s, %s, %s, %s, %s
                        WHERE EXISTS (
                            SELECT 1 FROM Device WHERE device_ID = %s
                        ) AND EXISTS (
                            SELECT 1 FROM User WHERE user_ID = %s
                        )
                    """, (new_automation_id, new_device_id, new_user_id, start_time, end_time, new_device_id, new_user_id))

                    if cursor.rowcount == 0:
                        messagebox.showerror("Error", "Either the Device ID or User ID does not exist.")
                    else:
                        connection.commit()
                        messagebox.showinfo("Success", f"New automation created with ID: {new_automation_id}")
                    
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    connection.close()


    def update_automation(self):
        """Update existing automation settings."""
        automation_id = self.automation_id_entry.get()
        new_device_id = self.new_device_id_entry.get()
        new_user_id = self.new_user_id_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()

        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                try:
                    # Updating automation settings for the specified automation_ID
                    cursor.execute(
                        "UPDATE Automation SET device_ID = %s, user_ID = %s, start_time = %s, end_time = %s WHERE automation_ID = %s",
                        (new_device_id, new_user_id, start_time, end_time, automation_id)
                    )
                    connection.commit()

                    if cursor.rowcount > 0:  # Check if any rows were updated
                        messagebox.showinfo("Success", "Automation settings updated successfully!")
                    else:
                        messagebox.showwarning("Warning", "No matching automation ID found.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            connection.close()

    def generate_new_automation_id(self):
        """Generate a new automation ID in the format A0__."""
        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT MAX(automation_ID) FROM Automation")
                last_id = cursor.fetchone()[0]
                if last_id is None:
                    return "A000"  # First ID if none exists
                else:
                    # Increment logic here; you may need to adjust based on your ID format and increment logic.
                    prefix = last_id[0:2]  # Get the prefix (A0)
                    number = int(last_id[2:]) + 1  # Increment the numeric part
                    new_id = f"{prefix}{number:02d}"  # Format as A0XX
                    return new_id

        
        
#--------------------------------------------------------------------
#MAINTENANCE PART
    def show_maintenance(self):
        """Display maintenance logs and allow insertion."""
        self.clear_screen()

        tk.Label(self.root, text="Maintenance Logs", font=("Arial", 16)).pack(pady=20)

        # Create a frame for the table
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10)

        # Treeview for displaying maintenance logs
        self.tree = ttk.Treeview(table_frame, columns=("session_ID", "device_ID", "date", "issue_reported", "next_maintenance_date"), show='headings', height=10)
        self.tree.pack(side=tk.LEFT)

        # Define column headings
        self.tree.heading("session_ID", text="Session ID")
        self.tree.heading("device_ID", text="Device ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("issue_reported", text="Issue Reported")
        self.tree.heading("next_maintenance_date", text="Next Maintenance Date")

        # Add a vertical scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        # Fetch and display maintenance logs from the database
        self.populate_maintenance_logs()

        # Input section for adding a new maintenance log
        tk.Label(self.root, text="Add Maintenance Log:", font=("Arial", 12)).pack(pady=10)

        tk.Label(self.root, text="Enter Device ID:", font=("Arial", 12)).pack(pady=5)
        self.device_id_entry = tk.Entry(self.root, font=("Arial", 12), width=40)
        self.device_id_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Issue Description:", font=("Arial", 12)).pack(pady=5)
        self.issue_entry = tk.Entry(self.root, font=("Arial", 12), width=40)
        self.issue_entry.pack(pady=5)

        tk.Button(self.root, text="Add Log", command=self.add_maintenance_log, width=20, bg='blue', fg='black').pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_common_options, width=20, bg='gray', fg='black').pack(pady=10)

    def add_maintenance_log(self):
        device_id = self.device_id_entry.get().strip()
        issue = self.issue_entry.get().strip()

        if not device_id or not issue:
            messagebox.showerror("Input Error", "Both Device ID and Issue Description must be provided.")
            return

        current_date = datetime.now().date()  # Get the current date
        new_date = current_date + relativedelta(years=1)  # Get the date 1 year from now

        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                try:
                    # Fetch the maximum session ID from the Maintenance table
                    cursor.execute("SELECT MAX(session_ID) FROM Maintenance")
                    result = cursor.fetchone()
                    max_session_id = result[0]

                    if max_session_id:
                        # Increment the last two digits
                        last_num = int(max_session_id[1:]) + 1  # Skip 'M' prefix
                        session_id = f"M{last_num:03}"  # Ensure the format is M___
                    else:
                        session_id = "M000"  # Starting point if no session exists

                    # Insert the maintenance log into the database
                    cursor.execute(
                        "INSERT INTO Maintenance (session_ID, device_ID, date, issue_reported, next_maintenance_date) VALUES (%s, %s, %s, %s, %s)",
                        (session_id, device_id, current_date, issue, new_date)
                    )
                    connection.commit()
                    messagebox.showinfo("Success", "Maintenance log added successfully!")

                    # Clear input fields
                    self.device_id_entry.delete(0, tk.END)
                    self.issue_entry.delete(0, tk.END)

                    # Refresh the log display
                    self.populate_maintenance_logs()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add maintenance log: {str(e)}")
                finally:
                    connection.close()

    def populate_maintenance_logs(self):
        """Fetch and display maintenance logs in the Treeview."""
        # Clear the current logs in the tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT session_ID, device_ID, date, issue_reported, next_maintenance_date FROM Maintenance")
                logs = cursor.fetchall()
            connection.close()

            # Insert fetched logs into the Treeview
            for log in logs:
                self.tree.insert("", tk.END, values=(log[0], log[1], log[2], log[3], log[4]))
        else:
            messagebox.showinfo("No Logs", "No maintenance logs available.")






#---------------------------------------------------------------------------
#DEVICE 
    def show_device_stats(self):
        """Display current device statistics and options to add or change device status."""
        self.clear_screen()

        tk.Label(self.root, text="Device Statistics", font=("Arial", 16)).pack(pady=20)

        # Fetch and display device statistics with toggle buttons
        device_stats = self.get_device_stats()
        print("Device Stats:", device_stats)  # Debug line

        # Create headers
        header = tk.Label(self.root, text="Device ID | Name | Status", font=("Arial", 12, 'bold'))
        header.pack(pady=5)
        
        for device_id, name, status in device_stats:
            # Ensure no None values
            device_id = device_id if device_id is not None else "Unknown ID"
            name = name if name is not None else "Unknown Name"
            status = status if status is not None else "Unknown Status"

            # Create a label for each device
            device_info = f"{device_id} | {name:<20} | {status}"
            tk.Label(self.root, text=device_info, font=("Arial", 12)).pack(pady=5)

            # Create a toggle button for each device
            toggle_text = "Deactivate" if status == "active" else "Activate"
            toggle_button = tk.Button(self.root, text=toggle_text, 
                                    command=lambda d_id=device_id, stat=status: self.toggle_device_status(d_id, stat), width=20)
            toggle_button.pack(pady=5)

        # Adding a frame for buttons to prevent layout issues
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Buttons for adding and changing device stats
        add_device_button = tk.Button(button_frame, text="Add New Device", command=self.show_add_device, width=20)
        add_device_button.pack(side=tk.LEFT, padx=5)

        back_button = tk.Button(button_frame, text="Back", command=self.show_common_options, width=20)
        back_button.pack(side=tk.LEFT, padx=5)




    def get_device_stats(self):
        """Fetch device statistics from the database."""
        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                # Updated query to include device name
                cursor.execute("SELECT device_ID, name, status FROM Device")
                stats = cursor.fetchall()
            connection.close()
            return stats  # Return the list of tuples (device_ID, name, status)
        return []

    def toggle_device_status(self, device_id, current_status):
        """Toggle the device status and update the database."""
        new_status = "active" if current_status == "inactive" else "inactive"
        
        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE Device SET status = %s WHERE device_ID = %s", (new_status, device_id))
                connection.commit()
                messagebox.showinfo("Success", f"Device {device_id} is now {new_status}.")
            connection.close()

        self.show_device_stats()
    
    def show_add_device(self):
        """Display the screen to add a new device with additional details."""
        self.clear_screen()

        tk.Label(self.root, text="Add New Device", font=("Arial", 16)).pack(pady=20)

        # Entry for device ID
        tk.Label(self.root, text="Device ID:", font=("Arial", 12)).pack(pady=5)
        self.device_id_entry = tk.Entry(self.root, width=30)
        self.device_id_entry.pack(pady=5)

        # Entry for device name
        tk.Label(self.root, text="Device Name:", font=("Arial", 12)).pack(pady=5)
        self.device_name_entry = tk.Entry(self.root, width=30)
        self.device_name_entry.pack(pady=5)

        # Entry for device model
        tk.Label(self.root, text="Device Model:", font=("Arial", 12)).pack(pady=5)
        self.device_model_entry = tk.Entry(self.root, width=30)
        self.device_model_entry.pack(pady=5)

        # Entry for device version
        tk.Label(self.root, text="Device Version:", font=("Arial", 12)).pack(pady=5)
        self.device_version_entry = tk.Entry(self.root, width=30)
        self.device_version_entry.pack(pady=5)

        # Entry for device status
        tk.Label(self.root, text="Device Status:", font=("Arial", 12)).pack(pady=5)
        self.device_status_entry = tk.Entry(self.root, width=30)
        self.device_status_entry.pack(pady=5)

        # Button to add new device
        tk.Button(self.root, text="Add Device", command=self.add_device, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_device_stats, width=20).pack(pady=10)

    def add_device(self):
        """Add a new device to the database with model, version, and name details."""
        device_id = self.device_id_entry.get()
        device_name = self.device_name_entry.get()
        device_model = self.device_model_entry.get()
        device_version = self.device_version_entry.get()
        device_status = self.device_status_entry.get()

        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                try:
                    # Insert new device into the Device table with additional details
                    cursor.execute(
                        "INSERT INTO Device (device_ID, name, model, version, status) VALUES (%s, %s, %s, %s, %s)",
                        (device_id, device_name, device_model, device_version, device_status)
                    )
                    connection.commit()
                    messagebox.showinfo("Success", f"New device added with ID: {device_id}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            connection.close()


    def change_device_stats(self):
        """Change device statistics."""
        self.clear_screen()

        tk.Label(self.root, text="Change Device Statistics", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Device ID:").pack(pady=5)
        self.device_id_entry = tk.Entry(self.root)
        self.device_id_entry.pack(pady=5)

        tk.Label(self.root, text="New Status:").pack(pady=5)
        self.new_status_entry = tk.Entry(self.root)
        self.new_status_entry.pack(pady=5)

        tk.Button(self.root, text="Update Status", command=self.update_device_status, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_device_stats, width=20).pack(pady=10)

    def update_device_status(self):
        """Update the status of a device."""
        device_id = self.device_id_entry.get()
        new_status = self.new_status_entry.get()

        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                try:
                    # Update device status for the specified device_ID
                    cursor.execute(
                        "UPDATE Device SET status = %s WHERE device_ID = %s",
                        (new_status, device_id)
                    )
                    connection.commit()
                    if cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Device status updated successfully!")
                    else:
                        messagebox.showwarning("Warning", "No matching device ID found.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            connection.close()

 

#------------------------------------------------------------------
#LOGS
    def display_logs(self):
        connection = self.create_connection()
        if connection:
            with connection.cursor() as cursor:
                try:
                    # Updated SQL query with join and aggregation
                    cursor.execute("""
                        SELECT 
                            l.log_id, 
                            d.device_id, 
                            l.date, 
                            l.time, 
                            SUM(l.duration) AS total_duration
                        FROM 
                            Logs l
                        JOIN 
                            Device d ON l.device_id = d.device_ID
                        GROUP BY 
                            l.log_id, d.device_id, l.date, l.time
                    """)
                    logs = cursor.fetchall()

                    # Create a new window to display logs
                    log_window = tk.Tk()
                    log_window.title("Logs")

                    # Create a Text widget to display the log information
                    text_display = tk.Text(log_window, wrap=tk.NONE)
                    text_display.insert(tk.END, "Log ID | Device ID | Date | Time | Duration (days:hrs:mins:secs)\n")
                    text_display.insert(tk.END, "-" * 70 + "\n")

                    def convert_minutes_to_dhms(minutes):
                        days = minutes // 1440
                        hours = (minutes % 1440) // 60
                        mins = minutes % 60
                        seconds = 0  # Assuming no seconds if only minutes are stored
                        return f"{days}:{hours:02}:{mins:02}:{seconds:02}"

                    for log in logs:
                        log_id, device_id, date, time, total_duration = log
                        duration_dhms = convert_minutes_to_dhms(total_duration)
                        log_line = f"{log_id} | {device_id} | {date} | {time} | {duration_dhms}\n"
                        text_display.insert(tk.END, log_line)

                    # Disable editing in the Text widget
                    text_display.config(state=tk.DISABLED)
                    text_display.pack(fill=tk.BOTH, expand=True)

                    log_window.mainloop()

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to retrieve logs: {str(e)}")
                finally:
                    connection.close()



#CREATE AUTOMATION- NESTED QUERY
#DISPLAY LOGS- JOIN AND AGGREGATE


#---------------------------------------------------------------------------------------------------------
    def clear_screen(self):
        """Clear the main window."""
        for widget in self.root.winfo_children():
            widget.destroy()




if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)
    root.mainloop()
