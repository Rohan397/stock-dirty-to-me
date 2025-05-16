#What it does 

This provides a programmatic interface with which to ask questions on a publically traded company's most recent earnings reports

#How it works 

This program uses a RAG pipeline and a chroma vector DB to query the stock the user asks for, retrieve the information, chunk and store 
it in a vector DB and then allow the user to query for information.

#How to run locally

To run locally: 
- create a virtual environment `python3 -m venv venv` 
- run `pip install -r requirements.txt`
- run `python3 main.py`
- follow the instructions!