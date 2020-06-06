


class Census:

    configs = 0

    contexts = 0

    models = 0

    params = 0

    @staticmethod
    def dump():
        return f'Contexts: {Census.contexts}\tConfigs: {Census.configs}\tModels: {Census.models}\tParams: {Census.params}'
