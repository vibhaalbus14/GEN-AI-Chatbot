from dotenv import load_dotenv,find_dotenv
from langchain_groq import ChatGroq
import os
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (FewShotPromptTemplate,PromptTemplate)
from langchain.chains import LLMChain
from fastapi import FastAPI,Path,Body
from typing import Optional,Union
from pydantic import BaseModel 
import logging
import uvicorn

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    model=ChatGroq(model="mixtral-8x7b-32768",api_key=os.getenv("GROQ_API_KEY"),temperature=0.3)
    logging.info("model initialized successfully")
except Exception as e:
    logging.error(f"ChatBot model not initialized : {e}")
    model=None

my_memory=ConversationBufferMemory(memory_key="memory_chain")
my_prompt='''you are a data structure and algorithms(DSA)  tutor .Guide the students appropriately in necessary
                languages.
                {memory_chain}
              question={question}  
            '''

my_prompt_overall=PromptTemplate(input_variables=['memory_chain','question'],
                         template=my_prompt)
chain=LLMChain(
        llm=model,
        memory=my_memory,
        prompt=my_prompt_overall,
        verbose=True
)
#user_input="what is a mongoose?"
#chain.predict(question=user_input)

app=FastAPI()

class PromptClass(BaseModel):
    prompt:Optional[str]=None

@app.get("/")
def intro():
    return{"Heyyyyyy there!!":"I'm Peachy the chatbot ;)"}

@app.post("/ask")
def ask_model(promptClass:PromptClass=Body(...,title="I'm Peachy!",description="Enter your query here")):
    if promptClass.prompt is None:
        return{"From Peachy":"How can I help you today?"}
    if model is None:
        return{"Model not initialized."}
    try:
       
        response=chain.predict(question=promptClass.prompt)
    except Exception as e:
        logging.error(f"LLM Chain prediction error : {e}")
        return "Error occured during chain prediction."
    return {"response":response}
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

