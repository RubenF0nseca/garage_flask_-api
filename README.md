
# Garage API

This guide explains how to install and configure the **Garage API** project. Follow the steps below to set up the project on your local machine.

## Installation

To install and configure the Garage API, follow these steps:

1. **Clone the repository:**  
   Download the repository to your local machine by running the following command in your terminal:
   ```bash
   git clone https://github.com/nacsantos/garage_flask_api.git
   ```

2. **Navigate to the project directory:**  
   After cloning the repository, move to the project directory:
   ```bash
   cd garage_flask_api
   ```

3. **Create and activate a virtual environment:**  
   To isolate the project dependencies, create a virtual environment. Use the following commands:  
   - For Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - For Windows:
     ```bash
     python3 -m venv venv
     venv\Scripts\activate
     ```

4. **Install the dependencies:**  
   With the virtual environment active, install the required packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**  
   To verify that the installation is successful, start the Flask application:
   ```bash
   flask run
   ```
   The application will be available at:
   ```
   http://127.0.0.1:5000/api
   ```

## Accessing the Swagger Documentation

To access the Swagger documentation, start the Flask application and navigate to the following URL in your browser:
```
http://127.0.0.1:5000/api/docs
```

The Swagger interface allows you to:
- Explore all API endpoints and models.
- Perform test calls to the API.
- Review parameters and expected responses.

The Swagger documentation is a valuable tool for developers, enabling seamless interaction with the API while improving productivity and ensuring code quality.

---

By following these steps, you will have the **Garage API** up and running on your local machine. If you encounter any issues, please check the repository or submit an issue.
