import os
import traceback
import PyPDF2
import json

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extract_text() or ""
            return text
        
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            raise Exception('Error reading the PDF file')
    
    elif file.name.endswith(".txt"):
        return file.read().decode('utf-8')
    
    else:
        raise Exception(
            'Unsupported file format only PDF and Text file supported.'
        )

def get_table_data(quiz_str):
    try:
        # Converting the quiz from str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # Iterating over the quiz dictionary and extracting the required information
        for key, value in quiz_dict.items():
            mcq = value['mcq']
            options = " || ".join(
                [
                    f"{option} -> {option_value}" for option, option_value in value['options'].items()
                ]
            )

            correct = value['correct']
            quiz_table_data.append({'MCQ': mcq, 'Choices': options, 'Correct': correct})
        
        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
