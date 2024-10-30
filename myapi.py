from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import Optional

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


@app.get(
    "/singers/{singer_id}",
    responses={
        404: {
            "description": "Singer with the specified ID not found.",
            "content": {
                "application/json": {
                    "example": {"detail": "Singer with the ID 123 not found."}
                }
            },
        }
    },
)
def get_singer_by_id(singer_id: int = Path(description="The ID of the singer", gt=0)):
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
    #TODO: add validation - empty request body fields, singer already exists

    for singer_id in singers:
        if singers[singer_id]["name"] == singer.name:
            raise HTTPException(
                status_code=409,
                detail=f"Singer with the name '{singer.name}' already exists.",
            )

    singers[len(singers) + 1] = singer.dict()
    return singers[len(singers)]


@app.patch("/singers/{singer_id}", status_code=201, response_model=UpdateSinger)
def update_singer(singer_id: int, new_singer: UpdateSinger):
    if singer_id not in singers:
        raise HTTPException(
            status_code=404, detail=f"Singer with the ID {id} not found."
        )

    stored_singer_data = singers[singer_id]
    update_data = new_singer.model_dump(
        exclude_unset=True
    )  # convert request body to a dictionary
    stored_singer_data.update(
        update_data
    )  # update the old singer data with the new data
    updated_singer = Singer(
        **stored_singer_data
    )  # convert the updated singer dictionary to an instance of the Singer model (for validations)
    singers[singer_id] = updated_singer.dict()  # store the updated data as a dictionary

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
