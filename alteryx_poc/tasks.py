from attr import field, Factory
import json
from typing import Callable

from griptape.tasks import ToolkitTask, ActionSubtask, PromptTask
from griptape.utils import minify_json

from alteryx_poc.utils.j2 import J2


class AlteryxToolkitTask(ToolkitTask):
    generate_assistant_subtask_template: Callable[[ActionSubtask], str] = field(
        default=Factory(
            lambda self: self.assistant_subtask_template_generator,
            takes_self=True,
        ),
        kw_only=True,
    )
    generate_user_subtask_template: Callable[[ActionSubtask], str] = field(
        default=Factory(
            lambda self: self.user_subtask_template_generator, takes_self=True
        ),
        kw_only=True,
    )

    def assistant_subtask_template_generator(self, subtask: ActionSubtask) -> str:
        return J2("templates/assistant_subtask.j2").render(subtask=subtask)

    def user_subtask_template_generator(self, subtask: ActionSubtask) -> str:
        return J2("templates/user_subtask.j2").render(subtask=subtask)

    def default_system_template_generator(self, _: PromptTask) -> str:
        memories = [r for r in self.memory if len(r.activities()) > 0]

        action_schema = minify_json(
            json.dumps(
                ActionSubtask.action_schema(self.action_types).json_schema(
                    "ActionSchema"
                )
            )
        )

        return J2("templates/react.j2").render(
            rulesets=self.all_rulesets,
            action_schema=action_schema,
            tool_names=str.join(", ", [tool.name for tool in self.tools]),
            tools=[
                J2("templates/partials/_tool.j2").render(tool=tool)
                for tool in self.tools
            ],
            memory_names=str.join(", ", [memory.name for memory in memories]),
            memories=[
                J2("templates/partials/_tool_memory.j2").render(memory=memory)
                for memory in memories
            ],
        )
