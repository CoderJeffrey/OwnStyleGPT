import streamlit as st
import os
import sys

import constants
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

from langchain.chat_models import ChatOpenAI

os.environ['OPENAI_API_KEY'] = constants.OPENAI_API_KEY
print(os.environ['OPENAI_API_KEY'])


# 1. Load the document
def get_answer(questio_text):
    loader = TextLoader("previous_text.txt")
    index = VectorstoreIndexCreator().from_loaders([loader])

    # 2. Ask a question
    topic = "how is Kanye West music?"

    # use ChatOpenAI to get the answer if it is not within the document
    ans = index.query(questio_text, llm = ChatOpenAI())

    return ans

# 5. Build an app with streamlit
def main():
    # set the page title as Custom Write Assistant and page icon as a robot
    st.set_page_config(
        page_title="Custom Write Assistant", page_icon=":robot_face:")

    st.header("Custom Write Assistant :robot_face:")
    # a sliding window of 5 text box that i can click right or left to switch between them
    # each of them is a text box

    text1 = st.text_area("A parapgraph of text you wrote")

    text2 = st.text_area("Another parapgraph of text you wrote")

    text3 = st.text_area("Final parapgraph of text you wrote")

    # text box for the question
    question = st.text_area("What is the question you want to answer?")

    if text1 and text2 and text3 and question:
        # Write the text1, text2, text3 to a txt file named "previous_text.txt" seperated by a new line
        with open("previous_text.txt", "w") as f:
            f.write(text1 + "\n")
            f.write(text2 + "\n")
            f.write(text3 + "\n")
        
        # load the text file and vectorize it
        answer_txt = get_answer(question)

        st.write("Generating best practice message...")

        result = answer_txt

        st.info(result)


if __name__ == '__main__':
    main()
