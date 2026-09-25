import asyncio

from dotenv import load_dotenv

load_dotenv(override=True)

from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_anthropic import ChatAnthropic

# llm = ChatOpenAI()
llm = ChatAnthropic(model="claude-opus-5", temperature=0)


stdio_server_params = StdioServerParameters(
    command="python",
    args=[
        "/Users/vsahare/Desktop/Vishal/Personal/Vishal/Padhai/Udemy/EdemMCPServerCourse/mcp-servers/langchain-mcp-adapters-usage/servers/math_server.py"
    ],
)


async def main():
    print("Hello from langchain-mcp-adapters-usage!")

    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("Session initialized")
            # tools = await session.list_tools()
            tools = await load_mcp_tools(session)
            print(tools)

            agent = create_agent(llm, tools)

            response = await agent.ainvoke(
                {"messages": [HumanMessage(content="What is 2+2?")]}
            )
            print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
