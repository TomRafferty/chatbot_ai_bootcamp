import streamlit as st  
from openai import OpenAI  
  
st.title("💬 Chatbot")  
st.write(  
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "  
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "  
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."  
)  
  
openai_api_key = st.text_input("OpenAI API Key", type="password")  
  
if not openai_api_key:  
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")  
else:  
    client = OpenAI(api_key=openai_api_key)  
  
    if "messages" not in st.session_state:  
        st.session_state.messages = []  
  
    for message in st.session_state.messages:  
        with st.chat_message(message["role"]):  
            st.markdown(message["content"])  
  
    if prompt := st.chat_input("What is up?"):  
        st.session_state.messages.append({"role": "user", "content": prompt})  
        with st.chat_message("user"):  
            st.markdown(prompt)  
  
        stream = client.chat.completions.create(  
            model="gpt-3.5-turbo",  
            messages=st.session_state.messages,  
            stream=True,  
        )  
  
        response_text = ""  
        with st.chat_message("assistant"):  
            message_placeholder = st.empty()  
            for chunk in stream:  
                chunk_message = chunk.choices[0].delta.get("content", "")  
                response_text += chunk_message  
                message_placeholder.markdown(response_text)  
  
        st.session_state.messages.append({"role": "assistant", "content": response_text})  