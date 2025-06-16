def build_prompt(text):
    return (
        "Extract the following information from the text below and return ONLY a JSON object with these keys: "
        "name, phone (for phone numbers), education (array with college, university, degree, and graduation_year), "
        "and skills (array). Do not include any explanation or markdown formatting, just the JSON object:\n\n"
        f"{text}\n\n"
    )
