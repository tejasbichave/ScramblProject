Project setup:

Step 1 : Install requirments.txt file in in Virtual Env
Command:
pip install -r requirements.txt

Step 2 : Go to the project repo
cd MyProject/

Step 3 :Run the Python local server
Command:
python manage.py runserver

User can test system API with postman

1.Get transaction with respect to transaction ID

URL: http://localhost:8000/assignment/transaction/{transaction_id}

Request Type: GET

2.Get transaction with respect to transaction ID

URL: http://localhost:8000/assignment/transactionSummaryByProducts/{last_n_days}

Request Type: GET

3.Get transaction with respect to transaction ID

URL: http://localhost:8080/assignment/transactionSummaryByManufacturingCity/{last_n_days}

Request Type: GET


