import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';

// --- Main Chat Component ---
function App() {
  // --- State Management ---
  const [messages, setMessages] = useState([]); // Stores the chat history
  const [input, setInput] = useState(''); // The user's current input
  const [status, setStatus] = useState('Disconnected'); // Connection status
  const ws = useRef(null); // Ref to hold the WebSocket object
  const messagesEndRef = useRef(null); // Ref to auto-scroll to the latest message

  // --- Auto-scrolling Effect ---
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // --- WebSocket Connection Logic ---
  useEffect(() => {
    const connect = () => {
      const wsUrl = process.env.NODE_ENV === 'production'
        ? `wss://${window.location.host}/api/chat/ws`
        : 'ws://localhost:8000/api/chat/ws';

      ws.current = new WebSocket(wsUrl);

      ws.current.onopen = () => setStatus('Connected');
      ws.current.onclose = () => {
        setStatus('Disconnected. Retrying in 3s...');
        setTimeout(connect, 3000);
      };
      ws.current.onerror = (err) => {
        console.error("WebSocket error:", err);
        ws.current.close();
      };

      // --- Message Handling for Streaming ---
      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);

        setMessages(prev => {
            const lastMessage = prev[prev.length - 1];

            if (data.type === 'status') {
                // Update the status of the last "thinking" message
                if (lastMessage && lastMessage.sender === 'ai' && lastMessage.isThinking) {
                    return prev.map((msg, index) =>
                        index === prev.length - 1
                            ? { ...msg, text: data.content }
                            : msg
                    );
                }
            }
            else if (data.type === 'stream_chunk') {
                // Append the chunk to the AI's response
                if (lastMessage && lastMessage.sender === 'ai' && lastMessage.isThinking) {
                    return prev.map((msg, index) =>
                        index === prev.length - 1
                            ? { ...msg, text: msg.text + data.content }
                            : msg
                    );
                }
            }
            else if (data.type === 'stream_end') {
                // Mark the message as complete
                if (lastMessage && lastMessage.sender === 'ai' && lastMessage.isThinking) {
                    return prev.map((msg, index) =>
                        index === prev.length - 1
                            ? { ...msg, isThinking: false }
                            : msg
                    );
                }
            }
            return prev;
        });
      };
    };

    connect();

    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  // --- Sending a Message ---
  const sendMessage = () => {
    if (input.trim() && ws.current && ws.current.readyState === WebSocket.OPEN) {
      // Add user message and AI placeholder in a single state update
      setMessages(prev => [
          ...prev,
          { text: input, sender: 'user' },
          { text: '', sender: 'ai', isThinking: true }
      ]);

      ws.current.send(input);
      setInput('');
    }
  };

  // --- UI Rendering ---
  return (
    <div className="flex flex-col h-screen bg-gray-100 font-sans">
      <header className="bg-white shadow-md p-4 text-center">
        <h1 className="text-2xl font-bold text-gray-800">AI E-commerce Assistant</h1>
        <p className="text-sm text-gray-500">Status: {status}</p>
      </header>

      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`prose max-w-lg p-3 rounded-lg shadow ${msg.sender === 'user' ? 'bg-blue-500 text-white prose-invert' : 'bg-white text-gray-800'}`}>
              <ReactMarkdown>{msg.text || '...'}</ReactMarkdown>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </main>

      <footer className="bg-white shadow-t p-4">
        <div className="flex">
          <input
            type="text"
            className="flex-1 border rounded-l-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about products, stock, or orders..."
          />
          <button
            className="bg-blue-500 text-white p-2 rounded-r-lg hover:bg-blue-600 focus:outline-none"
            onClick={sendMessage}
          >
            Send
          </button>
        </div>
      </footer>
    </div>
  );
}

export default App;