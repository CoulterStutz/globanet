def command(message: str):
    from_str = ""
    to_str = ""
    command_str = ""

    # Find the first occurrence of --> in the string
    arrow_index = message.find("-->")

    if arrow_index != -1:
        # Get the substring before the arrow
        from_str = message[message.find("[", 0, arrow_index):arrow_index]

        # Get the substring after the arrow
        to_index = message.find("[", arrow_index)
        if to_index != -1:
            to_str = message[to_index:message.find("]", to_index)] + "]"

            # Get the substring after the colon
            command_index = message.find(":")
            if command_index != -1:
                command_str = message[command_index + 2:]

            out = {
                "from": from_str.strip(),
                "to": to_str.strip(),
                "command": command_str.strip(),
            }
    return out
