"""
Manage the execution of employee data queries.
Ref: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
"""

# Import custom modules.
from utils.db import MySQL


class EmployeeModel:
    """
    This model performs CRUD operations for employee data.
    """
    _instance = None

    def __new__(cls):
        """
        Returns the instance of the class if class already initialized.
        Otherwise initialize the class.
        """
        if cls._instance is None:
            cls._instance = super(EmployeeModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the employee model with MySQL database connection.
        """
        self.__mysql = MySQL()

    def create(self, employee_data):
        """
        Creates a new employee in the database.
        """
        connection = None
        cursor = None
        try:
            connection = self.__mysql.get_connection()
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO employee (username, password, name, email, title, status, role)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                              (employee_data['username'], employee_data['password'],
                                employee_data['name'], employee_data['email'],
                                employee_data['title'], employee_data['status'],
                                employee_data['role'],))
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error creating employee: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def read(self, employee_id):
        """
        Retrives employee by employee id from the database.
        """
        connection = None
        cursor = None
        try:
            connection = self.__mysql.get_connection()
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM employee
                              WHERE id=%s""",
                              (employee_id,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error retrieving employee: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def read_by_email(self, email):
        """
        Retrives employee by employee email from the database.
        """
        connection = None
        cursor = None
        try:
            connection = self.__mysql.get_connection()
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM employee
                              WHERE email=%s""",
                              (email,))
            result = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            result = dict(zip(column_names, result))
            result['created'] = result['created'].strftime("%Y-%m-%d %H:%M:%S")
            result['updated'] = result['updated'].strftime("%Y-%m-%d %H:%M:%S")
            return result
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error retrieving employee: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def read_by_username(self, username):
        """
        Retrives employee by employee email from the database.
        """
        connection = None
        cursor = None
        try:
            connection = self.__mysql.get_connection()
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM employee
                              WHERE username=%s""",
                              (username,))
            result = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]
            result = dict(zip(column_names, result))
            result['created'] = result['created'].strftime("%Y-%m-%d %H:%M:%S")
            result['updated'] = result['updated'].strftime("%Y-%m-%d %H:%M:%S")
            return result
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error retrieving employee: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def update_status(self, employee_id, status):
        """
        Updates an existing employee in the database.
        """
        connection = None
        cursor = None
        try:
            connection = self.__mysql.get_connection()
            cursor = connection.cursor()
            cursor.execute("""UPDATE employee SET status=%s
                              WHERE id=%s""",
                              (status, employee_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error updating employee status: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def update_role(self, employee_id, role):
        """
        Updates an existing employee in the database.
        """
        connection = None
        cursor = None
        try:
            connection = self.__mysql.get_connection()
            cursor = connection.cursor()
            cursor.execute("""UPDATE employee SET role=%s
                              WHERE id=%s""",
                              (role, employee_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error updating employee status: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete(self, employee_id):
        """
        Deletes an existing employee in the database.
        """
        connection = None
        cursor = None
        try:
            connection = self.__mysql.get_connection()
            cursor = connection.cursor()
            cursor.execute("""DROP employee
                              WHERE id=%s""",
                              (employee_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
