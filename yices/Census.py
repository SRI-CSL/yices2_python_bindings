"""For leak detection"""

from .Context import Context
from .Config import Config
from .Parameters import Parameters
from .Model import Model
from .StringBuilder import StringBuilder

class Census:

    @staticmethod
    def dump():
        sb = StringBuilder()
        sb.append('\nCensus:\n')
        sb.append(f'\tContexts     {Context.population()}\n')
        sb.append(f'\tConfigs      {Config.population()}\n')
        sb.append(f'\tModels       {Model.population()}\n')
        sb.append(f'\tParameters   {Parameters.population()}\n')
        return str(sb)
