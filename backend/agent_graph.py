import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor

from .agent_tools import all_tools

# Load environment variables
load_dotenv(dotenv_path='backend/.env')
if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "YOUR_OPENAI_API_KEY_HERE":
    print("Warning: OPENAI_API_KEY not set. The Agent will not be able to function.")

# --- 1. Define the Agent State ---
class AgentState(TypedDict):
    """
    Represents the state of our agent. It's a dictionary that holds the
    conversation history in the 'messages' key.
    """
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]

# --- 2. Define the Graph Nodes ---

# Initialize the tool executor and the language model
tool_executor = ToolExecutor(all_tools)
# We will use a powerful model that is good at function calling
model = ChatOpenAI(temperature=0, model="gpt-4o")
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

def call_tool(state: AgentState):
    """
    The 'action' node. It executes the tools that the model has decided to call.
    """
    print("--- ACTION: Calling tool... ---")
    # The last message in the state should be the AI's decision to call a tool
    last_message = state['messages'][-1]

    # Ensure the message is an AIMessage with tool_calls
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        # This case should ideally not be reached if the graph logic is correct
        return {"messages": [HumanMessage(content="Error: No tool call found in the last message.")]}

    # Execute the tool calls
    tool_invocations = last_message.tool_calls
    tool_outputs = tool_executor.batch(tool_invocations)

    # Format the outputs as ToolMessage objects
    tool_messages = [
        ToolMessage(content=str(output), tool_call_id=inv["id"])
        for inv, output in zip(tool_invocations, tool_outputs)
    ]

    return {"messages": tool_messages}

# --- 3. Define the Graph Edges ---

def should_continue(state: AgentState) -> str:
    """
    This function decides the next step after the model has been called.
    - If the model decided to call a tool, we route to the 'action' node.
    - If the model responded directly without calling a tool, we are done ('END').
    """
    print("--- DECISION: Evaluating model response... ---")
    last_message = state['messages'][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        # The model wants to use a tool
        print("--- DECISION: Route to ACTION ---")
        return "continue"
    else:
        # The model has provided a final answer
        print("--- DECISION: Route to END ---")
        return "end"

# --- 4. Assemble the Graph ---

# Create a new state graph
workflow = StateGraph(AgentState)

# Add the nodes
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

# Define the entry point and the edges
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)
workflow.add_edge("action", "agent")

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