import yices_api as yapi

from .YicesException import YicesException


class Config:


    def __init__(self):
        self.config = yapi.yices_new_config()

    def default_config_for_logic(self, logicstr):
        assert self.config is not None
        errcode = yapi.yices_default_config_for_logic(self.config, logicstr)
        if errcode == -1:
            raise YicesException('yices_default_config_for_logic')

    def set_config(self, key, value):
        assert self.config is not None
        errcode = yapi.yices_set_config(self.config, key, value)
        if errcode == -1:
            raise YicesException('yices_set_config')

    def dispose(self):
        yapi.yices_free_config(self.config)
        self.config = None
