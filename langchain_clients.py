import asyncio
from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

llm = ChatOpenAI()

# print(load_dotenv.get)


async def main():
    print("mcp Server")

    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": [
                    "/Users/vsahare/Desktop/Vishal/Personal/Vishal/Padhai/Udemy/EdemMCPServerCourse/mcp-servers/langchain-mcp-adapters-usage/servers/math_server.py"
                ],
            },
            "weather": {"url": "http://127.0.0.1:8000/sse", "transport": "sse"},
        }
    )

    tools = await client.get_tools()
    agent = create_agent(llm, tools)

    result = await agent.ainvoke({"messages": "What is weather in San Francisco?"})
    # result = await agent.ainvoke({"messages": "What is 1+2*3?"})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
