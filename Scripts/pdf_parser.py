import fitz  # PyMuPDF

def Split_PDFS(pdf_file):

    # Open the PDF file
    pdf = fitz.open(pdf_file)

    # Create a list to hold the text of each resume
    resumes = []
    current_resume_text = ""

    # Loop through each page in the PDF
    for page_number in range(pdf.page_count):
        page = pdf.load_page(page_number)
        text = page.get_text("text")
        text = text.replace("NATIONAL INSTITUTE OF TECHNOLOGY KARNATAKA, SURATHKAL   \n P.O SRINIVASNAGAR, MANGALORE-575025 \n", " ")
        
        # Add the text of the current page to the current resume
        if "Placements 2009-10" in text:
            resumes.append(current_resume_text)
            current_resume_text = ""
            current_resume_text += text
        
        # Check if the current page is the end of a resume
        # You can modify the condition based on your specific case
        if "Placements 2009-10" not in text or page_number == pdf.page_count - 1:
            current_resume_text += text
    del resumes[0]
    return resumes