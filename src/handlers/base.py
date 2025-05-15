"""
Base request handler.
"""

# Import Tornado web framework module.
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """
    A base request handler that provides common functionality for all other request handlers.

    Properties:
        db (Database): Provides access to the MySQL database instance.
        config (dict): Provides access to the application configuration settings.

    Methods:
        initialize: Sets up common properties and settings for the handler.
        get_template_namespace: Retrieves the template namespace
                                with additional configuration settings.
    """

    @property
    def mysql(self):
        """
        Provides access to the MySQL database instance.

        Returns:
            Database: The database instance from the application.
        """
        return self.application.mysql

    @property
    def config(self):
        """
        Provides access to the application configuration settings.

        Returns:
            dict: The configuration settings of the application.
        """
        return self.application.config

    def initialize(self):
        """
        Sets up common properties and settings for the handler.

        Returns:
            None: This method does not return a value.
        """
        self.vars = {}
        self.vars['title'] = self.config['app']['name']
        self.vars['notify'] = []
        self.vars['auth_microservice_url'] = self.config['app']['auth_microservice']['url']
        self.vars['account_microservice_url'] = self.config['app']['account_microservice']['url']
        self.vars['chat_microservice_url'] = self.config['app']['chat_microservice']['url']
        self.vars['cdn_url'] = self.config['app']['cdn']['url']
