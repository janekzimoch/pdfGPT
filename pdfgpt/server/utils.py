import pypdf
import fitz


def remove_footnote(text):
    # I am assuming this is present on every page
    text = text.split('Animal Farm by George Orwell')[0]
    # this is also a solution only for this specific PDF
    return text


def read_PDF_PyPDF(pdfFileObj):
    ''' read PDF and store it as a list of strings where every string is a page. '''
    # note it would be good to clean the text a bit,
    # for example all parts of a page get saved, while we don't really want the bottom part.
    # there are also some errors where spaces are missing.
    # there are spaces missing from in between words too... i.e. lurched-across, a-fluttering - hopefully chatgpt will manage
    # pdfFileObj = open(path_to_pdf, 'rb')
    print(pdfFileObj)
    pdfReader = pypdf.PdfReader(pdfFileObj)
    num_pages = len(pdfReader.pages)
    list_of_texts = []
    for n in range(num_pages):
        pageObj = pdfReader.pages[n]  # create a page object
        text = pageObj.extract_text()  # extract text from page
        text = remove_footnote(text)
        list_of_texts.append(text)
    return list_of_texts


def remove_end_of_lines(list_of_texts):
    num_chunks = len(list_of_texts)
    for n in range(num_chunks):
        list_of_texts[n] = list_of_texts[n].replace('\n', ' ')
    return list_of_texts


def remove_short_chunks(list_of_texts):
    ''' short chunks are artefacts of PyMuPDF PDF parser
    i.e. page counts, chapter headers, footnotes etc.
    There will be some false positives i.e. poorly cut paragraph across pages, where 2nd part is very short.
    but we can fix that later, and those should be in minority. '''
    new_list = []
    for text in list_of_texts:
        if len(text) > 100:
            new_list.append(text)
    return new_list


def read_PDF_PyMuPDF(path_to_pdf):
    ''' this tool is better than pypdf because it keeps the paragraph structure of the document. 
    And it makes sense to embed paragraphs into vectors, as paragraphs encompas some semantic substance. '''
    doc = fitz.open(path_to_pdf)
    num_pages = len(doc)
    list_of_texts = []
    print(num_pages)
    for n in range(num_pages):
        page = doc[n]
        text = page.get_text("blocks")
        for chunk in text:
            list_of_texts.append(chunk[4])
    return list_of_texts


def combine_text(list_of_texts):
    ''' combine strings of texts into a single chunk '''
    text_as_string = ' '.join(list_of_texts)
    return text_as_string
