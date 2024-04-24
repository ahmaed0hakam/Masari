import streamlit as st
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_core.output_parsers import StrOutputParser
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

# Define the Streamlit UI
st.title("🤖 AI Career Assistant")
st.subheader("Unlock Your Potential 🚀: Let's Craft Your Path to Success!🌟")

# Define the user input options
user_choice = st.radio("Choose an option:", ("Generate Learning Path", "Skillfy"))
user_title = st.text_input("Enter the title:")
uploaded_file = st.sidebar.file_uploader("Upload your resume", type=["pdf", "docx"]) # File uploader for resume

# Define the Ollama model and callback manager
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = Ollama(model="llama3", callbacks=callback_manager, verbose=True)
output_parser = StrOutputParser()

# Define the function to get response
def get_response(user_choice, user_title):
    if not user_title:
        st.write("Please enter a title.")
        return

    response = None
    if user_choice == "Generate Learning Path":
        response = llm.stream(f"Generate a learning path with only the names of courses for '{user_title}' learning path. list directly & don't forget you are building a learning path, so ordering courses is important.\
                                  DON'T SAY 'Here is a sample..', LIST THEM UNDER THESE CATEGORIES: Fundamental Courses, Intermediate Courses, Advanced Courses, Specialized Courses. Don't finish with note.")
    elif user_choice == "Skillfy":
        if uploaded_file:
            temp_file = "./temp.pdf"
            with open(temp_file, "wb") as file:
                file.write(uploaded_file.getvalue())

            st.sidebar.subheader("Resume Preview")
            loader = PyPDFLoader(temp_file)
            documents = loader.load_and_split()

            text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
            texts = text_splitter.split_documents(documents)
            response = llm.stream(f"Based on the user position inside resume, identify missing skills from the resume: '{texts}', tell him why, then for each skill/s generate lessons to learn and master these skills.")

    if response:
        st.write(response)

# Display the prompt and get response
if st.button("Submit"):
    st.spinner("Processing...")
    get_response(user_choice, user_title)
