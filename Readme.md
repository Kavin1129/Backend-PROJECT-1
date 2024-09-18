
# Data Uploading and Retrieval Using ElasticSearch And FastAPI

This project is done for a job recruitment task, and the overall objective is to create a backend where news articles need to be scraped periodically, stored, and fetched efficiently using caching

## Task
* A backend for the retrieval of the documents. You are allowed to use any programming language. But, try to stick with Python/Go.
* The documents need to be stored in a database. You are free to use any encoders of your choice.
* You are required to cache the responses for ensuring faster retrieval (choose the most optimal method for caching, to improve the performance of the entire system. E.g. something like memcached may not be the best for this use case. Choose the best method of caching for this scenario and document your reasonings in the README.md file).
* There should be a background as soon as the server starts a different thread will start and scrape different news articles.
* Build a backend for this, with the following endpoints:
* /health - simply returns a random response for checking if the API is active.
* /search - this would return a list of top results for the query made by the client, it should be able to accept the below specified parameters. It should always be a default value, in case it’s not specified in the request.
* text: the prompt text.
* top_k: # of results to be fetched
* threshold: threshold for the similarity score.
* Dockerize the application and serve it.
* The request must have a `user_id`, if this user is already present in the database, the frequency of the API calls for the user must be incremented by 1. Else, create an entry and it should be assigned as 1.
* In case, this user makes more than 5 requests, it should throw HTTP 429 status code.
* Also, record inference time for each request, and preferably add API logging for good practices.
## API Reference

#### Get 

```http
  GET /health
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `No Parameter` | `-` | `-` |

#### Post

```http
  POST /search
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user_id`      | `Integer` | **Required**. Id of User |
| `text`      | `String` | **Required**. Text to search |
| `top_k`      | `Integer` | **Optional**.  Number of results to return (default: 10) |
| `threshold`      | `Float` | **Optional**. Minimum similarity threshold (default: 0.5) |



## Screenshots

![Screenshot 2024-09-18 130209](https://github.com/user-attachments/assets/6ce291b7-d592-4af9-bdc1-f4097abf38d0)

![{EAC439CF-907D-4BEE-9920-29BEB83E2ED3}](https://github.com/user-attachments/assets/47431853-7bf6-46c6-98df-3f738328a43a)
## Installation

Clone My Repo
```bash
git clone https://github.com/Kavin1129/Backend-PROJECT-1.git
```
Install all the requirements
```bash
pip install -r requirements.txt
```

Before Running the application Download Elasticsearch and run the Application (Elasticsearch) using terminal.
    
## Issue With Overall Application

* **Text Parameter Limitation:** The text parameter only accepts a single string, not a list of strings or strings containing spaces. This limits search flexibility.
* **Missing API Logging:** API request/response logging has not been implemented, which is essential for monitoring and debugging.
* **Case Sensitivity in Text Search:** The text parameter is case-sensitive, so if a user searches for "hello" and the article contains "Hello," the system will not return the article. This limits search accuracy.
* **Caching:** While Elasticsearch is used for indexing and searching, it is not a caching solution. To improve performance, we could use Redis for caching on top of Elasticsearch to reduce the load and speed up retrieval times for frequently searched queries.
* **Dockerize:** did not Dockerize the application.

**Feel Free to Clone and Improve the overall Application**
