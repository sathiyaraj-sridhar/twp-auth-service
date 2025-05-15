"""
Auth Microservice
"""

# Import standard modules.
import os

# Import Tornado web framework modules.
import tornado

# Import the configuration module.
from config import config

# Import Custom Modules
from utils.db import MySQL

# Import custom handler modules.
from handlers.auth import RootHandler, SignupHandler, LoginHandler, LogoutHandler

# Port on which the Tornado listens, this can be passed as command line arguments.
tornado.options.define('port',default=8001,type=int)


class Application(tornado.web.Application):
    """
    Custom Tornado application class that defines URL handlers and settings.
    """
    def __init__(self):
        """
        Initializes the application with URL handlers and settings.
        """
        handlers = [
            (r"/", RootHandler),
            (r"/signup", SignupHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler)
        ]
        is_cookie_secure = config['app']['scheme'] == 'https'
        samesite_value = "None" if is_cookie_secure else "Lax"
        settings = {
            'template_path':os.path.join(os.path.dirname(__file__),'templates'),
            'cookie_secret':config['app']['cookie_secret'],
            'xsrf_cookies':True,
            'xsrf_cookie_kwargs':{
                'httponly':False,
                'secure':is_cookie_secure,
                'samesite':samesite_value,
                'domain':'.'+config['app']['domain']
            },
            'debug':True
        }
        self.mysql = MySQL()
        self.config = config
        super().__init__(handlers, **settings)


if __name__ == '__main__':
    # Parse command-line options for the Tornado application.
    tornado.options.parse_command_line()
    # Create an HTTP server instance with the Tornado application.
    HttpServer = tornado.httpserver.HTTPServer(Application(),xheaders=True)
    try:
        # Start listening for incoming requests on the specified port.
        HttpServer.listen(tornado.options.options.port)
        print('Starting App...')
        # Start the Tornado I/O loop to handle requests and events.
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('Stopping App...')
    finally:
         # Stop the Tornado I/O loop and clean up resources.
        tornado.ioloop.IOLoop.instance().stop()
