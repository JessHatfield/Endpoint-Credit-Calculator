# Orbital Witness Backend Engineering Task - Copilot Usage Endpoint


## My Solution

I've used FastAPI to build an endpoint to calculate usage of Orbital Copilot. 

This my first time using FastAPI, I chose to use it here:
- Orbital Witness already use FastAPI in their tech stack
- Django felt like overkill, it would bring more complexity without extra benefit (plus performance hits as Django DRF doesn't have proper async support)
- I wanted to learn more about the framework and get some experience building with it


What did I focus on?

We had limited time to complete this exercise so my focus was mainly on

- Getting key behaviours under


What steps did I take to ensure the data we provide is accurate

I've used decimals to store credit costs to avoid floating point errors

I've ensured our tests cover each step of the API call:

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

- We've sent requests manually to our API to spot exceptions and confirm 

- I've written a quick integration test to confirm that all message_ids from the /messages/current-period endpoint are present in our endpoints output




Notes r.e. the usage structure. Our keys match the specification, the key order does not. I've confirmed with the engineering team that this is not an issue