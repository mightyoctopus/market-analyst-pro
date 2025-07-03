from dotenv import load_dotenv
import os
from datetime import datetime

from core.agent_manager import AgentManager
from core.messages import Messages
from core.workflow_controller import WorkflowController
import streamlit as st


load_dotenv()


def main():

    llm_config = {
        "model": "gpt-4.1-mini",
        "api_key": os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"],
        "temperature": 0.8,
        "timeout": 60,
    }

    date = datetime.now().strftime("%Y-%m-%d")

    col1, col2 = st.columns(2)

    with col1:
        st.title("Market Analyst Pro")
        st.markdown(
            "<span style='color:#FF6347'>😵‍💫 No more guesswork! 😵‍</span>",
            unsafe_allow_html=True
        )
        st.text("Just let our team of AI agents tells you if your stocks are set to soar!")

        assets = st.text_input(
            "What stocks do you want to look up?: (comma separated)",
            key="asset_input"
        )
        ### Reformat the assets value string to fit the file format.
        assets = assets.replace(" ", "").replace(",", "_")
        print("ASSETS USER INPUT: ", assets)
        hit_button = st.button("Start Analysis")

    with col2:
        st.image("assets/hero_img.png")

    if hit_button:
        if assets:
            msg = Messages(assets, date)
            agents = AgentManager(llm_config)
            controller = WorkflowController(agents, msg)

            with st.spinner("Please wait while our agents gather and organize a comprehensive dataset. \nThis typically takes 3 - 4 minutes..."):
                chat_results = controller.run()

            st.image("./coding/normalized_prices.png", width=800)

            ## Display the financial report
            report_path = f"./coding/{assets}_financial_report.md"
            try:
                with open(report_path, "r", encoding="utf-8") as f:
                    report_md = f.read()
                st.markdown(report_md, unsafe_allow_html=True)
            except FileNotFoundError:
                st.error(f"Could not find report at {report_path}. Would you try again in a moment?")
                try:
                    ## If failed, then try again
                    with open(report_path, "r", encoding="utf-8") as f:
                        report_md = f.read()
                    st.markdown(report_md, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"Could not find report at {report_path}. Would you try again in a moment?")
        else:
            st.info("Please type in at least one stock and hit enter.")
            return

print("NAME - main.py", __name__)
if __name__ == "__main__":
    main()





























