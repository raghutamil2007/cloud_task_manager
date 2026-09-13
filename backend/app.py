from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg2

app = FastAPI(title="Cloud Task Manager")

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "tasks")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


class Task(BaseModel):
    title: str


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/tasks")
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, completed FROM tasks ORDER BY id DESC"
    )

    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": task[0],
            "title": task[1],
            "completed": task[2]
        }
        for task in tasks
    ]


@app.post("/api/tasks")
def create_task(task: Task):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title) VALUES (%s) RETURNING id",
        (task.title,)
    )

    task_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": task_id,
        "title": task.title,
        "completed": False
    }


@app.put("/api/tasks/{task_id}")
def complete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = NOT completed
        WHERE id = %s
        RETURNING id, title, completed
        """,
        (task_id,)
    )

    task = cursor.fetchone()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": task[0],
        "title": task[1],
        "completed": task[2]
    }


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Task deleted"}