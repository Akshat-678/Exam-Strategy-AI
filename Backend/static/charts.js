let topicsChart = null;
let difficultyChart = null;

async function sendForAnalysis() {
    const text = document.getElementById("paperText").value;
    const status = document.getElementById("statusText");

    if (!text.trim()) {
        status.innerText = "Please paste some text first.";
        return;
    }

    status.innerText = "Analyzing...";

    const response = await fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    });

    const data = await response.json();

    status.innerText = "Analysis complete.";

    renderCharts(data);
}
function renderCharts(data) {

    /* ---------- TOPICS PIE ---------- */
    const topicsCtx = document.getElementById("topicsChart").getContext("2d");

    if (topicsChart) {
        topicsChart.destroy();
    }

    topicsChart = new Chart(topicsCtx, {
        type: "pie",
        data: {
            labels: Object.keys(data.topics),
            datasets: [{
                data: Object.values(data.topics)
            }]
        },
        options: {
            plugins: {
                legend: { position: "bottom" }
            }
        }
    });

    /* ---------- DIFFICULTY METER ---------- */
    const score = data.difficulty_score;
    const meterCtx = document.getElementById("difficultyMeter").getContext("2d");

    if (difficultyChart) {
        difficultyChart.destroy();
    }

    difficultyChart = new Chart(meterCtx, {
        type: "doughnut",
        data: {
            labels: ["Easy", "Moderate", "Hard"],
            datasets: [{
                data: [33, 34, 33],
                backgroundColor: ["#4CAF50", "#FFC107", "#F44336"]
            }]
        },
        options: {
            rotation: -90,
            circumference: 180,
            cutout: "70%",
            plugins: {
                tooltip: { enabled: false },
                legend: { position: "bottom" }
            }
        }
    });

    /* ---------- NEEDLE ---------- */
    const angle = -90 + (score * 180 / 100);
    document.getElementById("needle").style.transform =
        `rotate(${angle}deg)`;

    let label = "Moderate";
    if (score < 33) label = "Easy";
    else if (score > 66) label = "Hard";

    document.getElementById("difficultyText").innerText =
        `Difficulty Score: ${score} (${label})`;
}


