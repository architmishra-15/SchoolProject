import random
from getpass import getpass
from hashlib import sha256

import mysql.connector

# ----------------------------------------------------------------------------------------------------------------

# NOTE:
#    If the program is stuck after entering email,
#    try running it in cmd instead of IDE since most of the IDEs don't support getpass.
#
#   If you want to just check the code, you can temporarily replace getpass with input.
# ----------------------------------------------------------------------------------------------------------------

# Establish a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS ProjectTrainBookingSystem")
cursor.execute("USE ProjectTrainBookingSystem")

# Create the table with the required fields if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Data (
    Name VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Password CHAR(64),
    Age INT,
    Gender ENUM('Male', 'Female', 'Transgender'),
    Mobile_Number VARCHAR(20),
    Train_Name VARCHAR(255),
    Departure VARCHAR(255),
    Destination VARCHAR(255),
    PNR_Number BIGINT,
    Status VARCHAR(20)
)
""")


# Function to register a new user
def register_user():
    name = input("Enter your full name: ")
    email = input("Enter your email: ")
    password = getpass("Enter your password: ")
    age = input("Enter your age: ")
    gender = input("Enter your gender (Male/Female/Transgender): ")
    mobile_number = input("Enter your mobile number: ")

    # Hash the password using SHA-256
    hashed_password = sha256(password.encode('utf-8')).hexdigest()

    try:
        query = "INSERT INTO Data (Name, Email, Password, Age, Gender, Mobile_Number) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, hashed_password, age, gender, mobile_number))
        db.commit()
        print("Registration successful! Please go back and login.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def login_user():
    email = input("Enter your email: ")
    password = getpass("Enter your password: \n")

    # Hash the password using SHA-256
    hashed_password = sha256(password.encode('utf-8')).hexdigest()

    try:
        query = "SELECT Name, Email, Age, Gender, Mobile_Number FROM Data WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, hashed_password))
        result = cursor.fetchone()
        if result:
            name, email, age, gender, mobile_number = result
            print(f"\n Welcome {name}! Here are your details:\n")
            # Print the details in a tabular format
            print(f"{'Name':<15}{'Email':<15}{'Age':<15}{'Gender':<15}{'Mobile Number':<15}")
            print(f"{name:<15}{email:<15}{age:<15}{gender:<15}{mobile_number:<15}\n")
        else:
            print("Login failed. Incorrect email or password.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Function to log in an existing user and book a train ticket
def login_and_book():
    email = input("Enter your email: ")
    password = getpass("Enter your password: ")

    # Hash the password using SHA-256
    hashed_password = sha256(password.encode('utf-8')).hexdigest()

    try:
        query = "SELECT Name FROM Data WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, hashed_password))
        result = cursor.fetchone()
        if result:
            print("Login successful. Please choose a train to book:\n")
            for number, name in trains.items():
                print(f"{number}. {name}")
            train_choice = input("Enter the number of the train you want to book: ")
            train_name = trains.get(train_choice)
            departure = input("Enter your departure location: ")
            destination = input("Enter your destination location: ")
            pnr_number = random.randint(1000000000, 9999999999)
            status = "CONFIRMED"

            update_query = ("UPDATE Data SET Train_Name = %s, Departure = %s, Destination = %s, PNR_Number = %s, "
                            "Status = %s WHERE Email = %s")
            cursor.execute(update_query, (train_name, departure, destination, pnr_number, status, email))
            db.commit()
            print(f"Ticket booking successful. Your PNR is: {pnr_number}")
        else:
            print("\nLogin failed. Incorrect email or password.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Function to check the status of a booked train
def check_status():
    email = input("Enter your email: ")
    pnr_number = input("Enter your PNR number: ")

    try:
        query = "SELECT Train_Name, Departure, Destination, Status FROM Data WHERE Email = %s AND PNR_Number = %s"
        cursor.execute(query, (email, pnr_number))
        result = cursor.fetchone()
        if result:
            train_name, departure, destination, status = result
            print("\nHere are the details of your booked train:\n")
            print(f"{'Train Name':<20}{'Departure':<20}{'Destination':<20}{'PNR Number':<20}{'Status':<20}")
            print(f"{train_name:<20}{departure:<20}{destination:<20}{pnr_number:<20}{status:<20}\n")
        else:
            print("\nNo registered train found for the provided details.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Main menu
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Ticket Booking")
        print("2. Check Status")
        print("3. Other")
        choice = input("Please choose an option (1-3): ")

        if choice == "1":
            while True:
                print("\nTicket Booking:")
                print("1. Register")
                print("2. Login")
                print("3. Go Back")
                sub_choice = input("Please choose an option (1-3): ")
                if sub_choice == "1":
                    register_user()
                elif sub_choice == "2":
                    login_and_book()
                elif sub_choice == "3":
                    break
                else:
                    print("Invalid choice. Please select an option from 1 to 3.")
        elif choice == "2":
            check_status()
        elif choice == "3":
            register_or_login()
        else:
            print("Invalid choice. Please select an option from 1 to 3.")


# Function to handle registration or login from the "Other" menu
def register_or_login():
    while True:
        print("\nOther Services:")
        print("1. Register")
        print("2. Login")
        print("3. Go Back")
        sub_choice = input("Please choose an option (1-3): ")
        if sub_choice == "1":
            register_user()
        elif sub_choice == "2":
            login_user()
        elif sub_choice == "3":
            break
        else:
            print("Invalid choice. Please select an option from 1 to 3.")


# Trains dictionary
trains = {
    '1': 'Rajdhani Express',
    '2': 'Shatabdi Express',
    '3': 'Gatimaan Express',
    '4': 'Vande Bharat Express',
    '5': 'Tejas Express',
    '6': 'Maharaja Express',
    '7': 'Deccan Odyssey'
}

if __name__ == '__main__':
    main_menu()

# Close the cursor and connection
cursor.close()
db.close()
