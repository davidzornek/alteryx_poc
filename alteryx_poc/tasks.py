from attr import field, Factory
from typing import Callable

from griptape.tasks import ToolkitTask, ActionSubtask
from griptape.utils import J2


class AlteryxToolkitTask(ToolkitTask):
    def __attrs_post_init__(self):
        self.generate_assistant_subtask_template: Callable[
            [ActionSubtask], str
        ] = field(
            default=Factory(
                lambda self: self.assistant_subtask_template_generator,
                takes_self=True,
            ),
            kw_only=True,
        )
        self.generate_user_subtask_template: Callable[[ActionSubtask], str] = field(
            default=Factory(
                lambda self: self.user_subtask_template_generator, takes_self=True
            ),
            kw_only=True,
        )

    def assistant_subtask_template_generator(self, subtask: ActionSubtask) -> str:
        return J2("alteryx_poc/templates/assistant_subtask.j2").render(subtask=subtask)

    def user_subtask_template_generator(self, subtask: ActionSubtask) -> str:
        return J2("alteryx_poc/toolkit_task/user_subtask.j2").render(subtask=subtask)
