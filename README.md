# Tutor.ia.
Asistente virtual diseñado para mejorar el proceso de estudio mediante el uso de inteligencia artificial generativa.

## Repository Structure

The repository is organized into several key directories, each responsible for a specific part of the system:

```
    📦 tutor.ia/
    ├── 📂 aisrch/
    ├── 📂 backend/
    ├── 📂 frontend/
    ├── 📂 process_docs/
    ├── 📄 .gitignore.
    └── 📄 README.md
```

- **aisrch/**: This folder contains the configuration and setup for integrating with Azure AI Search. It handles the creation and management of the AI search capabilities used in the project.
- **backend/**: Responsible for the backend of the chatbot API. This directory contains the logic for processing user queries, interacting with the AI, and managing the core functionalities of the virtual assistant.
- **frontend/**: Manages the front-end interface of the project, providing a user-friendly experience for interacting with the chatbot. All UI-related components and logic can be found here.
- **process_docs/**: This directory handles document processing, where files are processed to extract textual data. This content is used to fuel the chatbot’s knowledge base and provide contextual responses to user queries.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Poetry (Python package manager)
- Azure subscription
- Vite with React