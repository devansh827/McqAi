import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# Loading json file 
with open(r'C:\Users\devan\OneDrive\Desktop\MCQ-dev\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# Set page config
st.set_page_config(page_title='MCQ Generator', page_icon='📝', layout='wide')

# Creating a title for the app
st.title('📝 MCQ Generator Application with Langchain')

st.markdown("""
    <style>
        .stForm {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stAlert {
            padding: 20px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .stTable thead th {
            background-color: #4CAF50;
            color: white;
        }
        .stTable tbody tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .stTable tbody tr:hover {
            background-color: #ddd;
        }
    </style>
""", unsafe_allow_html=True)

# Create a form using st.form
with st.form('user_inputs', clear_on_submit=True):
    st.header("📋 Upload Your File")
    uploaded_file = st.file_uploader('Upload a PDF or txt file', type=['pdf', 'txt'])

    st.header("🔧 Configure MCQ Generation")
    col1, col2 = st.columns(2)
    with col1:
        mcq_count = st.number_input('Number of MCQs', min_value=3, max_value=50, step=1, help="Select the number of MCQs to generate.")
    with col2:
        subject = st.text_input('Subject', max_chars=40, help="Enter the subject for the MCQs.")

    tone = st.text_input('Complexity Level of Questions', max_chars=20, placeholder='Simple', help="Enter the complexity level of the questions (e.g., Simple, Intermediate, Advanced).")

    st.header("📤 Submit to Generate MCQs")
    button = st.form_submit_button('Create MCQs')

    # Check if the button is clicked and all fields have input 
    if button:
        if uploaded_file is not None and mcq_count and subject and tone:
            with st.spinner('Generating MCQs, please wait...'):
                try:
                    text = read_file(uploaded_file)
                    # Count tokens and the cost of API call
                    with get_openai_callback() as cb:
                        response = generate_evaluate_chain(
                            {
                                'text': text,
                                'number': mcq_count,
                                'subject': subject,
                                'tone': tone,
                                'response_json': json.dumps(RESPONSE_JSON)
                            }
                        )

                except Exception as e:
                    st.error('An error occurred while generating the MCQs.')
                    st.error(f"Error details: {e}")
                    traceback.print_exception(type(e), e, e.__traceback__)
                else:
                    st.success('MCQs generated successfully!')

                    # st.write(f"**Total Tokens:** {cb.total_tokens}")
                    # st.write(f"**Prompt Tokens:** {cb.prompt_tokens}")
                    # st.write(f"**Completion Tokens:** {cb.completion_tokens}")
                    # st.write(f"**Total Cost:** ${cb.total_cost:.2f}")

                    if isinstance(response, dict):
                        quiz = response.get('quiz', None)
                        if quiz is not None:
                            table_data = get_table_data(quiz)
                            if table_data is not None:
                                df = pd.DataFrame(table_data)
                                df.index = df.index + 1
                                st.table(df)

                                st.text_area(label='Review', value=response.get('review', ''), height=200)
                            else:
                                st.error('Error in the table data')
                    else:
                        st.write(response)
        else:
            st.warning('Please fill out all fields and upload a file.')