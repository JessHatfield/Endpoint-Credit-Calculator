# Orbital Witness Backend Engineering Task - Copilot Usage Endpoint


## About My Solution

I've used FastAPI to build a small service to calculate usage costs for the Orbital Copilot product. 

This my first time using FastAPI, I chose to use it here:
- Orbital Witness already use FastAPI in their tech stack and I wanted to get more experience with
- Django and DRF would have brought extra complexity without extra benefit
- FastAPIs native pydantic support means it was easy to create a response structure that matches the spec

Overall I really enjoyed this exercise, after about 30 minutes of planning time I was able to build and test the whole project in about 3 hours 40 mins!

My solution implements the required logic in a testable, easy to read manner and returns accurate result very quickly

### Decisions worth highlighting:

- To keep response times low I decided to fetch data from external endpoints asynchronously
- I utilised a strategy pattern to keep our message cost calculator logic extensible/readable/testable
- I tried to keep as much of the application under unit tests as possible, taking care to cover a wide range of states
- To keep the build process smooth I took a test driven approach, building tests first and then writing logic to pass
- I wrote a short integration test and used this to flush out exceptions, confirm no messages where missed by our endpoint and indirectly test our logic fetching messages and reports
- I used decimals to represent credit_cost rather than floating points in order avoid a host of accuracy errors!
- I've allowed the application to fail with a 500 code if unexpected errors occur, it's better to give no usage cost vs an incomplete usage cost


### Things I would have added with a little more time:

- Unit testing the code that requests messages and reports
- Sticking the application in Docker to save you time on set up

### What steps did I take to ensure the data we provide is accurate

I've tried to ensure each step in the usage endpoint call was covered by some type of test:

  - We've got an endpoint test mocking our logic to fetch data and calculate message costs.
    - This confirms the general flow of execution works and that the response matches the schema
    - We use mocks covering each type of message
       - Regular Copilot messages
       - Report requests we could fetch costs for
       - Report requests which could not be found


  - Our message cost calculator is heavily tested
      - We test each rule individually across a few cases
      - We've tested that our message cost calculator can run multiple rules correctly
      - We've tested that our calculator produces the correct result against a real message
  

  - I spot checked a couple of usage results to confirm they had the correct cost


  - I've also written a quick integration test to confirm that all messages from the /messages/current-period endpoint are present in our endpoints output


## Getting Started

Here are instructions for setting this project up via the terminal

Alternatively you might prefer to import the project directly from GitHub via your ide of choice (I'm using pycharm)

1. Clone the repository:
    ```shell
    git clone https://github.com/JessHatfield/Endpoint-Credit-Calculator
    cd Endpoint-Credit-Calculator
    ```

2. Install requirements 
    ```shell
    python -m venv .venv
    source .venv/bin/activate
    pip install --no-cache-dir -r requirements.txt
    ```

3. Run our tests
    ```shell
    pytest /app/tests
    ```

4. Run our server
    ```shell
    python -m uvicorn app.main:app --reload
    ```

5. Fetch usage data
    
    Via curl
    ```shell
    curl -H -i http://127.0.0.1:8000/tech-task/usage/
    ```
    Via pycharm -> Double click test_main.http








