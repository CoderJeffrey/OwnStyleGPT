import streamlit as st
import os
import sys

import constants
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

from langchain.chat_models import ChatOpenAI

# os.environ['OPENAI_API_KEY'] = constants.OPENAI_API_KEY


# 1. Load the document and vectorize it
def get_answer(questio_text):
    loader = TextLoader("previous_text.txt")
    index = VectorstoreIndexCreator().from_loaders([loader])

    additional_text = " Using the writing style of the previous text. And use the context around the paper. Write like me."

    # use ChatOpenAI to get the answer if it is not within the document
    ans = index.query(questio_text + additional_text, llm = ChatOpenAI())

    return ans

# 5. Build an app with streamlit
def main():
    # set the page title as Custom Write Assistant and page icon as a robot
    st.set_page_config(
        page_title="Custom Write Assistant", page_icon=":robot_face:")

    st.header("Custom Write Assistant :robot_face:")
    # a sliding window of 5 text box that i can click right or left to switch between them
    # each of them is a text box

    # a small textbox that ask for the OpenAI API key from the user
    openai_api_key = st.text_input("OpenAI API Key")

    if openai_api_key:
        os.environ['OPENAI_API_KEY'] = openai_api_key

     # a small textbox that ask for the Undetectable AI API key from the user (optional)
    undetectable_ai_api_key = st.text_input("Undetectable AI API Key (optional)")

    # text box for the previous text with the maximum of 5000 characters
    text1 = st.text_area("An articile/homework you wrote. (Preferrable a paper similar to the one you want to write)", max_chars=5000)

    # text box for the context text regarding your paper (can list as bullet points)
    context_text = st.text_area("Context of your paper (can list as bullet points)", max_chars=1000)

    # text box for the question
    question = st.text_area("What is the question you want to answer?")

    if openai_api_key and text1 and context_text and question:
        # Write the text1, text2, text3 to a txt file named "previous_text.txt" seperated by a new line
        with open("previous_text.txt", "w") as f:
            f.write(" previous text" + text1 + "\n")
            f.write(" the context aroudn the paper to be written " + context_text + "\n")
        
        # load the text file and vectorize it
        answer_txt = get_answer(question)

        st.write("Generating best practice message...")

        result = answer_txt

        st.info(result)


if __name__ == '__main__':
    main()
