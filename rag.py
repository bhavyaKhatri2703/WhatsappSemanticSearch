from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
import os

import dotenv
dotenv.load_dotenv()

from langchain_core.callbacks.base import BaseCallbackHandler

class TerminalStreamCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(token, end='', flush=True)



def getDocs(chunks):
    docs = [Document(page_content=chunk) for chunk in chunks]
    return docs

def build_vectorStore(docs,persist_path = "faiss_db"):
    embeddings  = OpenAIEmbeddings()

    if os.path.exists(persist_path):
        return FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)
    
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(persist_path)
    return vectorstore

    
def build_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    template = """
You are a bot that understands people conversations in a specific groupchat.
You will be provided context as conversations and answer the question based on the context.
Be a bit casual in answering the question. Treat everything as past.

context: {context}
question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(model_name="gpt-4o-mini",streaming=True, temperature=0, callbacks=[TerminalStreamCallbackHandler()])
    return (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )