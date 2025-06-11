import dotenv
dotenv.load_dotenv()

from clean import clean, parse_chat,chunk_messages
from rag import build_vectorStore, build_rag_chain,getDocs



def main():

    messages = parse_chat("output.txt")
    docs = getDocs(messages)
    vectorstore = build_vectorStore(docs)
    rag_chain = build_rag_chain(vectorstore)

    query = input("Question:")
    rag_chain.invoke(query)



if __name__ == "__main__" :
    main()



