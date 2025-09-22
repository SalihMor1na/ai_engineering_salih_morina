import json
from constants import DATA_PATH, CURRENT_YEAR
from pprint import pprint
from pydantic import BaseModel, Field
def read_json(filename):
    with open(DATA_PATH / filename, "r") as file:
        data = json.load(file)
        
    return data

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int = Field(gt=1000, lt=CURRENT_YEAR + 1)
      
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 11,
                "title": "Learn with AIgineer",
                "author": "Kokchun Giang",
                "year": 2025,
            }
        }
    }


class Library(BaseModel):
    name: str
    books: list[Book]
    
def library_data(filename):
    json_data = read_json(filename)
    return Library.model_validate(json_data)


if __name__ == "__main__":
    library = library_data("library.json")
    pprint(library)
