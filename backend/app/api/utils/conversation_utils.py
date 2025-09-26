import re


def retrieve_subject_from_user_prompt(prompt: str) -> str:
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


def parse_subject(subject: str) -> str:
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


def get_subject(prompt: str) -> str:
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


def format_reference(source_data: dict) -> str:
    """
    Format a reference entry from source_data.
    Example: [filename (pág. <page+1>)](storage_url#page=<page+1>)
    """
    title = source_data.get("title", "Unknown")
    page = int(source_data.get("page", 0)) + 1  # add 1
    url = source_data.get("storage_url", "#")
    return f"[{title} (pág. {page})]({url}#page={page})"


def process_references(text: str, references: list, mode: str = "inline") -> str:
    """
    Replace or append references in text.

    Parameters:
        text (str): Input text containing [ref_id:N].
        references (list): Each item has .source_data attribute (dict).
        mode (str): "inline" -> replace inline with formatted link,
                    "bibliography" -> replace with [1],[2],... and append list.
    """
    pattern = r"\[ref_id:(\d+)\]"

    if mode == "inline":

        def replace_ref(match):
            idx = int(match.group(1))
            if 0 <= idx < len(references):
                return format_reference(references[idx].source_data)
            return match.group(0)

        return re.sub(pattern, replace_ref, text)

    elif mode == "bibliography":
        # Extract ids in order of first appearance
        ids = [int(m.group(1)) for m in re.finditer(pattern, text)]
        unique_ids = []
        for i in ids:
            if i not in unique_ids:
                unique_ids.append(i)

        # Map reference id -> citation number
        ref_map = {ref_id: i + 1 for i, ref_id in enumerate(unique_ids)}

        # Replace in-text refs with [n]
        def replace_with_number(match):
            idx = int(match.group(1))
            return f"[{ref_map[idx]}]" if idx in ref_map else match.group(0)

        clean_text = re.sub(pattern, replace_with_number, text)

        # Build references section
        biblio = "\n\nFuentes:  \n"
        for ref_id, num in ref_map.items():
            if 0 <= ref_id < len(references):
                biblio += (
                    f"  [{num}] {format_reference(references[ref_id].source_data)}  \n"
                )

        return clean_text.strip() + biblio

    else:
        raise ValueError("mode must be either 'inline' or 'bibliography'")
