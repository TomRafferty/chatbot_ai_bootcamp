import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.title("💬 Chatbot")  
  
openai_api_key = "o2Mwk7oNN90NNgONc2HCTY4sAEPJyBekxSz45Q4aAZVmcnnDdtrBJQQJ99BGACmepeSXJ3w3AAAAACOG0CfP"  

if "chat_history" not in st.session_state:
    #initialize an empty chat history
    st.session_state.chat_history = []

for chat_msg in st.session_state.chat_history:
    #iterrate over the chat history and display each message using .chat_message
    st.chat_message(chat_msg["role"]).write(chat_msg["content"])


#creates a chat input widget using st.chat_input
user_input = st.chat_input("Hi there! how can I assist you today?")
if user_input:
    #append the new message to the chat history and display it
    st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
    st.chat_message("user").write(user_input)

    #initializing AzureChatOpenAI with appropriate params
    llm = AzureChatOpenAI(  
        azure_endpoint="https://hmrcmu-ai-training-uk-o-resource.cognitiveservices.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2025-01-01-preview",  
        api_version="2025-01-01-preview",  
        deployment_name="gpt-4.1-mini",  
        api_key="o2Mwk7oNN90NNgONc2HCTY4sAEPJyBekxSz45Q4aAZVmcnnDdtrBJQQJ99BGACmepeSXJ3w3AAAAACOG0CfP"  
    )

    #create a ChatPromptTemplate with system and human messages
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "you are a cringe tiktok influencer who attempts to help but is always completely wrong and unhelpful"),
        ("human", "{user_message}")        
    ])  

    #creating the chain for prompt template to llm to StrOutputParser
    chain = prompt_template | llm | StrOutputParser()

    #invoking the chain with user input to get response
    response = chain.invoke({
        "user_message": user_input
    })

    if response:
        #append the response to the chat history and display it
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        st.chat_message("assistant").write(response)