import logging

from handlers import handlers
from classes.handler import BaseHandler
from classes.app import App
from classes.config import is_debug

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG if is_debug() else logging.INFO)

    for handler in handlers:
        _handler = handler['handler']
        _name = handler['name']

        if issubclass(_handler, BaseHandler):
            handler['handler'](_name)
        else:
            raise Exception(f'Handler "{_name}" is not initialized, due to wrong class type')

    App.updater.run_updater()

if __name__ == '__main__':
    main()
