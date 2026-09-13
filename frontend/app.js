async function loadTasks() {

    const response = await fetch("/api/tasks");

    const tasks = await response.json();

    const taskList = document.getElementById("taskList");

    taskList.innerHTML = "";

    tasks.forEach(task => {

        const div = document.createElement("div");

        div.className = "task";

        div.innerHTML = `
            <span class="${task.completed ? "completed" : ""}">
                ${task.title}
            </span>

            <div>
                <button onclick="toggleTask(${task.id})">
                    ✓
                </button>

                <button onclick="deleteTask(${task.id})">
                    🗑
                </button>
            </div>
        `;

        taskList.appendChild(div);
    });
}


async function addTask() {

    const input = document.getElementById("taskInput");

    const title = input.value.trim();

    if (!title) return;

    await fetch("/api/tasks", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: title
        })

    });

    input.value = "";

    loadTasks();
}


async function toggleTask(id) {

    await fetch(`/api/tasks/${id}`, {
        method: "PUT"
    });

    loadTasks();
}


async function deleteTask(id) {

    await fetch(`/api/tasks/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}


loadTasks();