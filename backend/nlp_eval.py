from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

EXPECTED = "This is a good structured answer"

def evaluate_answer(user_answer):

    embeddings = model.encode([EXPECTED, user_answer])
    similarity = util.cos_sim(embeddings[0], embeddings[1])

    score = float(similarity[0][0]) * 10

    if score > 7:
        feedback = "Good answer"
    elif score > 4:
        feedback = "Average answer"
    else:
        feedback = "Needs improvement"

    return round(score, 2), feedback