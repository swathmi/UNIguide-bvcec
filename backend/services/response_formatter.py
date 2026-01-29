def normalize_to_list(data):
    if isinstance(data, list):
        return [str(item).strip() for item in data if str(item).strip()]

    if isinstance(data, str):
        for sep in ["•", "-", "–", "|", "\n"]:
            data = data.replace(sep, "\n")
        return [line.strip() for line in data.split("\n") if line.strip()]

    return []


def format_lines(title, content, emoji="🔹"):
    lines = normalize_to_list(content)
    response = f"{title}:\n\n"
    for line in lines:
        response += f"{emoji} {line}\n"
    return response.strip()
