import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # read local .env file


def user_login(supabase):
    ''' Once i create frontend for user authentication, user credentials will be passed via request
    This sounds like a sensitive topic so i will need to be careful. 
    '''
    random_email: str = "janekzimoch@gmail.com"
    random_password: str = os.environ["DB_SUPABASE_PASSWORD"]
    user = supabase.auth.sign_in_with_password(
        {"email": random_email, "password": random_password})
    # set the right key to enable RSL - security
    postgrest_client = supabase.postgrest
    postgrest_client.auth(user.session.access_token)
    return user


def user_logout(supabase, key):
    ''' user login and logout should be created as decorators. I will change that later when code is more mature. '''
    # after running queries - exceute this
    supabase.auth.sign_out()
    postgrest_client = supabase.postgrest
    postgrest_client.auth(key)


def is_not_empty(supabase):
    data = supabase.table("documents").select("id").execute()
    return len(data.data) > 0


def get_metadata(list_of_texts):
    contents = [par['content'] for par in list_of_texts]
    metadata = [{'page': par['page'], 'title': par['title']}
                for par in list_of_texts]
    return contents, metadata


def formulate_prompt(query, docs_with_score):
    # # " Try to be quite descriptive but without repeating yourself or making things up. " + \
    prompt = "You are an experienced and skilled litigation lawyer. " +\
        "Your task is to assist a user in answering questions about a legal case. " + \
        "You don't have access to the entire document, but the most relevant exerpts from the case will be provided to you for reference. " +\
        "Exerpts will be provided alongside with scores of how relevant those texts are to the question asked and also with page number to indicate on which pages in the document these paragraphs apeared. " +\
        "You can use page numbers and scores to judge relevance of paragraphs and to know in what order paragraphs apeared in the document. " +\
        "The lower the score the more relevant the exerpt is according to some imperfect scoring technique. " + \
        "You are required to answer truthfully and explain why you made a certain decision. " +\
        "If provided paragraphs do not contain enough context to deduce the answer, you should acklowedge so. " + \
        "\n" + \
        f"The question is: {query} \n" + \
        "Here are the most relevant exerpts, their scores, and page numbers where they appeared: \n" + \
        ('\n').join([f"Exerpt: {doc.page_content}; Score: " +
                     str(round(scr, 3)) + f"; Page: {doc.metadata['page']}" for doc, scr in docs_with_score])
    return prompt
