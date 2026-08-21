1. Project Title & Overview
Anonymous Social Network & AI Support Engine
A full-stack, decoupled web application providing real-time AI emotional support and an anonymous community feed. Engineered with a non-blocking WebSocket architecture and a paginated REST API.

2. System Architecture
Backend Server: Built with FastAPI, utilizing WebSockets for real-time chat and RESTful endpoints for the social feed.

Data Persistence: Integrates SQLite via SQLAlchemy ORM for relational data mapping, alongside local object storage for media uploads.

Frontend Client: Developed in Streamlit, managing dynamic UI rendering, HTTP requests, and session state.

3. Key Engineering Features
Conversational Memory: AI instances maintain isolated conversation histories per active socket connection using the Gemini API.

Data Pagination: Implemented limit/offset SQL queries to chunk database records, preventing frontend memory exhaustion.

Admin Analytics: A secure, authenticated dashboard for monitoring engagement metrics—serving as a foundational prototype for broader B2B client management platforms.

Thread Offloading: Uses Python's asyncio to push blocking AI network calls to background threads, maximizing server throughput.

4. Local Setup Instructions
Create a virtual environment and install dependencies: pip install -r requirements.txt

Configure environment variables in a .env file: GEMINI_API_KEY=your_key_here

Start the FastAPI backend server: python entry.py

Launch the Streamlit frontend: streamlit run frontend/streamlit_app.py