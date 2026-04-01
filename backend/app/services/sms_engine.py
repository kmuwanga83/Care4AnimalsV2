def build_sms_response(user_text: str) -> str:
    text = user_text.strip().lower()
    if text in {"start", "hi", "hello"}:
        return (
            "Welcome to CARE4ANIMALS\n"
            "Choose language:\n"
            "1. English\n"
            "2. Luganda\n"
            "3. Swahili"
        )
    if text == "1":
        return (
            "Topics:\n"
            "1. Disease Management\n"
            "2. Vaccination\n"
            "3. Animal Welfare\n"
            "Reply with a number."
        )
    return "Thank you. More guided SMS flow will be connected next."
