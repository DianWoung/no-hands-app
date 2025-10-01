import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from .agent_tools import all_tools

# Load environment variables
load_dotenv(dotenv_path='backend/.env')

# --- Get AI Service Configuration ---
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

if not api_key or api_key == "YOUR_OPENAI_API_KEY_HERE":
    print("Warning: OPENAI_API_KEY not set or is a placeholder. The Agent may not function.")

# --- 1. Define the Agent State ---
class AgentState(TypedDict):
    """
    Represents the state of our agent. It's a dictionary that holds the
    conversation history in the 'messages' key.
    """
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]

# --- 2. Define the Graph Nodes ---

# Initialize the ToolNode with our set of tools
tool_node = ToolNode(all_tools)

model = ChatOpenAI(
    temperature=0,
    model=model_name,
    openai_api_key=api_key,
    openai_api_base=api_base,
)
# Bind the tools to the model
model = model.bind_tools(all_tools)

def call_model(state: AgentState):
    """
    The 'agent' node. It calls the model to decide the next action.
    """
    print("--- AGENT: Calling model... ---")
    messages = state['messages']
    response = model.invoke(messages)
    # The response from the model is added to the state
    return {"messages": [response]}

# --- 3. Define the Graph Edges ---

# --- 4. Assemble the Graph ---

# Create a new state graph
workflow = StateGraph(AgentState)

# Add the nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Define the entry point and the edges
workflow.set_entry_point("agent")

# Use the prebuilt tools_condition to decide whether to call tools or end
workflow.add_conditional_edges(
    "agent",
    tools_condition,
    {
        # If the agent wants to call a tool, route to the 'tools' node
        "continue": "tools",
        # If the agent is finished, route to the 'end' node
        "end": END,
    },
)

# After calling a tool, we route back to the agent to respond
workflow.add_edge("tools", "agent")

# Compile the graph into a runnable object
agent_graph = workflow.compile()

print("Agent graph compiled successfully.")

# --- Helper function for running the agent ---
def run_agent(question: str, history: list = None):
    """
    Runs the agent graph with a user question and optional history.
    """
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "YOUR_OPENAI_API_KEY_HERE":
        return "I am sorry, but my brain (the Language Model) is not configured. Please set the OpenAI API key."

    inputs = [HumanMessage(content=question)]
    if history:
        inputs = history + inputs

    final_state = agent_graph.invoke({"messages": inputs})
    # The final response is the last message from the AI
    return final_state['messages'][-1].content