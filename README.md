# Financial Advisor LLM

Features:
- **Framework**: Leverages OpenAI's API and built with a FastAPI backend and a node.js frontend, using PostgreSQL for data storage.
- **Tool calling**: The LLM has access to tool calls to support operation, e.g., calling APIs, retrieving portfolios, etc.
- **Multi-agentic framework**: Uses an orchestration agent to direct requests to agents optimised for specific roles.
- **Vector store retrieval**: Stores regulatory filings in a vector database (ChromaDB/pgvector) for retrieval during inference.
- **API calls**: Can access up-to-date news, regulatory filings, and real-time data feeds via API calls.
- **Generative UI**: Populates UI elements in a generative fashion as directed by the LLM, useful for displaying data.
- **User auth**: User authentication handled via FastAPI/SQLAlchemy/PostgreSQL. 
