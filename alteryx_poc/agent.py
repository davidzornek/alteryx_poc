from griptape.structures import Agent
from griptape.tools import Calculator

from alteryx_poc.tasks import AlteryxToolkitTask


class AlteryxAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tools = [Calculator()]
        self.add_task(AlteryxToolkitTask(self.input_template, tools=self.tools))
