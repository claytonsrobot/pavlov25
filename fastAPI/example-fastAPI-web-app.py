from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my Dockerized API!"}

@app.get("/analyze-data")
def analyze_data(param: str):
    if not param:
        raise HTTPException(status_code=400, detail="Invalid parameter")
    result = {"analysis": f"Processed data for {param}"}
    return result