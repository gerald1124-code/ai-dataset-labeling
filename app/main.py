from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field

app=FastAPI(title="AI Dataset Labeling Platform")
projects=[]; items=[]; annotations={}

class Project(BaseModel):
    name:str=Field(min_length=1)
    labels:list[str]=Field(min_length=2)
class Item(BaseModel):
    external_id:str=Field(min_length=1)
    text:str=Field(min_length=1)
class Annotation(BaseModel):
    label:str
    notes:str=""
    annotator:str=""

@app.post("/projects")
def create_project(p:Project):
    row={"id":len(projects)+1,**p.model_dump()}; projects.append(row); return row

@app.post("/projects/{project_id}/items")
def add_item(project_id:int,i:Item):
    if not any(p["id"]==project_id for p in projects): raise HTTPException(404,"Project not found")
    row={"id":len(items)+1,"project_id":project_id,**i.model_dump()}; items.append(row); return row

@app.put("/items/{item_id}/annotation")
def annotate(item_id:int,a:Annotation):
    item=next((x for x in items if x["id"]==item_id),None)
    if not item: raise HTTPException(404,"Item not found")
    project=next(x for x in projects if x["id"]==item["project_id"])
    if a.label not in project["labels"]: raise HTTPException(400,"Invalid label")
    annotations[item_id]=a.model_dump(); return {"saved":True}

@app.get("/projects/{project_id}/items")
def project_items(project_id:int):
    return [{**x,**annotations.get(x["id"],{})} for x in items if x["project_id"]==project_id]

@app.get("/projects/{project_id}/stats")
def stats(project_id:int):
    rows=project_items(project_id); done=[r for r in rows if "label" in r]; dist={}
    for r in done: dist[r["label"]]=dist.get(r["label"],0)+1
    return {"total":len(rows),"annotated":len(done),
            "progress":round(100*len(done)/len(rows),2) if rows else 0,
            "distribution":dist}
