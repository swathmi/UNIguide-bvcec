def normalize_to_list(data):
    if isinstance(data, list):
        # Clean each item and remove embedded newlines
        result = []
        for item in data:
            item_str = str(item).strip()
            # Split on newlines and add each part separately
            parts = item_str.split('\n')
            for part in parts:
                clean_part = part.strip()
                if clean_part:
                    result.append(clean_part)
        return result

    if isinstance(data, str):
        # Split on multiple separators
        for sep in ["•", "-", "–", "|", "\n"]:
            data = data.replace(sep, "\n")
        return [line.strip() for line in data.split("\n") if line.strip()]

    return []


def format_lines(title, content, emoji="🔹"):
    lines = normalize_to_list(content)
    # Build response with just newlines - no HTML tags
    response_lines = [f"{title}:"]
    for line in lines:
        response_lines.append(f"{emoji} {line}")
    return "\n".join(response_lines)


def format_plain_text(text):
    """
    Converts any plain text to line-by-line format
    Useful for wrapping raw responses to ensure consistent formatting
    """
    if not isinstance(text, str) or not text.strip():
        return text
    
    # Split into lines and preserve structure
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            formatted_lines.append(stripped)
    
    return "\n".join(formatted_lines)
