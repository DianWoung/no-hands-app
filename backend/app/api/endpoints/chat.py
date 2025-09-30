from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from langchain_core.messages import AIMessage, HumanMessage

from app.services.agent_graph import agent_graph

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handles the WebSocket connection for the chat interface.
    Streams the agent's intermediate steps and final answer token by token.
    """
    await websocket.accept()
    # Each connection gets its own conversation history.
    # In a real app, you'd tie this to user sessions.
    history = []
    try:
        while True:
            user_message = await websocket.receive_text()

            # Add user message to history
            history.append(HumanMessage(content=user_message))
            graph_input = {"messages": history}

            full_response = ""

            # Use astream_events to get token-level streaming
            async for event in agent_graph.astream_events(graph_input, version="v1"):
                kind = event["event"]

                if kind == "on_tool_start":
                    await websocket.send_json(
                        {"type": "status", "content": f"Calling tool: `{event['name']}`..."}
                    )

                elif kind == "on_tool_end":
                    # This provides the output of the tool
                    await websocket.send_json(
                        {
                            "type": "status",
                            "content": f"Tool `{event['name']}` finished. Analyzing results...",
                        }
                    )

                elif kind == "on_chat_model_stream":
                    chunk = event["data"]["chunk"]
                    if isinstance(chunk, AIMessage) and chunk.content:
                        full_response += chunk.content
                        await websocket.send_json(
                            {"type": "stream_chunk", "content": chunk.content}
                        )

            # The full response is now assembled, add it to the history
            history.append(AIMessage(content=full_response))
            await websocket.send_json({"type": "stream_end"})

    except WebSocketDisconnect:
        print(f"Client disconnected: {websocket.client}")