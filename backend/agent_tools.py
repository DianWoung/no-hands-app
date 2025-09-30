import requests
from langchain_core.tools import tool

# Base URL for our FastAPI application
BASE_URL = "http://localhost:8000"

@tool
def get_stock_status(product_name: str) -> str:
    """
    Looks up the stock status for a given product name.
    Returns the stock count and status (In Stock / Out of Stock).
    """
    print(f"--- Calling Tool: get_stock_status for product: {product_name} ---")
    try:
        response = requests.get(f"{BASE_URL}/api/products/{product_name}/stock")
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return f"Product: {data['product_name']}, Stock: {data['stock']}, Status: {data['status']}"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Error: Product '{product_name}' not found."
        return f"Error: An HTTP error occurred: {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error: A network error occurred: {e}"

@tool
def get_order_status(order_id: int) -> str:
    """
    Looks up the shipping status for a given order ID.
    """
    print(f"--- Calling Tool: get_order_status for order ID: {order_id} ---")
    try:
        response = requests.get(f"{BASE_URL}/api/orders/{order_id}/status")
        response.raise_for_status()
        data = response.json()
        return f"Order ID: {data['order_id']}, Status: {data['status']}"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Error: Order ID '{order_id}' not found."
        return f"Error: An HTTP error occurred: {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error: A network error occurred: {e}"

@tool
def answer_general_question(question: str) -> str:
    """
    Answers general questions about products, policies, or troubleshooting
    by searching the knowledge base. Use this for any question that is not
    about real-time stock or a specific order status.
    """
    print(f"--- Calling Tool: answer_general_question for question: '{question}' ---")
    try:
        response = requests.post(
            f"{BASE_URL}/api/knowledge/answer",
            json={"question": question}
        )
        response.raise_for_status()
        data = response.json()
        # We return a formatted string combining answer and source
        return f"Answer: {data['answer']}\nSource: {data['source']}"
    except requests.exceptions.HTTPError as e:
        return f"Error: Could not retrieve an answer. The knowledge base might be offline. Details: {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error: A network error occurred: {e}"

# A list of all tools available to the agent
all_tools = [get_stock_status, get_order_status, answer_general_question]