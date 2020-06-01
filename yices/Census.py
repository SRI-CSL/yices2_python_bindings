


class Census:

    configs = 0

    contexts = 0

    models = 0

    params = 0

    @staticmethod
    def dump():
        return f'Contexts: {Census.contexts}\nConfigs: {Census.configs}\nModels: {Census.models}\nParams: {Census.params}'
