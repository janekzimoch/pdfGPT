import numpy as np
from tqdm import tqdm
import fitz


def get_page_lines(page):
    lines = []
    line_numbers = []
    i = 1
    parsed_page = page.get_text("dict")
    for paragraph in parsed_page['blocks']:
        if 'lines' in paragraph:
            for line in paragraph['lines']:
                line_text = (' ').join([span['text']
                                        for span in line['spans']])
                line_text = line_text.rstrip()
                if len(line_text) > 0:
                    lines.append(line_text)
                    line_numbers.append(i)
                    i += 1
    return lines, line_numbers


def get_doc_lines(doc):
    ''' combine all line objects into a single list 
    page count starts from 1 not 0 (thus: n+1 below)
    '''
    N = len(doc)
    doc_lines = []
    for n in tqdm(range(N)):
        page = doc[n]
        page_lines, page_line_numbers = get_page_lines(page)
        page_lines = [{'content': text, 'page': n+1, 'start_line': i}
                      for text, i in zip(page_lines, page_line_numbers)]
        doc_lines += page_lines
    return doc_lines


def get_mean_line_length(lines):
    ''' return mean number of characters in a line. '''
    line_lengths = []
    for line in lines:
        line_lengths.append(len(line))
    return np.mean(line_lengths)


def word_break_edge_case(line):
    ''' function coverign an edge case where line ends with a word break i.e.
    "Thomas went out fi-
    shing with friends."

    We would like two halfs of the word to be joined post merger of lines.
    '''
    if line[-1] == '-':
        return line[:-1], ''
    else:
        return line, ' '


def combine_lines_into_paragraphs(lines, title, long):
    ''' note, we are using a hardcoded threshold here. 
    We need to use some smart way to use the disribution of line lengths to find what could be the sortest line 
    that wouldn't indicate a new paragraph. But note even then we only consider liens which end with .!? so the chances that it is actuallya finish 
    of a paragraph are quite high. 

    each paragraph should be a dict:
    {
        'content': text,
        'page': n,
        'title': filename,
        'start_line': m,
    }
    '''
    paragraphs = []
    new_paragraph = None
    # mean will be skewed towards shorter sentences becasue there won't be many much longer
    mean_length = get_mean_line_length([line['content'] for line in lines])
    for line in tqdm(lines):
        if new_paragraph is None:
            new_paragraph = {'content': '',
                             'page': line['page'],
                             'title': title,
                             'start_line': line['start_line']
                             }
        if len(line['content']) > 1:

            line['content'], space = word_break_edge_case(line['content'])

            if (line['content'][-1] in '.?!') and (line['content'][-2] != ' '):
                new_paragraph['content'] += space + line['content']
                if long:
                    if len(line['content']) > mean_length:  # still the same paragraph
                        continue
                    else:  # it's a new paragraph
                        paragraphs.append(new_paragraph)
                        new_paragraph = None
                else:
                    paragraphs.append(new_paragraph)
                    new_paragraph = None
            else:
                if len(line['content']) < (mean_length / 2):
                    # if it's shorter than ~20 characters than it's probably soe miscelenous artefact
                    continue
                else:
                    new_paragraph['content'] += space + line['content']
    return paragraphs


def get_paragraphs(path_to_pdf, title, long=False):
    doc = fitz.open(path_to_pdf)
    doc_lines = get_doc_lines(doc)
    paragraphs = combine_lines_into_paragraphs(doc_lines, title, long)
    return paragraphs
