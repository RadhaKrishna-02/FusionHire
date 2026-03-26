let mediaRecorder;
let audioChunks = [];
let questions = [];
let currentQ = 0;

// ⚠️ CHANGE THIS AFTER RENDER DEPLOY
const BASE_URL = "http://127.0.0.1:8000";

async function startSetup() {

    let file = document.getElementById("resume").files[0];
    let difficulty = document.getElementById("difficulty").value;

    let formData = new FormData();
    formData.append("resume", file);
    formData.append("difficulty", difficulty);

    await fetch(`${BASE_URL}/setup/`, {
        method: "POST",
        body: formData
    });

    let res = await fetch(`${BASE_URL}/questions/`);
    let data = await res.json();

    questions = data.questions;

    document.getElementById("setup").style.display = "none";
    document.getElementById("interview").style.display = "block";

    showQuestion();
}

function showQuestion() {
    document.getElementById("question").innerText = questions[currentQ];
}

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };
}

async function stopRecording() {

    mediaRecorder.stop();

    mediaRecorder.onstop = async () => {

        const blob = new Blob(audioChunks, { type: 'audio/wav' });

        let formData = new FormData();
        formData.append("audio", blob);
        formData.append("qno", currentQ);

        const res = await fetch(`${BASE_URL}/answer/`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        document.getElementById("result").innerText =
            `Score: ${data.score} | ${data.feedback}`;

        audioChunks = [];
        currentQ++;

        if (currentQ < questions.length) {
            setTimeout(showQuestion, 2000);
        } else {
            finishInterview();
        }
    };
}

async function finishInterview() {

    let res = await fetch(`${BASE_URL}/result/`);
    let data = await res.json();

    document.getElementById("interview").style.display = "none";
    document.getElementById("final").style.display = "block";

    document.getElementById("score").innerText =
        `Final Score: ${data.average_score} (${data.verdict})`;
}