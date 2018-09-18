import yices


class Config(object):


    def __init__(self):
        self.config = yices.yices_new_config()

    def default_config_for_logic(self, logicstr):
        assert self.config is not None
        yices.yices_default_config_for_logic(self.config, logicstr)

    def set_config(self, key, value):
        assert self.config is not None
        yices.yices_set_config(self.config, key, value)

    def dispose(self):
        yices.yices_free_config(self.config)
        self.config = None
