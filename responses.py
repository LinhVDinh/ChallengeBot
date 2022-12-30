def handle_response(message) -> str:
    l_message = message.lower()

    #help
    if l_message == '!help':
        return 'this is filler'
    elif l_message == '!challenge':
        return 'Challenge accepted!'
    elif l_message == '!checkin':
        return "Checked in!"
    elif l_message == '!leaderboard':
        return 'Leaderboards:'