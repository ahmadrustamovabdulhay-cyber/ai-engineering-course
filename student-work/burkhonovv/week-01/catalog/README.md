# (Session 01 endpoints and) Homework 02 - Customer Endpoint

## Run the application

Open a terminal in this catalog folder and run:

```powershell
python -m uvicorn main:app --reload
```

open http://127.0.0.1:8000/docs to test POST /customers.

## Test results

1. Missing city
   - Request: {"name": "Bobur"}
   - Status: 422
   - Response: {"detail":[{"type":"missing","loc":["body","city"],"msg":"Field required","input":{"name":"Bobur"}}]}

2. Missing name
   - Request: {"city": "Seoul"}
   - Status: 422
   - Response: {"detail":[{"type":"missing","loc":["body","name"],"msg":"Field required","input":{"city":"Seoul"}}]}

3. Empty name
   - Request: {"name": "", "city": "Seoul"}
   - Status: 422
   - Response: {"detail":[{"type":"string_too_short","loc":["body","name"],"msg":"String should have at least 1 character","input":"","ctx":{"min_length":1}}]}

4. Valid customer
   - Request: {"name": "Bobur", "city": "Seoul"}
   - Status: 201
   - Response: {"id": 9, "name": "Bobur", "city": "Seoul"}

``` Valid product — Session 01
   - Request: {"name": "Bicycle Turbo 575", "price": 799, "category": "Sports"}
   - Status: 201
   - Response: {"id": 4, "name": "Bicycle Turbo 575", "price": 799, "category": "Sports"} ``` # from session 01


## Answers to the 4 questions:


### Where do name and city come from?
They are entered by the client/user and CustomerCreate chacks that data validity before letting the function recive it. 

### Which checks does Pydantic perform?
Pydantic checks that both fields are given and that they are strings and meet the length requirements. If they do fit, it responses with 422 error/status code

### Why does the server generate the ID?
The server generates id to give each user a uniqe identifier to prevent future conflicts. Counter starts from 1 and each time the customer id is given to someone, the new_id is increased by 1.

### What happens when the server restarts?
When the server restarts, it forgets all the customers stored in memory, but if the page is reloaded on the browser, the data does not get cleared.
