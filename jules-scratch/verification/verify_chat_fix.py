from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the local development server
            page.goto("http://localhost:3000")

            # Wait for the input field to be ready
            input_selector = "input[placeholder='Ask about products, stock, or orders...']"
            expect(page.locator(input_selector)).to_be_visible(timeout=10000) # 10s timeout

            # Type a message and send it
            page.fill(input_selector, "css grid的用法")
            page.click("button:has-text('Send')")

            # Wait for the AI's response container to appear and have some text.
            # We target the last message element, which should be the AI's.
            response_selector = ".prose:not(.prose-invert)"

            # Wait for the final response to be rendered (isThinking is false)
            # This is a bit tricky, we'll wait for the response to contain some stable text.
            # The streaming makes it hard to know when it's "done".
            # Let's wait for a piece of text that appears at the end of the example response.
            expect(page.locator(response_selector).last).to_contain_text("Stack Overflow", timeout=20000) # 20s timeout for stream

            # Take a screenshot of the chat area
            page.locator("main").screenshot(path="jules-scratch/verification/verification.png")

        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()