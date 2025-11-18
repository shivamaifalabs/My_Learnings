""" 
try:
    risky_operation()
except SomeError:
    handle_error()
else:
    run_if_no_exception()
finally:
    run_always()

 """

# Small- Example:-

class AppError(Exception):
    #Base class for all custom application errors.
    pass


class ValidationError(AppError):
    #When user input is invalid.
    pass


class DatabaseError(AppError):
    #Base class for database-related errors.
    pass


class DatabaseConnectionError(DatabaseError):
    #Raised when DB connection fails.
    def __init__(self, host, port, message="Database connection failed"):
        self.host = host
        self.port = port
        super().__init__(f"{message} -> {host}:{port}")


class QueryExecutionError(DatabaseError):
    #Raised when a DB query fails.
    pass


#-----------------------------------
def validate_username(username: str):
    if not username:
        raise ValidationError("Username cannot be empty")

    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters")

    return username


def create_user_in_db(username, connection):
    try:
        # Simulate query failure
        result = 1 / 0
    except ZeroDivisionError as e:
        raise QueryExecutionError("Failed to execute query") from e  # Exception- Chaining

    return True
