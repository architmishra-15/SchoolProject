# Train Ticket Reservation System

This is a Python-based project that allows users to book train tickets. It provides functionalities such as user registration, login, ticket booking, and checking the status of a booked ticket.

## Dependencies

This project uses the following Python modules:

- `random`
- `getpass`
- `hashlib`
- `mysql-connector-python`

You can install the `mysql-connector-python` module using pip:

```bash
pip install mysql-connector-python
```
- To know more about `mysql-connector`, check out their <a href="https://dev.mysql.com/doc/connector-python/en/" target="_blank">official documentation</a>
- `random` <a href="https://docs.python.org/3/library/random.html" target="_blank">Documentation</a>
- `hashlib` <a href="https://docs.python.org/3/library/hashlib.html" target="_blank">official documentation</a>
- `getpass` <a href="https://docs.python.org/3/library/getpass.html" target="_blank">official documentation</a>

## How it works

The program starts by establishing a connection to a MySQL database and creating a table with the required fields if it doesn’t exist.

Users can register by providing their full name, email, password, age, gender, and mobile number. The password is hashed using SHA-256 for security purposes.

Once registered, users can log in using their email and password. After successful login, users can choose a train to book from a list of available trains. They also need to provide their departure and destination locations. A unique PNR number is generated for each booking.

Users can also check the status of their booked train by providing their email and PNR number.

## Note

There is possibilty that the program is stuck after entering email when running in an IDE.
If the program is stuck after entering email, try running it in cmd instead of IDE since most of the IDEs don’t support getpass. If you want to just check the code, you can temporarily replace getpass with input.

Use the code

```bash
python directory\folder\Project.py
```
replace `directory` with your directory where file is saved (like C: or E:) and `folder` with the folder where it is saved.


## THANK YOU
