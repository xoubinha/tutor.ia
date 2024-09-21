# tutor.ia.
Asistente virtual diseñado para mejorar el proceso de estudio mediante el uso de inteligencia artificial generativa.

## Overview

This project is a FastAPI application designed with the following endpoints:

- **Health Check Endpoint**: Verifies that the application is running correctly.
- **Conversation Endpoint**: Accepts a string (`prompt`) from the user and a `conversation_id`.

## Repository Structure

Here's the structure of the repository:

```
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── health.py
│   │       └── conversation.py
│   └── schemas/
│       ├── __init__.py
│       └── conversation.py
├── pyproject.toml
├── .gitignore
└── README.md
```

### Description of Each Folder and File

- **app/**: The main application directory.
  - **__init__.py**: Indicates that `app` is a Python package.
  - **main.py**: The entry point of the application where the FastAPI instance is created.
  - **api/**: Contains the API-related code.
    - **__init__.py**: Indicates that `api` is a Python package.
    - **endpoints/**: Contains the route handlers.
      - **__init__.py**: Indicates that `endpoints` is a Python package.
      - **health.py**: Defines the health check endpoint.
      - **conversation.py**: Defines the conversation endpoint.
  - **schemas/**: Contains the Pydantic models for request and response validation.
    - **__init__.py**: Indicates that `schemas` is a Python package.
    - **conversation.py**: Contains the data models for the conversation endpoint.
- **pyproject.toml**: Lists all the dependencies required for the project.
- **.gitignore**: Specifies intentionally untracked files to ignore.
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

### Running the Application

Start the application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The application will be accessible at `http://localhost:8000`.

## API Endpoints

### 1. Health Check Endpoint

- **URL**: `/health/`
- **Method**: `GET`
- **Description**: Checks if the application is running.
- **Response**:

  ```json
  {
    "status": "OK"
  }
  ```

### 2. Conversation Endpoint

- **URL**: `/conversation/`
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

FastAPI provides interactive documentation:

- Open your browser and navigate to `http://localhost:8000/docs` for Swagger UI.
- Alternatively, use `http://localhost:8000/redoc` for ReDoc documentation.

## Contributors
- [Christian](https://twitter.com/ccarballolozano)
- [Sara](https://twitter.com/sara_sanluis)

If you'd like to contribute to this repository by adding more demo projects or improving existing ones, feel free to fork the repository, make your changes, and submit a pull request explaining your changes. We welcome contributions from the community!

## Disclaimer
This project is provided as-is with no warranty or guarantee of its performance or results. Use at your own risk.