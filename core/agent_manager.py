import autogen

class AgentManager:
    def __init__(self, config):
        self.config = config
        self.financial_assistant = self.create_financial_assistant()
        self.research_assistant = self.create_research_assistant()
        self.writer = self.create_writer()
        self.critic = self.create_critic()
        self.reviewers = self.create_reviewers()
        self.export_assistant = self.create_exporter()
        self.user_proxy_auto = self.create_user_proxy_auto()

    def create_financial_assistant(self) -> autogen.AssistantAgent:
        return autogen.AssistantAgent(
            name="financial_assistant",
            llm_config=self.config,
        )

    def create_research_assistant(self) -> autogen.AssistantAgent:
        return autogen.AssistantAgent(
            name="research_assistant",
            llm_config=self.config,
        )

    def create_writer(self) -> autogen.AssistantAgent:
        return autogen.AssistantAgent(
            name="writer",
            llm_config=self.config,
            system_message="""
            You are a professional financial writer known for creating insightful and engaging reports.
            Your task is to write a detailed financial report in Markdown format. Use headings, bullet points, bold text, and tables where appropriate to clearly present the information.

            Important instructions:
            - Write the final report using **Markdown formatting** (e.g., `#`, `-`, `**`, tables).
            - **Do not** wrap the entire report in triple backticks or use any code block indicators (like ``` or ```markdown).
            - Only return the final Markdown-formatted report — do not include any extra explanations, comments, or metadata.
            - You must polish your writing based on the feedback you receive from critic and refine your blog post to be aligned with the given feedback.
            - When you revise the report based on the feedback, end your message with the word 'TERMINATE'.
            """
        )

    def create_critic(self) -> autogen.AssistantAgent:
        return autogen.AssistantAgent(
            name="critic",
            llm_config=self.config,
            system_message="""
            You area critic. You review the writing pieces the writer has written. 
            Your main role is to provide feedback on the writing in a way that improves the 
            quality of the content overall.
            """
        )

    def create_reviewers(self):
        return {
            "legal": autogen.AssistantAgent(
                name="legal_reviewer",
                llm_config=self.config,
                system_message="""
                You are a legal reviewer known for your ability to ensure the content is legally compliant 
                and free from any potential legal issues. 
                These are the notes you should follow:
                - Make sure your suggestion is concise (within 3 bullet points)
                concrete, highlighting only what matters. 
                - Begin your review by stating your role first.
                """
            ),
            "consistency": autogen.AssistantAgent(
                name="consistency_reviewer",
                llm_config=self.config,
                system_message="""
                You are a consistency reviewer known for your ability to ensure the written content is consistent 
                throughout the report(content). 
    
                These are the notes you should follow:
                - In case of contradictions, use the numbers and data in the report to decide which version is accurate.
                - Make sure your suggestion is concise (within 3 bullet points)
                concrete, highlighting only what matters. 
                - Begin your review by stating your role first.
                """
            ),
            "text_alignment": autogen.AssistantAgent(
                name="text_alignment_reviewer",
                llm_config=self.config,
                system_message="""
                You are a text alignment reviewer, known for your ability to ensure that all data and narrative content 
                are meaningfully and consistently aligned.
    
                Follow these instructions:
                - Check that all numbers and factual data in the text are consistent and do not contradict each other.
                - If inconsistencies are found, suggest corrections in a concise format (no more than 3 bullet points).
                - Focus only on the most important inconsistencies — be direct and concrete.
                - Start your review by stating your role.
                """
            ),
            "completion": autogen.AssistantAgent(
                name="completion_reviewer",
                llm_config=self.config,
                system_message="""
                You are a content completion reviewer responsible for verifying that financial reports include all required elements.
    
                Your task is to ensure that the report contains:
                - A news summary for each asset
                - Explanations of all financial ratios and price data
                - A discussion of possible future scenarios
                - A table comparing fundamental ratios
                - At least one figure or chart
    
                If anything is missing or incomplete, provide clear and specific suggestions — limited to 3 bullet points.
                Keep your feedback concise, concrete, and focused only on what matters.
                Begin your response by stating your role.
                """
            ),
            "meta": autogen.AssistantAgent(
                name="meta_reviewer",
                llm_config=self.config,
                system_message="""
                You are a meta reviewer. 
                Aggregate all feedback from the reviewers and summarize key suggestions for the critic. 
                Then, provide a final message for the critic to send to the writer: 'Please revise the original report based on the following feedback. 
                Return only the updated report in Markdown format. 
                End your response with TERMINATE.
                """
            )
        }

    def create_exporter(self) -> autogen.AssistantAgent:
        return autogen.AssistantAgent(
            name="exporter",
            llm_config=self.config,
        )

    def create_user_proxy_auto(self) -> autogen.AssistantAgent:
        return autogen.AssistantAgent(
            name="user_proxy_auto",
            human_input_mode="NEVER",
            is_termination_msg=lambda x: x.get("content", "").strip().endswith("TERMINATE"),
            code_execution_config={
                "last_n_messages": 3,
                "work_dir": "coding",
                "use_docker": False,
            }
        )