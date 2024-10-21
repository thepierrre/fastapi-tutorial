from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder

app = FastAPI()

singers = {
    1: {"name": "Taylor Swift", "favorite_song": "Cruel Summer"},
    2: {"name": "Lady Gaga", "favorite_song": "Born This Way"},
    3: {"name": "Kylie Minogue", "favorite_song": "Padam"},
}

class Singer(BaseModel):
    name: str
    favorite_song: str

class UpdateSinger(BaseModel):
    name: Optional[str] = None
    favorite_song: Optional[str] = None


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


@app.post("/singers", status_code=201, response_model=Singer)
def create_singer(singer: Singer):
    # add validation - empty request body fields, singer already exists
    singers[len(singers) + 1] = singer
    return singers[len(singers)]


@app.patch("/singers/{singer_id}", status_code=201, response_model=UpdateSinger)
def update_singer(singer_id: int, new_singer: UpdateSinger):
    if singer_id not in singers:
         raise HTTPException(
            status_code=404, detail=f"Singer with the ID {id} not found."
        )
    
    stored_singer = singers[singer_id]
    stored_singer_model = Singer(**stored_singer) # store the singer as an instance of the Singer model (for validation etc.)
    update_data = new_singer.model_dump(exclude_unset=True) # creates a dictionary from the json body (new_singer). exclude_unset = enables partial updates
    updated_singer = stored_singer_model.model_construct(**stored_singer_model.model_dump(), **update_data)
    singers[singer_id] = jsonable_encoder(update_singer)
    return updated_singer

    
@app.delete("/singers/{singer_id}", status_code=204)
def delete_singer(singer_id: int):
     if singer_id not in singers:
         raise HTTPException(
            status_code=404, detail=f"Singer with the ID {singer_id} not found."
        )
     
     singers.pop(singer_id)
     return

# .model_dump = creates a dictionary from the data
# ** is used to unpack the dictionary into the keyword arguments (kwargs) to merge the data
# positional arguments vs. keyword arguments