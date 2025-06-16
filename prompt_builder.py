def build_prompt(text):
    return (
        "Extract the following information from the text below and return as JSON with keys: "
        "name, phone or 'contact' or 'contact no', skills, education (with college, university, graduation_year):\n\n"
        f"{text}\n\n"
        "JSON:"
    )
