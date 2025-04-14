import os
import asyncio
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

load_dotenv()

async def main():
    # Load OpenAI client
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    postgres_conn_str = os.getenv("POSTGRES_CONN_STR")

    # Use local command-line code executor (within current Python env)
    code_executor = LocalCommandLineCodeExecutor(work_dir="./")
    await code_executor.start()

    # Define the code execution agent
    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutor",
        code_executor=code_executor
    )

    # FinderAgent that writes Python code using pandas
    finder = AssistantAgent(
        name="FinderAgent",
        model_client=model_client,
        system_message=(
            "Your role is ONLY to read 'data/messy_sales.csv' using pandas, "
            "summarize it using print(), and save the raw dataframe as-is to 'data/temp_clean_input.csv' using df.to_csv(). "
            "Do not clean or modify the data. ONLY summarize and save."
        )
    )

    transformer = AssistantAgent(
        name="TransformerAgent",
        model_client=model_client,
        system_message=(
            "Your job is to read the file 'data/temp_clean_input.csv' using pandas, "
            "clean the data by doing the following:\n"
            "- Fill missing Product Name with 'Unknown'\n"
            "- Convert Quantity to numeric (set invalid to 0)\n"
            "- Fill missing Price with 0\n"
            "- Convert Sale Date to datetime (drop rows where invalid)\n"
            "Then write the cleaned data to 'data/final_clean.csv'.\n"
            "Use print(df.head()) at the end to show the result.\n"
            "Respond only with executable Python code inside triple backticks. "
        )
    )

    loader = AssistantAgent(
        name="LoaderAgent",
        model_client=model_client,
        system_message=(
            f"Load the data from 'data/final_clean.csv' into Postgres table 'sample_schema.sales_data' "
            f"using pandas and SQLAlchemy with connection string: '{postgres_conn_str}'.\n"
            "Steps:\n"
            "- Read the CSV using pandas\n"
            "- Add column 'ingestion_ts' with pd.Timestamp.now()\n"
            "- Rename all column names to lowercase and replace spaces with underscores\n"
            "- Use df.to_sql(..., if_exists='append') to load\n"
            "- If load is successful, print only this exactly: 'Load Successful. Task Completed.'\n"
            "- Once printed, do not perform any further actions.\n"
            "Only output python code in triple backticks."
        )
    )

    # Orchestrator (you)
    orchestrator = UserProxyAgent(name="Orchestrator")

    # Setup round-robin group chat
    groupchat = RoundRobinGroupChat(
        participants=[orchestrator, finder, code_executor_agent, transformer, loader],
        max_turns=20,
        termination_condition=TextMentionTermination("Thanks")
    )

    # Start the conversation
    await Console(groupchat.run_stream(
        task="Ingest 'data/messy_sales.csv' into Postgres table 'sample_schema.sales_data' after cleaning it properly."
    ))

    # Cleanup
    await model_client.close()
    await code_executor.stop()

if __name__ == "__main__":
    asyncio.run(main())