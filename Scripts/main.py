import os
from pdf_parser import Split_PDFS
from extraction_Deepseek import details_extractor
import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

os.chdir('C:\\Users\\manoj\\Downloads\\Manpower_Resume_Extraction')

MainPDF='2.resumes_compiled.pdf'
resumes=Split_PDFS(MainPDF)

details_all=pd.DataFrame()
details_all_errors=pd.DataFrame()

for i in range(len(resumes)):
    try:
        details=details_extractor(resumes[i])
        if len(details_all.columns)>0 :
        #and len(details.columns)==len(details_all.columns):
            details.columns=details_all.columns
        # Concatenate DataFrames
        details_all = pd.concat([details_all, details], axis=0, ignore_index=True)
    except Exception as e:
        details_all_errors = pd.concat([details_all_errors, details], axis=0, ignore_index=True)
        print(f"An error occurred: {e}. Skipping {i}.")
        logging.error(f"An error occurred: {e}. Skipping {i}.values {details}")


details_all.to_csv("Resume_details_all.csv", index=False)
details_all_errors.to_csv("Resume_details_all_errors.csv", index=False)