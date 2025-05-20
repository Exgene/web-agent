from dataclasses import dataclass, field

from src.agents.base import BaseAgent, LLMType
from src.tool_calls.web_tools import WebTools
from src.utils.tool_calls import generate_json_from_tool_calls

SYSTEM_PROMPT = """

"""


@dataclass
class TaskSeperatorAgent(BaseAgent):
    input: str = ""
    system_prompt: str = field(init=False)
    llm: LLMType = None
    tool_calls: list[dict] = field(default_factory=list)

    def __post_init__(self):
        self.system_prompt = SYSTEM_PROMPT
        self.tool_calls = generate_json_from_tool_calls(WebTools)

    def run(self):
        pass
