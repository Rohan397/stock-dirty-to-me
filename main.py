from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import get_retriever, process_document, initialize_vectore_store
from edgar import download_latest_filing


model = OllamaLLM(model="llama3.2")

template = """
You are an expert in anaylzing financial statements. Answer the questions in 2-3 sentences, using the information provided in the financial statements.

Here are the relevant financial statements: {statements}

Here is the question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model
seen = {}
vector_store = initialize_vectore_store()


print("Hi! I'm EDGAR! I can help you analyze stocks and companies!")

while True:
    print("\n----------------------------\n")
    next_step = input(
        "Do you want me to:\n - analyze a new stock (type search)\n - answer a question about a stock I've already read up on (type ask)\n - quit (type quit)\n response: "
    )
    if next_step == "quit":
        break
    elif next_step == "search":
        ticker = input("enter the ticker for the stock you want me to analyze: ")
        if seen.get(ticker):
            print("I've already read up on this!")
        else:
            seen[ticker] = True
            filename = download_latest_filing(ticker)
            if filename == "No filings found":
                print("No filings found for this ticker")
                continue
            process_document(filename, vector_store)
    elif next_step == "ask":
        question = input("Ask me your question here: ")
        retriever = get_retriever(vector_store)
        statements = retriever.invoke(question)
        result = chain.invoke({"statements": statements, "question": question})
        print(result)
    else:
        print("I don't know what to do with that, let me take you back to the options.")
    # else:
print("Bye!")
