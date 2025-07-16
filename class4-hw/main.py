from agents import Agent, Runner, function_tool
from connection import config
import aiohttp

@function_tool
async def get_furniture() -> list:
    url = "https://hackathon-apis.vercel.app/api/products"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return [{"error": f"Failed to fetch data. Status code: {response.status}"}]

            try:
                content_type = response.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    text = await response.text()
                    return [{"error": f"Unexpected content type: {content_type}", "body": text}]

                data = await response.json()
                return data

            except Exception as e:
                return [{"error": f"Error decoding response: {str(e)}"}]
        
agent = Agent(
    name="assistant",
    instructions="""
        You are a helpful assistant with access to a function that gives you furniture products.
        The user might ask for specific types of furniture like sofas, beds, tables, etc.

        You can call the get_furniture tool to get a list of all products.
        Then you should look through the name and description fields to find the items
        that match what the user is asking about. Respond in a clear and helpful way.
        If nothing is found, just say that.""",
        tools=[get_furniture]
)
loop = True
while loop == True:
    userInput = input("Give the prompt (type 'exit' or 'q' to close): ")
    if userInput.lower() == "q" or "exit":
        loop = False
    else:
        result = Runner.run_sync(
        agent,
        userInput,
        run_config=config
        )
        print(result.final_output)




