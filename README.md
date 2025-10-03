# Financial Advisor LLM
<img width="873" height="541" alt="image" src="https://github.com/user-attachments/assets/b0675c88-7171-4c45-afcf-407b2550bac5" />

## Features
- **Framework**: Leverages OpenAI's API and built with a FastAPI backend and a node.js frontend, using PostgreSQL for data storage.
- **Tool calling**: The LLM has access to tool calls to support operation, e.g., calling APIs, retrieving portfolios, etc.
- **Multi-agentic framework**: Uses an orchestration agent to direct requests to agents optimised for specific roles.
- **Vector store retrieval**: Stores regulatory filings in a vector database (ChromaDB/pgvector) for retrieval during inference.
- **API calls**: Can access up-to-date news, regulatory filings, and real-time data feeds via API calls.
- **Generative UI**: Populates UI elements in a generative fashion as directed by the LLM, useful for displaying data.
- **User auth**: User authentication handled via FastAPI/SQLAlchemy/PostgreSQL.

## Installation and Execution
Requires local installation of `node.js` and `Docker Compose`. 
To install and execute:
```bash
git clone git@github.com:j9smith/fin-llm.git
cd fin-llm
npm start
```
The webpage can then be accessed at `http://127.0.0.1:3000`.

The following script must be executed to create necessary `.env` files (fill your own API keys):
```bash
echo "OPENAI_API_KEY={YOUR API KEY HERE}" > .env
echo "REACT_API_APP_URL=127.0.0.1:8000" > frontend_app/goose/.env
```

## Contributors
This project was a joint effort between: 
- [@alexlambert1](https://github.com/alexlambert1)
- [@crabbacus](https://github.com/crabbacus)
- [@j9smith](https://github.com/j9smith)
