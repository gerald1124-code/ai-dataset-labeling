from fastapi import FastAPI

from app.schemas import DatasetItem

from app.db import save_item, get_items

from app.services import stats



app = FastAPI(
    title="AI Dataset Labeling Platform",
    version="1.0.0"
)



@app.get("/")
def home():

    return {
        "message": "AI Dataset Labeling Platform"
    }



@app.post("/items")
def create_item(item: DatasetItem):

    data = item.model_dump()

    return save_item(data)



@app.get("/items")
def items():

    return get_items()



@app.get("/stats")
def statistics():

    return stats(get_items())