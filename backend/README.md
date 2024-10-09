# Tutor.ia.
An AI-powered virtual assistant designed to enhance the learning process through generative AI.


## Overview
This repository contains the backend of the Tutor.IA project, built using FastAPI. The backend is responsible for handling user conversations and health checks through a simple API structure. It provides two main endpoints:

- Health Check Endpoint: Ensures that the application is running smoothly.
- Conversation Endpoint: Accepts user input in the form of a prompt and a conversation_id for contextual responses.

## Repository Structure

The project follows this structure:

```
    ├── 📂 app/
    |       ├── 📂 api/
    |       │       ├── 📂 endpoints/
    |       |       │       ├── 📄 __init__.py
    |       |       │       ├── 📄 conversation.py
    |       |       │       ├── 📄 health.py
    |       ├── 📂 schemas/
    |       │       ├── 📄 __init__.py
    |       │       └── 📄 conversation.py
    |       ├── 📄 __init__.py
    |       ├── 📄 main.py/
    ├── 📄 pyproject.toml
    ├── 📄 .env.template.toml
    └── 📄 README.md
```

### Description of Each Folder and File

- **app/**: The core application directory
  - **__init__.py**: Indicates that `app` is a Python package.
  - **main.py**: Application entry point, where the FastAPI instance is created.
  - **api/**: Contains API-related code.
    - **__init__.py**: Indicates that `api` is a Python package.
    - **endpoints/**: Contains the route handlers.
      - **__init__.py**: Indicates that `endpoints` is a Python package.
      - **health.py**: Defines the health check endpoint.
      - **conversation.py**: Defines the conversation endpoint.
  - **schemas/**: Contains Pydantic models for request and response validation.
    - **__init__.py**: Indicates that `schemas` is a Python package.
    - **conversation.py**: Contains the data models for the conversation endpoint.
- **pyproject.toml**: Manages dependencies and project settings using Poetry.
- **.env.template**: Environment variables template for configuring the application
- **README.md**: Provides an overview and instructions for the project.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Poetry (Python package manager)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/xoubinha/tutor.ia.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd <your_project_path>
   ```

3. **Create a Virtual Environment and Install the Dependencies**

   ```bash
   poetry install
   ```

4. **Activate the Virtual Environment**

     ```bash
     poetry shell
     ```

### Set the environment variables

Environment variables are key-value pairs that are accessible to any program running within the environment in which they are set. These variables often contain sensitive information such as API keys, database credentials, or configuration settings. To set them up, just copy the `.env.template` file and make a new file called `.env`. Then, fill in the blanks with the appropiate info, each variable is explained in the below table:

| **Parameter**                               | **Description**                                                                                            |
|---------------------------------------------|------------------------------------------------------------------------------------------------------------|
| AZURE_OPENAI_ENDPOINT                       | Endpoint URL for the Azure OpenAI service instance.                                                        |
| AZURE_OPENAI_API_KEY                        | API key used to authenticate requests to the Azure OpenAI service.                                          |
| OPENAI_API_VERSION                          | Version of the OpenAI API to be used.                                                                      |
| AZURE_OPENAI_MODEL                          | Name of the OpenAI model to be used.                                                                       |
| AZURE_SEARCH_ENDPOINT                       | Endpoint URL for the Azure Search service instance.                                                        |
| AZURE_SEARCH_INDEX_NAME                     | Name of the Azure Search index to be used.                                                                 |
| AZURE_SEARCH_API_KEY                        | API key used to authenticate and authorize requests to the Azure Search service.                           |


### Running the Application

Start the application using Uvicorn from the `app` folder:

```bash
uvicorn main:app --reload
```

The application will be accessible at `http://localhost:8000`.

## API Endpoints

### 1. Health Check Endpoint

- **URL**: `/health`
- **Method**: `GET`
- **Description**: Checks if the application is running.
- **Response**:

  ```json
  {
    "status": "OK"
  }
  ```

### 2. Conversation Endpoint

- **URL**: `/conversation`
- **Method**: `POST`
- **Description**: Receives a `prompt` and a `conversation_id` from the user.
- **Request Body**:

  ```json
  {
    "prompt": "Your prompt here",
    "conversation_id": "conversation123"
  }
  ```

- **Response**:

  ```json
  {
    "response": "Processed prompt: Your prompt here"
  }
  ```


## Testing the Endpoints

### Using the Interactive API Docs
FastAPI provides built-in interactive documentation, available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Disclaimer
This project is provided as-is with no warranty or guarantee of its performance or results. Use at your own risk.