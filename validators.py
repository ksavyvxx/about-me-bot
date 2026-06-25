import re
def validate_feedback(text: str) -> dict | None:
    pattern = r"^([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,20}):\s*(.+)$"
    match = re.match(pattern, text.strip())

    if match:
        return {
            "email": match.group(1),
            "text": match.group(2).strip()
        }
    return None


def check_secret_code(text: str) -> bool:
    pattern = r"^capedu2026-[a-z0-9]+$"
    return bool(re.match(pattern, text.strip(), re.IGNORECASE))