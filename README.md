# Orbital Witness Backend Engineering Task - Copilot Usage Endpoint


## About My Solution

I've used FastAPI to build an endpoint to calculate usage costs for the Orbital Copilot product. 

This my first time using FastAPI, I chose to use it here:
- Orbital Witness already use FastAPI in their tech stack and I wanted to get more experience with
- Django felt like overkill, it would bring more complexity without extra benefit
- FastAPIs pydantic support means it was easy to create a response structure that matches the spec
- 

I really enjoyed this exercise, after about 30 minutes of planning time I was able to build and test the whole project in about 3 hours 40 mins!

My solution implements the required logic in a testable, easy to read manner and returns accurate result very quickly.

### Decisions worth highlighting:

- To keep response times low I decided to fetch data from external endpoints asynchronously
- I utilised a strategy pattern to keep our message cost calculator logic extensible/readable/testable
- I tried to keep as much of the application under unit tests as possible, taking care to cover a wide range of states
- To keep the build process smooth I took a test driven approach, building tests first and then writing logic to pass
- I wrote a short integration test and used this to flush out exceptions, confirm no messages where missed by our endpoint and indirectly test our logic fetching messages and reports
- I used decimals to represent credit_cost rather than floating points in order avoid a host of accuracy errors!


### Things I would have added with more time:

- Placing the logic calling the messages and reports endpoint under unit test
- Machine-readable logs and a sentry integration
- Caching on the function fetching report information

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


  - I've written a quick integration test to confirm that all messages from the /messages/current-period endpoint are present in our endpoints output


## How To Run My Project







