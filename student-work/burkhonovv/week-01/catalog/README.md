# (Session 01 endpoints and) Homework 02 - Customer Endpoint

## Run the application

Open a terminal in this catalog folder and run:

```powershell
python -m uvicorn main:app --reload
```

open http://127.0.0.1:8000/docs to test POST /customers.

## Test results

1. First valid customer
   - Request: {"name": "Abdulloh", "city": "Namangan"}
   - Status: 201
   - Response: {"id": 1, "name": "Abdulloh", "city": "Namangan"}

2. Second valid customer
   - Request: {"name": "Muhammad", "city": "Namangan"}
   - Status: 201
   - Response: {"id": 2, "name": "Muhammad", "city": "Namangan"}

3. Missing name
   - Request: {"city": "Namangan"}
   - Status: 422
   - Response message: "Field required" for name.

4. Empty name
   - Request: {"name": "", "city": "Namangan"}
   - Status: 422
   - Response message: "String should have at least 1 character" for name.

5. Empty city
   - Request: {"name": "Muhammad", "city": ""}
   - Status: 422
   - Response message: "String should have at least 1 character" for city.

6. Name longer than 100 characters
   - Request: {"name": "Abu Abdulloh Muhammad ibn Ismoil ibn Ibrohim ibn al-Mug‘iyra ibn Bardizba al-Jo‘fiy al-Buxoriyning muxlisi", "city": "Namangan"}
   - Status: 422
   - Response message: "String should have at most 100 characters" for name.

7. Third valid customer after rejected requests
   - Request: {"name": "Hamidulloh Burhon", "city": "Namangan"}
   - Status: 201
   - Response: {"id": 3, "name": "Hamidulloh Burhon", "city": "Namangan"}
```
```

## Answers to the 4 questions:


### Where do name and city come from?
They are entered by the client/user and CustomerCreate checks that data validity before letting the function recieve it. 

### Which checks does Pydantic perform?
Pydantic checks if both fields are given and if they are strings meeting the length requirements. If they do not fit, it responses with 422 error/status code

### Why does the server generate the ID?
The server generates id to give each user a unique identifier to prevent future conflicts. Counter starts from 1 and each time the customer id is given to someone, the next_customer_id is increased by 1.

### What happens when the server restarts?
When the server restarts, it forgets all the customers stored in memory, but if the page is reloaded on the browser, the data does not get cleared.
