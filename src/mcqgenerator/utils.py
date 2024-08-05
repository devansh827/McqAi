import os
import traceback
import PyPDF2
import json

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
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
        # Print the input to debug
        print("Received quiz_str:", repr(quiz_str))

        # Strip the prefix if it exists
        if quiz_str.startswith('### RESPONSE_JSON\n'):
            quiz_str = quiz_str[len('### RESPONSE_JSON\n'):]

        # Check if the input is empty
        if not quiz_str.strip():
            raise ValueError("Input JSON string is empty")

        # Convert the quiz from str to dict
        quiz_dict = json.loads(quiz_str)
        
        # Verify that quiz_dict is a dictionary
        if not isinstance(quiz_dict, dict):
            raise ValueError("Parsed JSON is not a dictionary")

        quiz_table_data = []

        # Iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            if not isinstance(value, dict):
                raise ValueError(f"Item {key} is not a dictionary")

            mcq = value.get('mcq')
            options = value.get('options', {})
            correct = value.get('correct')
            
            if not mcq or not isinstance(options, dict) or not correct:
                raise ValueError(f"Missing required fields in item {key}")

            options_str = " | ".join(
                [f"{option}: {option_value}" for option, option_value in options.items()]
            )

            quiz_table_data.append({'MCQ': mcq, 'Choices': options_str, 'Correct': correct})

        return quiz_table_data

    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        return False
    except ValueError as e:
        print("Value error:", e)
        return False
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False



