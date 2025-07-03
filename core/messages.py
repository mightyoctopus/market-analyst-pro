
class Messages:
    def __init__(self, stocks, date):
        self.stocks = stocks
        self.date = date

        self.financial_task_msg = self.create_financial_task_messages()
        self.writing_task = self.create_writing_task_message()
        self.exporting_task = self.create_exporting_task_message()
        self.meta_reviewer_msg = self.create_meta_reviewer_message()


    def create_financial_task_messages(self) -> list[str]:
        return [
        f"""
        What are the current stock prices of {self.stocks} on the current date as {self.date}, 
        and the performance over the past 6 months in terms of percentage change.
        Start by retrieving the full name of each stock and use it for all the future requests.
        You also need to prepare a figure of the normalized price of those stocks and save it to a file named 'normalized_prices.png'.
        I need you to make a stock analysis from these perspectives below:
        * P/E ratio
        * Forward P/E
        * Dividends
        * Price to book
        * Debt/Eq
        * ROE
        * Analyze the correlation between the stocks
        Note: Do not use a solution that requires an API key.
        If some of the data doesn't make sense, for example a price shown as 0 etc, modify the query and re-try.
        You should also analyze only the stocks user requested. Do not pull out random stock info which users didn't request.
        """,
        """Investigate possible reasons of the stock performance leveraging market news headlines from Bing News or Google Search. 
        Retrieve news headlines using python and return them. 
        Use the full name stocks to retrieve headlines. 
        Retrieve at least 10 headlines per stock. 
        Do not use a solution that requires an API key.
        Web scrape headlines only in English.
        """,
    ]

    def create_writing_task_message(self) -> list[str]:
        return [
        """
        Below are what you as a writer have to perform in your report:
        
        - Develop an engaging financial report using all given information including the chart image in the normalized_prices.png file provided,
        and factors in with any other figures given by other agents (financial, research agent and critic agent that gives you feedback).
        - Create a table comparing all the fundamental ratios and data.
        - Provide comments and description on all the fundamental ratios and data.
        - Compare the stocks, considering their correlation and risks, providing a comprehensive analysis of the stocks.
        - Provide a summary of the latest news about each stock.
        - Ensure that you comment and summarize the news headlines for each stock and provide a comprehensive analysis of the news.
        - Analyze connections between the recent news headlines provided and the fundamental ratios and explain about it in your report.
        - Provide an analysis of possible future scenarios. 
            """,
    ]

    def create_exporting_task_message(self) -> list[str]:
        return [
        f"Save the blog post in .md format using Python script (Example: {self.stocks}_financial_report.md). It must only include the content of blog post inside the md file.",
    ]

    def create_meta_reviewer_message(self) -> str:
        return """
            Aggregate all feedback from the reviewers. 
            Provide a final message to send to the writer: 'Please revise the original report based on the following feedback. 
            Return only the updated report in Markdown format. 
            End your response with TERMINATE.
        """

    def return_summary_prompt_user_proxy_to_financial_assistant(self) -> dict[str, str]:
        return {
                "summary_prompt": """
                            Return all results in a JSON object only.
                            Include the following:
                            Current stock prices
    
                            - Performance over the past 6 months (e.g., percentage change)
                            - All calculated financial metrics (P/E, ROE, Debt/Equity, etc.)
                            - The full company name for each stock
                            - A list of all figure or chart file names generated (e.g., "normalized_prices.png")
                        """
            }

    def return_summary_prompt_user_proxy_to_research_assistant(self) -> dict[str, str]:
        return {
            "summary_prompt": """
                               - Provide news headlines on the relevant stocks.
                               - Each stock name should be formatted as a paragraph.
                               - Be precise and do not include news events that aren't fact-checked or just are vague 
                               - Return the result as a JSON object only.
                       """
        }

    def return_meta_reviewer_msg(self) -> str:
        return """
        Aggregate all feedback from the reviewers. 
        Provide a final message to send to the writer: 'Please revise the original report based on the following feedback. 
        Return only the updated report in Markdown format. 
        End your response with TERMINATE.
        """




