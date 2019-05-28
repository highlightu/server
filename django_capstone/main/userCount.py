user_count = 0


def userCreated():
    global user_count
    user_count += 1

    return str(user_count)
