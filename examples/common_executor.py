import logging
import time

from pywinauto.application import Application, ProcessNotFoundError
from pywinauto import ElementNotFoundError, WindowNotFoundError
from pywinauto.remote_memory_block import AccessDenied


class CommonController:
    def __init__(self, path: str, logger_name: str = "logger", backend: str = 'uia'):
        self.backend = backend
        self.path = path.replace('"', '')
        self.logger = logging.getLogger(name=logger_name)
        self.main_window = None
        self.main_flags = {}
        self.closed = False
        self.app = None

    def __str__(self):
        return self.__class__.__name__

    def start(self, connect_timeout: int = 30):
        self.logger.info(f"Start {self.__class__.__name__} from path: {self.path}")
        try:
            self.app = Application(backend=self.backend).connect(path=self.path, timeout=connect_timeout)
            self.logger.info(f"Connected to existing {self.__class__.__name__} instance")
        except ProcessNotFoundError:
            self.app = Application(backend=self.backend).start(self.path, wait_for_idle=True, timeout=connect_timeout)
            self.logger.info(f"Start new instance {self.__class__.__name__}")
        self._get_main_form()

    def _get_main_form(self, timeout: int = 60):
        start = time.time()
        success = False
        self.logger.info(f"Try to found main window for {self.__class__.__name__} with criteria {self.main_flags}")
        while time.time() - start < timeout and not success:
            try:
                if self.main_flags:
                    self.main_window = self.app.window(**self.main_flags)
                else:
                    self.main_window = self.app.top_window()
                self.main_window.wrapper_object()
                success = True
            except (WindowNotFoundError, ElementNotFoundError, AccessDenied):
                time.sleep(3)

        if not success:
            self.close()
            self.logger.error(f"Main window for {self.__class__.__name__} not found, exit")
            exit()

    def close(self):
        if not self.closed:
            self.logger.info(f"Close {self.__class__.__name__}")
            if self.main_window is not None:
                self.main_window.wrapper_object().close()
            else:
                self.app.kill()
            self.closed = True
        else:
            self.logger.info(f"{self.__class__.__name__} already closed")
