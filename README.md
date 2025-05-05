# tabnews-scrapy-ia

## Overview

The `tabnews-scrapy-ia` application is designed to scrape content from specified URLs, process the data, and provide summarized results through a FastAPI interface. It leverages Scrapy for web scraping, FastAPI for building the API, and a custom AI summarization module to condense the content.

## Technologies Used

- **Python**: The core programming language.
- **Scrapy**: For web scraping.
- **FastAPI**: To create the API endpoints.
- **Pydantic**: For data validation.
- **Crochet**: To run Scrapy spiders in a non-blocking way.
- **dotenv**: For environment variable management.
- **Logging**: For logging application activities.

## API Endpoints

- **POST /get-by-urls**: Accepts a list of URLs to scrape and returns the summarized content.

## How to Run the Application

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yuripinheirot/tabnews-scrapy-ia
   cd tabnews-scrapy-ia
   ```

2. **Install Dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your API key:
   ```
   API_KEY=your_api_key_here
   ```

4. **Run the Application**:
   Start the FastAPI server:
   ```bash
   fastapi dev ./src/main.py
   ```

5. **Test the Application**:
   Use the client to test the API. You can use tools like `curl` or Postman to send a POST request to the `/get-by-urls` endpoint with a JSON body containing the URLs you want to scrape.

6. **Access the API Documentation**:
   Visit `http://127.0.0.1:8000/docs` to view the Swagger UI and test the endpoints interactively.

## Testing the Application

To test the application using the client:

1. **Navigate to the Client Directory**:
   ```bash
   cd client
   ```

2. **Open `index.html` in a Browser**:
   This file provides a simple interface to interact with the API.

3. **Enter URLs and Submit**:
   Input the URLs you wish to scrape and click the submit button to see the results.

## Additional Information

- **Logging**: The application logs important events and errors, which can be found in the console output.
- **Error Handling**: The application handles errors gracefully and returns appropriate HTTP status codes and messages.
