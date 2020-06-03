


class Census:

    configs = 0

    contexts = 0

    models = 0

    params = 0

    @staticmethod
    def dump():
        return f'\tContexts: {Census.contexts}\n\tConfigs: {Census.configs}\n\tModels: {Census.models}\n\tParams: {Census.params}'
