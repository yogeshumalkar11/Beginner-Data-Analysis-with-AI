import os
import pandas as pd
import streamlit as st
from secret import openapi_key
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain.callbacks import get_openai_callback

os.environ['OPENAI_API_KEY'] = openapi_key

st.set_page_config(page_title="Data Analysis with AI", page_icon=None, layout="wide", initial_sidebar_state="auto",
                   menu_items=None)
st.title("Data Analysis with AI")
st.markdown("Performs basic data analysis with help of only **Pandas Library**.")


def main():
    st.sidebar.subheader("CSV file")
    csv = st.sidebar.file_uploader('Upload a CSV file:', type='csv')
    if csv is not None:
        df = pd.read_csv(csv)
        st.sidebar.write("Uploaded CSV file Successfully!")
        st.subheader("CSV File Details")
        st.write("First 5 rows in the CSV file:")
        st.dataframe(df.head(5))
        with st.expander("View complete CSV file"):
            st.dataframe(df)
        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
            df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )
        st.subheader("Query and Response")
        query = st.text_input("Enter your Query:")
        st.write("Response:")
        if query:
            with get_openai_callback() as cb:
                response = agent.run(query)
                print(cb, "\n")
            st.write(response)
    else:
        st.markdown("*Please Upload a CSV file*")


if __name__ == "__main__":
    main()
