import os
import streamlit as st #custom, interactive web applications
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

LLM_PROVIDER=os.getenv("LLM_PROVIDER","openai")


prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a NEET AI Agent that generates a mock assignment with four levels of difficulty: "
            "Easy, Medium, Hard, Expert. The assignment must be related to the given topic and subject "
            "(Biology, Physics, Chemistry). Each level should contain exactly one question, increasing "
            "in difficulty."),
        ("user","Generate an assignment on the topic '{topic}' under the subject '{subject}'."),
    ]
)

output_parser=StrOutputParser()

# set llm provider
def get_llm_provider():
    if LLM_PROVIDER=="openai":
        return ChatOpenAI(model=os.getenv("OPENAI_MODEL"),api_key=os.getenv("OPENAI_API_KEY"),temperature=0.8,)
    elif LLM_PROVIDER=="gemini":
        return ChatOpenAI(model=os.getenv("GEMINI_MODEL"),api_key=os.getenv("GEMINI_API_KEY"),temperature=0.8,)
    else:
        raise ValueError(f"Invalide LLM_PROVIDER: {LLM_PROVIDER}")

llm=get_llm_provider()
chain=prompt | llm | output_parser
    
    
st.title("Neet AI Assignment Generator")
input_subject=st.text_input("Enter the subject (e.g., Biology, Physics, Chemistry):")
input_topic=st.text_input("Enter the topic for the assignment:")

if st.button("Generate Assignment"):
    if not input_subject or not input_topic:
        st.error("Please provide both subject and topic")
    else:
         with st.spinner("Generating assignment..."):
             response=chain.invoke({"subject":input_subject,"topic":input_topic})
             st.success("Assignment Generated Successfully!")
             st.write(response) 



