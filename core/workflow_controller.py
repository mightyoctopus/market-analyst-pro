from core.agent_manager import AgentManager
from core.messages import Messages
import autogen

class WorkflowController:
    def __init__(self, agents: AgentManager, msg: Messages):
        self.agents = agents
        self.msg = msg

    def reflection_message(self, _, messages, *__) -> str:
        if not messages:
            return "No content to review."
        last_msg = messages[-1]["content"]
        return f"""
                Review the following content.
                \n\n {last_msg}
                """

    def build_review_chats(self) -> list[dict[str, any]]:
        reviewers = self.agents.reviewers
        common_attributes = {
            "message": self.reflection_message,
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": """
                                      Return review in a JSON object only:
                                      e.g. {"reviewer": "", "review": ""}
                                      """
            },
            "max_turns": 1,
        }

        return [
            {**{"recipient": reviewers["legal"]}, **common_attributes},
            {**{"recipient": reviewers["consistency"]}, **common_attributes},
            {**{"recipient": reviewers["text_alignment"]}, **common_attributes},
            {**{"recipient": reviewers["completion"]}, **common_attributes},
            {
                "recipient": reviewers["meta"],
                "message": self.msg.return_meta_reviewer_msg(),
                "max_turns": 1,
            }
        ]

    def build_main_chat_flow(self):
        common_attributes = {
            "summary_method": "reflection_with_llm",
            "clear_history": False
        }

        return [
            {
                **{
                    "sender": self.agents.user_proxy_auto,
                    "recipient": self.agents.financial_assistant,
                    "message": self.msg.financial_task_msg[0],
                    "summary_args": self.msg.return_summary_prompt_user_proxy_to_financial_assistant(),
                    "carryover": "Wait for confirmation of code execution before terminating the conversation. Verify that the data is not completely composed of NaN values. Reply TERMINATE in the end when everything is done."
                },
                **common_attributes
            },
            {
                **{
                    "sender": self.agents.user_proxy_auto,
                    "recipient": self.agents.research_assistant,
                    "message": self.msg.financial_task_msg[1],
                    "summary_args": self.msg.return_summary_prompt_user_proxy_to_research_assistant(),
                    "carryover": "Wait for confirmation of code execution before terminating the conversation. Verify that the data is not completely composed of NaN values. Reply TERMINATE in the end when everything is done."
                },
                **common_attributes
            },
            {
                "sender": self.agents.critic,
                "recipient": self.agents.writer,
                "message": self.msg.create_writing_task_message()[0],
                "carryover": "Wait for confirmation of code execution before terminating the conversation. Verify that the data is not completely composed of NaN values. Reply TERMINATE in the end when everything is done.",
                "max_turns": 2,
                "summary_method": "last_msg",
            },
            {
                "sender": self.agents.user_proxy_auto,
                "recipient": self.agents.export_assistant,
                "message": self.msg.exporting_task[0],
                "carryover": "Wait for confirmation of code execution before terminating the conversation. Reply TERMINATE in the end when everything is done.",
            }
        ]

    def run(self):
        self.agents.critic.register_nested_chats(
            chat_queue=self.build_review_chats(),
            trigger=self.agents.writer
        )

        return autogen.initiate_chats(self.build_main_chat_flow())

