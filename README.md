# Project: Laptop Recommendation System

## Overview
This project is a **Laptop Recommendation System** that leverages AI and a structured database to provide users with tailored laptop suggestions based on their requirements and use cases. It features:

- A chatbot interface for user interaction.
- Database integration for storing and retrieving laptop information.
- Customizable chat UI components.

## Features
- **Chatbot Integration**: An AI-driven chatbot specializes in understanding user queries and providing structured recommendations.
- **Database-Backed Recommendations**: Uses MongoDB and ChromaDB to store and fetch laptop details.
- **Logging**: Maintains INFO, ERROR, and WARNING logs.
- **Engaging Chat**: Holds a engaging flow in the conversation with the user by asking them about their budget, preffered brand, or any specific features automatically.
- **Multilingual**: Supports multiple languages e.g, Urdu and Pashto.
- **Customizable UI**: Dynamic React components for buttons and cards to enhance the user interface.
- **FastAPI Backend**: Handles API requests and provides streaming responses for an engaging user experience.

## File Structure

### Project Structure
```
├── .git
├── chromadb
├── data
├── env
├── frontend
├── src
│   ├── __pycache__
│   ├── chat_history.py
│   ├── chatbot.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── logs.log
│   ├── main.py
├── .env
├── .gitignore
├── config.py
├── Dockerfile
├── README.md
├── requirements.txt
```

### Backend
- **`main.py`**: Entry point for the FastAPI server, handling API routes and middleware.
- **`chatbot.py`**: Contains the core chatbot logic to generate recommendations and interact with the database.
- **`chat_history.py`**: Handles saving and retrieving chat history from MongoDB.
- **`embeddings.py`**: Manages the creation and retrieval of document embeddings for the ChromaDB database.
- **`chunking.py`**: Splits large text data into smaller chunks for better processing.

### Frontend
- **`Button.jsx`**: Customizable button component with multiple styles and sizes.
- **`Card.jsx`**: Card component for displaying structured data.
- **`ChatCustomizer.jsx`**: A component to customize the chatbot's appearance and functionality.

### Logs
- **`logs.log`**: A log file for tracking API requests and debugging issues.

## Installation

### Prerequisites
1. Python 3.10 or higher.
2. Node.js and npm.
3. MongoDB database.
4. OpenAI API key.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/YusraSaeed/CI-Project-Final.git
   cd CI-Project-Final
   ```

2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

4. Set up the `.env` file with the required environment variables:
   ```plaintext
   MONGODB_URI=<your-mongodb-uri>
   OPENAI_API_KEY=<your-openai-api-key>
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

6. Start the frontend server:
   ```bash
   npm start
   ```

## Usage

1. Access the chatbot via the frontend UI.
2. Ask questions about laptops or provide your use case, and the chatbot will recommend suitable laptops based on stored data.

## Key Features Explained

### Chatbot
- Uses OpenAI GPT model for natural language understanding.
- Context-aware responses tailored to user preferences and requirements.

### Database
- **MongoDB**: Stores chat history and user interactions.
- **ChromaDB**: Efficiently handles laptop metadata and embeddings for quick search.

### Frontend Components
- **Button.jsx**: Provides a reusable button with multiple styles.
- **Card.jsx**: Displays laptop details in a clean, structured layout.
- **ChatCustomizer.jsx**: Allows users to personalize the chatbot interface.

## Authors
- **Yusra Saeed**
- **Wali Akbar Khan**

## Feedback
For feedback, suggestions, or issues, please reach out via email or create an issue on the repository.

## Contributing
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes and push:
   ```bash
   git commit -m "Add new feature"
   git push origin feature-branch
   ```
4. Create a Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- **OpenAI**: For providing the GPT model.
- **MongoDB**: For the database services.
- **React**: For building the user interface.

---

For further queries or contributions, feel free to reach out!
