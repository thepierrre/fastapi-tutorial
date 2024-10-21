from fastapi import FastAPI, Path, Query, HTTPException

app = FastAPI()

singers = {
    1: {"name": "Taylor Swift", "favorite_song": "Cruel Summer"},
    2: {"name": "Lady Gaga", "favorite_song": "Born This Way"},
    3: {"name": "Kylie Minogue", "favorite_song": "Padam"},
}


@app.get("/")
def index():
    return {"name": "Peter"}


@app.get("/singers/{singer_id}", responses={
    404: {
        "description": 'Singer with the specified ID not found.',
        "content": {
            "application/json": {
                "example": {
                    "detail": 'Singer with the ID 123 not found.'
                }
            }
        }
    }
})
def get_singer_by_id(singer_id: int = Path(description = "The ID of the singer", gt=0)):
    if singer_id not in singers:
        raise HTTPException(
            status_code=404, detail=f"Singer with the ID {singer_id} not found."
        )
    return singers[singer_id]

@app.get("/singers")
def get_singer_by_name(name: str | None = None):
    if name is None:
        return singers
    
    for singer in singers:
        if singers[singer]["name"] == name:
            return singers[singer]
    
    raise HTTPException(
        status_code=404, detail=f"Singer with the name '{name}' not found."
        )