"""
Manage database connections.
Ref: https://dev.mysql.com/doc/connector-python/en/connector-python-connection-pooling.html
"""

# Import the custom configuration module
from config import config

# Import community modules.
from mysql.connector import pooling


class MySQL:
    """
    Establish pool of connection to MySQL server.
    It contains the Singleton pattern for managing connections.
    """
    _instance = None

    def __new__(cls):
        """
        Returns the instance of the class if class already initialized.
        Otherwise initialize the class.
        """
        if cls._instance is None:
            cls._instance = super(MySQL, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the class.
        """
        _config = {
            "pool_name":config['mysql']['pool_name'],
            "pool_size":config['mysql']['pool_size'],
            "host":config['mysql']['host'],
            "user":config['mysql']['user'],
            "password":config['mysql']['password'],
            "database":config['mysql']['database']
        }
        self.cnxpool = pooling.MySQLConnectionPool(**_config)

    def get_connection(self):
        """
        Returns the connection from the pool of connection.
        """
        return self.cnxpool.get_connection()
