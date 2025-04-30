import re 


def retrieve_subject_from_user_prompt(prompt:str) -> str:
    """
    Extracts the subject from a user prompt enclosed in square brackets.

    Args:
        prompt (str): The user prompt containing the subject in square brackets.

    Returns:
        str: The subject extracted from the prompt, or None if no subject is found.
    """
    pattern = r"\[(.*?)\]"
    match = re.search(pattern, prompt)
    if match:
        return match.group(1)
    else:
        return None

def parse_subject(subject:str) -> str:
    """
    Parses the subject extracted from a user prompt.

    Args:
        subject (str): The subject extracted from the user prompt.

    Returns:
        str: The parsed subject.
    """
    if "aprendizaje" in subject.lower():
        return "pscicologia-del-aprendizaje"
    if "fundamentos" in subject.lower():
        return "fundamentos-de-investigacion"
    else:
        return None

def get_subject(prompt:str) -> str:
    """
    Extracts and parses the subject from a user prompt.

    Args:
        prompt (str): The user prompt containing the subject in square brackets.

    Returns:
        str: The parsed subject extracted from the prompt.
    """
    subject = retrieve_subject_from_user_prompt(prompt)
    if subject:
        return parse_subject(subject)
    else:
        return None