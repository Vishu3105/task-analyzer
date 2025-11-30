console.log("script.js loaded");

// DOM elements (objects that represent HTML elements)
const analyzeBtn = document.getElementById("analyzeBtn");
const suggestBtn = document.getElementById("suggestBtn");
const taskInput = document.getElementById("taskInput");
const resultsDiv = document.getElementById("results");
const strategySelect = document.getElementById("strategy");

const addTaskBtn = document.getElementById("addTaskBtn");
const titleInput = document.getElementById("title");
const dueDateInput = document.getElementById("due_date");
const hoursInput = document.getElementById("estimated_hours");
const importanceInput = document.getElementById("importance");
const depsInput = document.getElementById("dependencies");

// In-memory list like admin table
let inMemoryTasks = [];
let nextId = 1;

// click events
analyzeBtn.addEventListener("click", analyzeTasks);
suggestBtn.addEventListener("click", fetchSuggestions);
addTaskBtn.addEventListener("click", addTaskFromForm);

// ---------- left side input tasks ----------

function parseDependencies(value) {
    if (!value) return [];
    return value
        .split(",")
        .map(v => v.trim())
        .filter(v => v.length > 0)
        .map(v => parseInt(v, 10))
        .filter(n => !Number.isNaN(n));
}

function refreshTaskTextarea() {
    taskInput.value = JSON.stringify(inMemoryTasks, null, 2);
}

function addTaskFromForm() {
    const title = (titleInput.value || "").trim();
    const dueDate = dueDateInput.value || null;
    const hours = parseInt(hoursInput.value, 10);
    const importance = parseInt(importanceInput.value, 10);
    const deps = parseDependencies(depsInput.value);

    if (!title || !dueDate || Number.isNaN(hours) || Number.isNaN(importance)) {
        alert("Please fill Title, Due date, Estimated hours and Importance.");
        return;
    }

    const task = {
        id: nextId++,
        title: title,
        due_date: dueDate,
        estimated_hours: hours,
        importance: importance,
        dependencies: deps
    };

    inMemoryTasks.push(task);
    refreshTaskTextarea();

    // To reset some fields
    titleInput.value = "";
    hoursInput.value = "1";
    importanceInput.value = "5";
    depsInput.value = "";
}

// ---------- Priority visual helper ----------

function priorityClass(score) {
    if (score >= 120) {
        return "high";
    } else if (score >= 80) {
        return "medium";
    } else {
        return "low";
    }
}

// ---------- Analyze JSON tasks ----------

async function analyzeTasks() {
    let tasks;

    try {
        const text = taskInput.value.trim();
        tasks = text ? JSON.parse(text) : [];
    } catch (e) {
        alert("Invalid JSON. Please check Input Tasks JSON.");
        return;
    }

    if (!Array.isArray(tasks) || tasks.length === 0) {
        alert("Please add at least one task (via the form or JSON).");
        return;
    }

    const strategy = strategySelect ? strategySelect.value : "smart";

    const url = `/api/tasks/analyze/?strategy=${encodeURIComponent(strategy)}`;
    console.log("Calling URL:", url);

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(tasks)
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.error || "Server error");
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error(error);
        alert("Failed to analyze tasks: " + error.message);
    }
}

// ---------- Fetch suggestions from DB ----------

async function fetchSuggestions() {
    const strategy = strategySelect ? strategySelect.value : "smart";
    const url = `/api/tasks/suggest/?strategy=${encodeURIComponent(strategy)}`;
    console.log("Calling suggestions URL:", url);

    try {
        const response = await fetch(url, {
            method: "GET"
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.error || "Server error");
        }

        const data = await response.json();
        if (!data || data.length === 0) {
            alert("No tasks found in database. Add tasks in admin first.");
        }
        displayResults(data);
    } catch (error) {
        console.error(error);
        alert("Failed to fetch suggestions: " + error.message);
    }
}

// ---------- Render results ----------

function displayResults(tasks) {
    resultsDiv.innerHTML = ""; // To clear previous

    if (!tasks || tasks.length === 0) {
        resultsDiv.textContent = "No results.";
        return;
    }

    tasks.forEach(task => {
        const wrapper = document.createElement("div");
        const level = priorityClass(task.score ?? 0);
        wrapper.className = `results-card ${level}`;

        const title = document.createElement("h3");
        title.textContent = task.title || "(No title)";

        const meta = document.createElement("p");
        meta.textContent =
            `Due: ${task.due_date || "N/A"} | ` +
            `Hours: ${task.estimated_hours ?? "?"} | ` +
            `Importance: ${task.importance ?? "?"} | ` +
            `Dependencies: ${(task.dependencies || []).join(", ") || "None"}`;

        const score = document.createElement("p");
        score.className = "score";
        score.textContent = `Score: ${task.score}`;

        const expl = document.createElement("p");
        expl.className = "explanation";
        expl.textContent = task.explanation || "";

        wrapper.appendChild(title);
        wrapper.appendChild(meta);
        wrapper.appendChild(score);
        wrapper.appendChild(expl);

        resultsDiv.appendChild(wrapper);
    });
}
