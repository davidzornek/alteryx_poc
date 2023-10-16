from griptape.structures import Agent
from griptape.tools import Calculator

from alteryx_poc.tasks import AlteryxToolkitTask


class AlteryxAgent(Agent):
    def __init__(self, character_sheet):
        super().__init__()
        self.character_sheet = character_sheet
        self.tools = [Calculator()]
        self.add_task(AlteryxToolkitTask(self.input_template, tools=self.tools))
