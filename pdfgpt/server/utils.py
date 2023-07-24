import pypdf
import fitz
from langchain.schema import Document


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
        list_of_texts[n]['content'] = list_of_texts[n]['content'].replace(
            '\n', ' ')
    return list_of_texts


def remove_short_chunks(list_of_texts):
    ''' short chunks are artefacts of PyMuPDF PDF parser
    i.e. page counts, chapter headers, footnotes etc.
    There will be some false positives i.e. poorly cut paragraph across pages, where 2nd part is very short.
    but we can fix that later, and those should be in minority. '''
    new_list = []
    for paragraph in list_of_texts:
        if len(paragraph['content']) > 100:
            new_list.append(paragraph)
    return new_list


def read_PDF_PyMuPDF(path_to_pdf, filename):
    ''' this tool is better than pypdf because it keeps the paragraph structure of the document. 
    And it makes sense to embed paragraphs into vectors, as paragraphs encompas some semantic substance. '''
    doc = fitz.open(path_to_pdf)
    num_pages = len(doc)
    list_of_texts = []
    for n in range(num_pages):
        page = doc[n]
        text = page.get_text("blocks")
        for chunk in text:
            list_of_texts.append({
                'content': chunk[4],
                'page': n,
                'title': filename,
            })
    return list_of_texts


def append_metadata(list_of_texts):
    list_of_documents = [
        Document(page_content=par['content'], metadata={'page': par['page'], 'title': par['title']}) for par in list_of_texts]
    return list_of_documents


def get_metadata(list_of_texts):
    contents = [par['content'] for par in list_of_texts]
    metadata = [{'page': par['page'], 'title': par['title']}
                for par in list_of_texts]
    return contents, metadata


def combine_text(list_of_texts):
    ''' combine strings of texts into a single chunk '''
    text_as_string = ' '.join(list_of_texts)
    return text_as_string


def get_paragraphs(df_file, pdf_name):
    list_of_texts = read_PDF_PyMuPDF(df_file, pdf_name)
    list_of_texts = remove_end_of_lines(list_of_texts)
    list_of_texts = remove_short_chunks(list_of_texts)
    return list_of_texts


def formulate_prompt(query, docs_with_score):
    # # " Try to be quite descriptive but without repeating yourself or making things up. " + \
    prompt = "You are a system to answer questions about some documents. " + \
        "You don't have access to the entire document, but the most relevant exerpts from the document will be provided to you for reference, alongside with scores of how relevant those texts are to the question asked. The lower the score the more relevant the exerpt is according to some imperfect scoring technique. " + \
        "You are required to answer truthfully and acklowedge so when you don't know the answer " + \
        " or provided texts do not provide you with enought context to make a confident answer. " + \
        "\n" + \
        f"The question is: {query} \n" + \
        "Here are the most relevant exerpts and their scores: \n" + \
        ('\n').join([f"Exerpt: {doc.page_content}; Score: " +
                     str(round(scr, 3)) for doc, scr in docs_with_score])
    return prompt
