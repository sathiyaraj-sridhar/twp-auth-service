"""
Authentication request handlers.
"""

# Import standard modules.
from datetime import datetime, timezone, timedelta

# Import ecryption module.
import jwt

# Import hashing module.
from argon2 import PasswordHasher

# Import the base handler from custom modules.
from handlers.base import BaseHandler

# Import form validate module.
from utils.form import validate
from utils.exception import ValidationError
from models.employee import EmployeeModel


class RootHandler(BaseHandler):
    """
    Handles requests to the root URL ("/") of the application.

    The RootHandler is responsible for redirecting any requests to the root URL ("/")
    to the login page ("/login"). This ensures that employees are directed to the appropriate
    entry point of the application, typically where authentication occurs.

    Methods:
        get: Processes GET requests to the root URL and redirects to the login page.
    """

    def get(self):
        """
        Processes GET requests to the root URL ("/").

        This method automatically redirects employees to the login page ("/login").
        It does not return any content directly but issues an HTTP 302 redirect.

        Returns:
            None: This method does not return a value.
        """
        self.redirect("/login", permanent=False)


class SignupHandler(BaseHandler):
    """
    Handles routes related to employee signup.

    Methods:
        get: Processes GET requests to render the signup page.
        post: Processes POST requests to handle employee signup and redirect to the login page.
    """

    def get(self):
        """
        Processes GET requests to render the signup page.

        Returns:
            None: This method does not return a value but renders the 'signup.html' template.
        """
        self.vars['title'] = f"Create your account - {self.config['app']['name']}"
        self.render('signup.html', **self.vars)

    def post(self):
        """
        Processes POST requests to handle employee signup.

        Returns:
            None: This method does not return a value but redirects to the '/login' route.
        """
        self.vars['title'] = f"Create your account - {self.config['app']['name']}"
        try:
            # Step 1: Collect employee's data.
            emp_data = {
                'name': self.get_argument("name"),
                'email': self.get_argument("email"),
                'phone': self.get_argument("phone"),
                'username': self.get_argument("username"),
                'password': self.get_argument("password")
            }

            # Step 2: Validate employee's data.
            is_valid, errors = validate(emp_data)
            if not is_valid:
                raise ValueError(errors)

            # Step 3: Instantiate employee model and verify whether given username is exist.
            employee = EmployeeModel()
            if employee.read_by_username(emp_data['username']):
                raise ValidationError("Username already exists.")

            # Step 4: Instantiate password hasher and hash the employee's password.
            ph = PasswordHasher()
            emp_data['password'] = ph.hash(emp_data['password'])

            # Step 5: Create a new employee.
            emp_data['title'] = 'Software Engineer'
            emp_data['status'] = '0'
            emp_data['role'] = '0'
            response = employee.create(emp_data)
            if not response:
                raise Exception({"status": "error", "message": "Unexpected error."})

            self.vars['notify'].append(
                {"status": "Success", "message": "Account created successfully."}
            )
            self.render('signup.html', **self.vars)
        except ValueError as ve:
            for e in ve.args[0].items():
                self.vars['notify'].append({'status':'Error','message':f'{e[0].upper()}: {e[1]}'})
            self.render('signup.html', **self.vars)
        except ValidationError as ve:
            self.vars['notify'].append({'status':'Error','message':ve})
            self.render('signup.html', **self.vars)
        except Exception as e:
            print(e)
            self.vars['notify'].append({'status':'Error','message':'Internal server error.'})
            self.render('signup.html', **self.vars)


class LoginHandler(BaseHandler):
    """
    Handles routes related to employee login.

    Methods:
        get: Processes GET requests to render the login page.
        post: Processes POST requests to handle employee login and redirect to the home page.
    """

    def get(self):
        """
        Processes GET requests to render the login page.

        Returns:
            None: This method does not return a value but renders the 'login.html' template.
        """
        self.vars['title'] = f"Login your account - {self.config['app']['name']}"
        self.render('login.html',**self.vars)

    def post(self):
        """
        Processes POST requests to handle employee login.

        Returns:
            None: This method does not return a value but redirects to the '/home' route.
        """
        self.vars['title'] = f"Login your account - {self.config['app']['name']}"
        try:
            # Step 1: Collect employee's inputs.
            emp_data = {
                'username': self.get_argument("username"),
                'password': self.get_argument("password")
            }

            # Step 2: Validate employee's data.
            is_valid, errors = validate(emp_data)
            if not is_valid:
                raise ValueError(errors)

            # Step 3: Instantiate employee model
            employee = EmployeeModel()
            # Fetch existing employee data for given username.
            existing_emp_data = employee.read_by_username(emp_data['username'])
            if not existing_emp_data:
                raise ValidationError("Invalid credentials.")

            # Step 4: Instantiate password hasher and hash the employee's password.
            ph = PasswordHasher()

            # Step 5: Validate password.
            if not ph.verify(existing_emp_data['password'], emp_data['password']):
                raise ValidationError("Invalid password.")

            # Step 6: Delete password in the existing employee data.
            del existing_emp_data['password']

            # Step 7: Generaate token.
            existing_emp_data['exp'] = datetime.now(tz=timezone.utc) + timedelta(days=1)
            token = jwt.encode(
                existing_emp_data,
                self.config['app']['app_secret'],
                algorithm="HS256"
            )

            # Step 8: Set cookie and redirect to account dashboard.
            is_cookie_secure = self.config['app']['scheme'] == 'https'
            samesite_value = "None" if is_cookie_secure else "Lax"
            self.set_signed_cookie(
                'auth',
                token,
                httponly=True,
                secure=is_cookie_secure,
                samesite=samesite_value,
                domain='.'+self.config['app']['domain']
            )

            account_microservice_url = self.config['app']['account_microservice']['url']
            self.redirect(f"{account_microservice_url}/dashboard", permanent=False)
        except ValueError as ve:
            for e in ve.args[0].items():
                self.vars['notify'].append({'status':'Error','message':f'{e[0].upper()}: {e[1]}'})
            self.render('login.html', **self.vars)
        except ValidationError as ve:
            self.vars['notify'].append({'status':'Error','message':ve})
            self.render('login.html', **self.vars)
        except Exception as e:
            print(e)
            self.vars['notify'].append({'status':'Error','message':'Internal server error.'})
            self.render('login.html', **self.vars)


class LogoutHandler(BaseHandler):
    """
    Handles routes related to employee logout.

    Methods:
        get: Processes GET requests to handle employee logout and redirect to the login page.
    """

    def get(self):
        """
        Processes GET requests to handle employee logout.

        Returns:
            None: This method does not return a value but redirects to the '/login' route.
        """
        is_cookie_secure = self.config['app']['scheme'] == 'https'
        samesite_value = "None" if is_cookie_secure else "Lax"
        self.clear_all_cookies(
            httponly=True,
            secure=is_cookie_secure,
            samesite=samesite_value,
            domain='.'+self.config['app']['domain']
        )
        self.redirect("/login", permanent=False)
