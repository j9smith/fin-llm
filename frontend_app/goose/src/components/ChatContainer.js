import React, { useState, useEffect, useRef } from 'react';
import { Form, Button, Card } from 'react-bootstrap';
import { marked } from 'marked';


function ChatContainer( { setActiveUIElement, setNewsData }) {

  // Set the states for the component
  // A state is an object that holds information about a component's current situation or data that is likely to change
  // We use states here to store the chat history 
  // States are mutable (their value can be changed) and triggers re-renders when updated

  // useState('')/useState([]) sets the initial value of the state to an empty string/an empty list respectively 
  // [input, is the state variable, which holds the current value of the state
  // , setInput] is the state setter function, which is the function we call to update the state variable with a new value
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]); // state variable 'messages', set by 'setMessages'
  const chatWindowRef = useRef(null);
  const maxHistoryLength = 5;

  // handleSendMessage called when 'Send' is clicked or the enter key is pressed in the prompt entry textbox
  const handleSendMessage = () => {

    // If the input is empty then do nothing
    if (!input.trim()) return;

    // Creates a new object with variable 'sender' as 'user' and the variable 'text' as the contents of the input 
    const newUserMessage = { sender: 'user', text: input };

    // Updates the state variable 'messages'
    // Calling 'setMessages' triggers a re-render of the component with the updated messages state
    // prevMessages => { .. } is a callback function which uses the current state as an argument (i.e., the status of the chat before the new addition)
    // updatedMessages is the new message array which contains the current status appended with the new user message
    // 'return updatedMessages' sets the messages state as updatedMessages
    setMessages(prevMessages => {
      const updatedMessages = [...prevMessages, newUserMessage];
      return updatedMessages;
    });

    // Empties the input box after the user message is sent 
    setInput('');

    // Send message to backend, in correct format to avoid parsing
    // Sends the last 5 messages from the chat 
    // Appends the users most recent input 
    const context = messages
    .slice(-maxHistoryLength) 
    .concat(newUserMessage)
    .map(msg => ({
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.text
    }));

    const apiUrl = process.env.REACT_APP_API_URL; // add REACT_APP_API_URL=http://127.0.0.1:8000 to .env for local to work, within goosedlegs
    console.log("API URL:", process.env.REACT_APP_API_URL);
    fetch(`${apiUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: context })
    })
      .then(response => {
        if (!response.body) throw new Error('ReadableStream not supported');
        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let accumulatedText = '';
        let isFirstChunk = true;

        function readChunk() {
          reader.read().then(({ done, value }) => {
            
            // Check the value (chunk) contains data
            if (value) {

              // Initialises an instance of TextDecoder, taking value (chunk) and converting into text string
              // stream:true allows decoder to handle streaming data
              const chunk = decoder.decode(value, { stream: true });

              // We use this to handle JSON objects passed through the stream (i.e., for our genUI objects)
              // Try to parse each chunk as a JSON object, and if it contains a field 'ui_type', then generate a widget
              // After handling the UI object, continue to read chunks
              try {
                const parsedJson = JSON.parse(chunk);
                if (parsedJson.ui_type) {
                    if (parsedJson.target === "news_space") {
                        setNewsData(parsedJson);  // We need this prop from Workspace
                    } else {
                        setActiveUIElement(parsedJson);
                    }
                    readChunk();
                    return;
                } else {
                    throw new Error();
                }
            } catch (e) {
                // Not JSON, proceed with normal handling
            }

              // Decoded text is appended to an accumulator to build up the response
              // Formatted for Markdown on the go 
              accumulatedText += chunk;
              const formattedChunk = marked.parse(accumulatedText);
        
              // If the first chunk of response, create a new entry in 'messages' with the sender 'bot' 
              // Performs a check to see if the last message was a bot message, in which case append chunks to that instead of creating a new message (fixes duplication bug)
              // Each time setMessages() is called, the state of 'messages' is changed and the component is re-rendered to show the next text
              if (isFirstChunk) {
                setMessages(prevMessages => {
                  const lastMessage = prevMessages[prevMessages.length - 1];
                  if (lastMessage && lastMessage.sender === 'bot') {
                    lastMessage.text = formattedChunk;
                    isFirstChunk = false;
                    return [...prevMessages];
                  } else {
                    const updatedMessages = [...prevMessages, { sender: 'bot', text: formattedChunk }];
                    isFirstChunk = false; 
                    return updatedMessages;
                  }
                });
              } else {
                setMessages(prevMessages => {
                  const updatedMessages = [...prevMessages];
                  updatedMessages[updatedMessages.length - 1].text = formattedChunk; 
                  return updatedMessages;
                });
              }
        
              chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
            }
        
            // Once the stream is done apply any final cleaning up (Markdown, trim whitespace) - we could probably remove this
            if (done) {
              if (accumulatedText.trim()) {
                setMessages(prevMessages => {
                  const updatedMessages = [...prevMessages];
                  updatedMessages[updatedMessages.length - 1].text = marked.parse(accumulatedText.trim());
                  return updatedMessages;
                });
              }
              return;
            }
            readChunk();
          }).catch(error => {
            console.error('Stream read error:', error);
            setMessages(prevMessages => [...prevMessages, { sender: 'bot', text: 'An error occurred while streaming the response.' }]);
          });
        }
        readChunk();
      })
      .catch(error => {
        console.error('Fetch error:', error);
        setMessages(prevMessages => [...prevMessages, { sender: 'bot', text: 'An error occurred while fetching the response.' }]);
      });
  };


  // useEffect allows us to perform 'side effects' when our components are re-rendered (e.g., the state variable changes; a new messages is added)
  // The interior deals with the logic - in this case, scrolling to the bottom of the chatbox
  // The array afterwards contains the dependencies
  // The useEffect() function will only run if any of the dependencies in the array change between renders
  // In our case, if the component is re-rendered and the 'messages' array has changed (i.e., new message)
  // Then scroll to the bottom of chatWindow 
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  // Event listener for clicked links 
  useEffect(() => {
    const handleLinkClick = (event) => {
      const target = event.target;
      if (target.tagName === 'A' && target.href.includes('/company/')) {
        event.preventDefault(); // Prevent default navigation
        const companyName = target.textContent;
        console.log(`Custom behavior for: ${companyName}`);
        // Replace console.log to implement custom behaviour when links (i.e., company names) are clicked
      }
    };
    const chatContainer = chatWindowRef.current;
    if (chatContainer) {
      chatContainer.addEventListener('click', handleLinkClick);
    }
    // Cleanup event listener on component unmount
    return () => {
      if (chatContainer) {
        chatContainer.removeEventListener('click', handleLinkClick);
      }
    };
  }, [messages]);

  return (
    <Card className="p-3 h-100">
      <Card.Body className="d-flex flex-column h-100">
        <div ref={chatWindowRef} className="chat-window mb-3 flex-grow-1" style={{ overflowY: 'auto', maxHeight: '100%' }}>
          
          {/* Iterates over messages state array and renders each message as a div based on sender (user/bot) */}
          {messages.map((msg, index) => (
            <div key={index} className={`my-2 ${msg.sender === 'user' ? 'text-end' : 'text-start'}`}>
              <Card.Text
              style={{ backgroundColor: msg.sender === 'user' ? '' : '#f2f2f2', color: msg.sender === 'user' ? '' : '#000000' }}
              className={`d-inline-block p-2 rounded ${msg.sender === 'user' ? 'bg-primary text-white' : ''}`} dangerouslySetInnerHTML={{ __html: msg.text }}></Card.Text>
            </div>

          ))}
        </div>
        <Form.Control
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          className="mb-2"
        />
        <Button variant="primary" onClick={handleSendMessage}>Send</Button>
      </Card.Body>
    </Card>
  );
}

export default ChatContainer;
