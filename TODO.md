# To do list

Going to start collecting things that need doing in here. Feel free to add/remove.

## General

- **Logging:** we could do with implementing logging/diagnostics across the system. Would be useful to keep a handle on how well everything is performing or if there are any bugs/special cases we should be aware of.
- **Multiple threads:** ideally we need to introduce the ability to have multiple threads. Conversations will grow more and more expensive as time goes on, context gets lost, etc. Separately, the way most people use chatbots is to have a separate thread open for each topic of discussion.
- **Sessions:** we need to implement user sessions, for obvious reasons. This implicitly includes user auth which we also need to add.
- **Online deployment:** ideally we should deploy our solution on a live online server as soon as possible.
- **Metrics:** this is a big one for me. We need to start introducing metrics across the system so we can evaluate how well each aspect is performing. Basic stuff like token usage per request/conversation up to more complex stuff like evaluating the relevance of our RAG requests. What we can measure we can improve. Ideally we'd have a centralised interface where we can have an overview of all of these.
- **Generative UI:** could look in to how we can leverage our tool calls to pass back an appropriate UI element to include in a response. For example, if we're passing back some time series data, we'd want the chat to generate a graph element.
- **Defining file structures and I/O:** need to start thinking about how we're going to dynamically pull in external files (like news articles and reg. filings), how we're going to process them, and how we're going to store them.
- **Portfolio importing:** import user portfolios and store in a database. This could live in a separate part of the UI (i.e. standard upload in user area), and the model then knows to use this for context.
More generally as part of this just need the app to be able to handle user inputting e.g. an image into the chat bot itself. Doesn't necessarily need to be stored at this point, but just so it can be used as part of the context 
- **Cache:** we need to implement a cache to avoid for example redundant API requests. What if multiple users request the same stock price on the same day? We don't want to make multiple API calls, we want to pull from the cache instead. 
- **Tooling:** we need to introduce more tooling.
  - _News:_ need to add a tool to pull in recent news.
  - _Pricing:_ something that can pull in pricing data (like stock prices). Could be just call an external API for now, but I agree with Mitch that we should have some sort of static storage that we update daily, just to avoid incurring big API costs.
  - Plenty more that we could add as well
  - Do we want to add analytics for portfolios? Not saying we need the boring stuff like "tracking", but perhaps can sell it as the "tooling professionals use to analyse their positions" etc. 

## app.py

## vectorstore.py

- **Different formats:** for the moment, the vectorstore is called 'filings' and contains only reg. filings. Do we do a separate vecdb for different formats (e.g., news, analyst reports, etc.)? Or do we just tag them with metadata that describes what sort of file they are?
- **Pdf chunking:** we need to find a better way to chunk pdfs. Currently, they are split in to chunks of 500. Ideally, we'd chunk them by section headers or similar to keep each chunk topical.
- **Pre-processing:** could look in to using summarisation models to chop down any files we're importing (could be news, could be reg. filings) to increase information density. Will hopefully yield better results, more clarity for the chatbot, and lower token usage/other costs.
- **Embeddings model:** we need to look at how well we're generating embeddings for the vecdb currently. Optimisations could include changing the embedding model. We could look in to finetuning a domain-specific one, or we could look in to using finBERT.
- **Metadata parsing:** currently just uses list slicing to select the correct characters in the filename that contain our relevant metadata. We need to find a solution that is a bit more robust. What happens when we start pulling files from different reg agencies etc?
- **Results ranking:** we could look into ranking the results of our vector store retrievals for order of importance/relevance. For example, we could rank by date (e.g., most recent receives the highest ranking). Ranking by relevance could be computationally intensive so maybe not essential.
- **METRICS:**
  - We need to measure how relevant the information we're pulling is for the user query.
  - We need to measure if we're pulling information that is actually useful for the chatbot. We could look in to using ROUGE to determine how much of the returned content is making its way in to the final response (but then not sure if the chabot will just use whatever content is sent to it by default).

## chat_logic.py

-**Bug fix:** there's a bug where sometimes the model will respond normally, and then try and call a tool at the end of its response. This tool call just prints out in chat as plaintext. We need to find a way to either completely avoid, or catch and process these cases.

- **System prompt:** we need to optimise the system prompt. How do we get closer to the results we want? What do we want our chatbot to sound like? Are there any important notes we need to give the chatbot about its capabilities, or constraints for how it should perform?

## script.js
