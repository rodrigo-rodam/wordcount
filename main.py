import os
import sys
import pytesseract
from PIL import Image
from collections import Counter
from pdf2image import convert_from_path

"""
Get the words tha we need to find inside the text
"""


def get_words():
    return "la vigilancia y control, pablo, mauro, carlos, robert fisk, del dinero, mafia, del poder, mafia del poder, fifí(s), chairo(s), poder al pueblo, cuarta transformación"


"""
Count how many times an expression appears inside a text
"""


def popularity(text, words):

    text = text.lower()
    words = [word.strip() for word in words.lower().split(",")]

    listp = []

    for word in words:
        if text.count(word) > 0:
            listp.append((word, text.count(word)))
    return listp


"""
Read the directory and get the files that will be processed
"""


def get_files_to_process(files_directory):
    return [f for f in os.listdir(files_directory) if f.endswith(".pdf")]


"""
Read PDF file using OCR, extract each page as a JPEG file, write a file w/ the text
extracted and return the text
"""


def read_file(directory, file_path):
    """
    Part #1 : Converting PDF to images 
    """
    # Store all the pages of the PDF in a variable
    pages = convert_from_path(f"{directory}/{file_path}", 500)
    # Counter to store images of each page of PDF to image
    image_counter = 1

    # output directory
    output_dir = "./out"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all the pages stored above
    for page in pages:

        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        # PDF page 2 -> page_2.jpg
        # PDF page 3 -> page_3.jpg
        # ....
        # PDF page n -> page_n.jpg
        filename = f"{file_path}_page_{image_counter}.jpg"

        # Save the image of the page in system
        page.save(f"{output_dir}/{filename}", "JPEG")

        # Increment the counter to update filename
        image_counter = image_counter + 1

    """ 
    Part #2 - Recognizing text from the images using OCR 
    """
    # Variable to get count of total number of pages
    filelimit = image_counter - 1

    text_from_pages = ""

    # Iterate from 1 to total number of pages
    for i in range(1, filelimit + 1):
        # Set filename to recognize text from
        # Again, these files will be:
        # page_1.jpg
        # page_2.jpg
        # ....
        # page_n.jpg
        filename = f"{output_dir}/{file_path}_page_{i}"

        # Recognize the text as string in image using pytesserct
        text = str(((pytesseract.image_to_string(Image.open(f"{filename}.jpg")))))

        # The recognized text is stored in variable text
        # Any string processing may be applied on text
        # Here, basic formatting has been done:
        # In many PDFs, at line ending, if a word can't
        # be written fully, a 'hyphen' is added.
        # The rest of the word is written in the next line
        # Eg: This is a sample text this word here GeeksF-
        # orGeeks is half on first line, remaining on next.
        # To remove this, we replace every '-\n' to ''.
        text = text.replace("-\n", "")
        text_from_pages += text

    # Finally, write the processed text to the file.
    f = open(f"{output_dir}/{file_path}.txt", "a")
    f.write(text_from_pages)
    f.close()

    return text_from_pages


def process_directory(files_directory):
    files_to_process = get_files_to_process(files_directory)
    for file_to_process in files_to_process:
        text_extracted = read_file(files_directory, file_to_process)
        print(f"File: {file_to_process} >>> ")
        print(popularity(text_extracted, get_words()))
        # TODO: the variable text_extracted contains the PDF text you can use to
        # count words or something else... in general the OCR process recognize the
        # text very well but it's important review the extraction! See the out directory
        # to review the text extracted.


if __name__ == "__main__":
    # TODO: Put the path for the directory in your machine
    pdfs_directory = "./data/"
    print(process_directory(pdfs_directory))
