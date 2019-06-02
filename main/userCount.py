user_count = 0


def userCreated():
    global user_count
    # 8자리로 만들기
    user_count += 1
    output = str(user_count).zfill(8)

    return output
