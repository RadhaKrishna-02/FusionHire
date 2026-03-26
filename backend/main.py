from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil

from speech import transcribe_audio
from nlp_eval import evaluate_answer

app = FastAPI()

# ✅ CORS (IMPORTANT for Netlify connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

questions = []
answers = []


# 📌 Setup: Upload resume + difficulty
@app.post("/setup/")
async def setup(resume: UploadFile = File(...), difficulty: str = Form(...)):

    # Save resume
    with open("resume.pdf", "wb") as f:
        shutil.copyfileobj(resume.file, f)

    global questions, answers
    answers = []

    # Simple static questions (upgrade later)
    questions = [
        "Introduce yourself",
        "Explain your projects",
        "What are your strengths?",
        "Explain a technical concept you know",
        "What is OOP?",
        "What is Machine Learning?",
        "Explain your favorite subject",
        "What challenges did you face?",
        "Why should we hire you?",
        "Where do you see yourself in 5 years?"
    ]

    return {"message": "Setup complete", "total_questions": len(questions)}


# 🎤 Answer processing
@app.post("/answer/")
async def answer(audio: UploadFile = File(...), qno: int = Form(...)):

    filename = f"temp_{qno}.wav"
    with open(filename, "wb") as f:
        f.write(await audio.read())

    text = transcribe_audio(filename)
    score, feedback = evaluate_answer(text)

    answers.append(score)

    return {
        "transcript": text,
        "score": score,
        "feedback": feedback
    }


# 📊 Final result
@app.get("/result/")
def result():
    if not answers:
        return {"error": "No answers found"}

    avg_score = sum(answers) / len(answers)

    if avg_score > 7:
        verdict = "Excellent"
    elif avg_score > 4:
        verdict = "Good"
    else:
        verdict = "Needs Improvement"

    return {
        "average_score": round(avg_score, 2),
        "verdict": verdict
    }


# 📌 Get questions
@app.get("/questions/")
def get_questions():
    return {"questions": questions}