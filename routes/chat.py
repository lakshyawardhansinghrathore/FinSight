import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from langchain_huggingface import HuggingFaceEmbeddings
from vectorstore.chroma_db import Retriever
from langchain_google_genai import ChatGoogleGenerativeAI

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    company: str | None = None
    year: int | None = None

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        # Initialize retriever
        retriever = Retriever(embeddings=embeddings)

        # Retrieve relevant context
        context = ""
        docs = retriever.invoke(
            query=request.question,
            company=request.company,
            year=request.year
        )
        
        context = "\n\n".join(doc.page_content for doc in docs)

        # Build chat prompt – include retrieved context and the user question
        prompt = f"You are an expert financial analyst. Use the following context from corporate reports to answer the user's question. If the context does not contain relevant information, politely indicate that you do not have enough data.\n\nContext:\n{context}\n\nUser Question: {request.question}\n\nAnswer:"

        llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_CHAT_MODEL", "gemini-3.6-flash"),
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0
        )
        
        response = llm.invoke(prompt)
        answer = response.content
        
        if isinstance(answer, list):
            texts = []
            for block in answer:
                if isinstance(block, dict) and "text" in block:
                    texts.append(block["text"])
                elif isinstance(block, str):
                    texts.append(block)
                else:
                    texts.append(str(block))
            answer = "".join(texts)
        elif not isinstance(answer, str):
            answer = str(answer)

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
