# Tutor.ia
An AI-powered virtual assistant designed to enhance the learning process through generative AI.

## Overview

This repository contains the code for creating the frontend for the Tutor.IA project. It is designed to create a chatbot user interface.

## Project Structure

This section provides an overview of the directory structure for the Tutor.ia frontend project.

```
    📦 frontend/
    ├── 📂 public/
    ├── 📂 src/
    │    ├── 📂 api/
    │    ├── 📂 assets/
    │    ├── 📂 components/
    │    ├── 📂 pages/
    │    ├── 📂 util/
    │    └── 📄 index.css
    │    └── 📄 index.tsx
    ├── 📄 index.html
    ├── 📄 package.json
    ├── 📄 vite.config.ts
```

- **public/**: Contains static files that are served directly, such as images and icons.
- **src/**: Main source code directory for the application.
    - **api/**: Houses the code for interacting with backend APIs.
    - **assets/**: Contains static assets such as images and fonts used in the project.
    - **components/**: Contains reusable UI components for building the frontend.
    - **pages/**: Houses different page components that make up the application's views.
    - **util/**: Includes utility functions and helpers used throughout the project.
    - **index.css**: Main stylesheet for the application, defining global styles.
    - **index.tsx**: The entry point of the React application, rendering the main component.
- **index.html**: The main HTML file for the application, serving as the template for the frontend.
- **package.json**: Manages project dependencies and scripts for building and running the application.
- **vite.config.ts**: Configuration file for Vite, the build tool used in the project.

## Getting started 

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/xoubinha/tutor.ia.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd frontend
   ```

3. **Install the Dependencies**

   ```bash
   npm install
   ```

4. **Run the application**

     ```bash
     npm run dev
     ```
The application will be accessible at `http://localhost:5173`.

## Disclaimer
This project is provided as-is with no warranty or guarantee of its performance or results. Use at your own risk.