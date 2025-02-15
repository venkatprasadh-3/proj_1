from fastapi import FastAPI, HTTPException
import os
from api.agent import process_task, read_file

app = FastAPI()

@app.post("/run")
def run_task(task: str):
    try:
        result = process_task(task)
        return {"status": "success", "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
def read_task_file(path: str):
    return read_file(path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)