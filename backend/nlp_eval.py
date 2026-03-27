def evaluate_answer(user_answer):

    word_count = len(user_answer.split())

    if word_count > 25:
        return 9, "Excellent answer"
    elif word_count > 15:
        return 7, "Good answer"
    elif word_count > 8:
        return 5, "Average answer"
    else:
        return 3, "Needs improvement"
