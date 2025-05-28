import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")



external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

translator = Agent(
    name="Translator",
    instructions="""
    Your sole job is to translate non-English input into English. 
    If the input is already in English or not a translation task, respond with:
    'I'm only here to help with translation. Please enter text in a different language.'
    """,
)

user_input = input("\n\nEnter the text to translate: ")

response = Runner.run_sync(
    translator,
    input= user_input,
    run_config=config
)

print("\n\nTranslated text:")
print(response.final_output)


