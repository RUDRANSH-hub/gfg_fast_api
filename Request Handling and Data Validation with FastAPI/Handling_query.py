from fastapi import FastAPI, Header, Query, Cookie

app = FastAPI()

@app.get("/items/")
def get_items(
    q: str = Query(None, min_length=3, max_length=50),
    user_agent: str = Header(default=None),
    session_token: str = Cookie(default=None)
):
    return {"q": q, "user_agent": user_agent, "session_token": session_token}
