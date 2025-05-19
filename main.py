from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class State(TypedDict):
    # messages have the type "list".
    # The add_messages function appends messages to the list, rather than ov`erwriting them
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"], stream=True)]}

if __name__ == "__main__":
    graph_builder = StateGraph(State)

    llm = ChatOpenAI(model="gpt-4o-mini")

    graph_builder.set_entry_point("chatbot")
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.set_finish_point("chatbot")

    graph = graph_builder.compile()

    # Run the chatbot
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        for event in graph.stream({"messages": [("user", user_input)]}):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)