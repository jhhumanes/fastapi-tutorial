from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


# The API
app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "year": "Year 12"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

# Endpoints
@app.get("/")
def index():
    return {"name": "Primer Dato"}

# Path parameters
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(None, description="Id del estudiante", gt=0, lt=3)):
    return students[student_id]

# Query parameters
# El * permite poner parámetros obligatorios después de parámetros opcionales en la firma de la función.
@app.get("/get-by-name")
def get_student(*, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "No hay datos"}

# Combine path and query parameters
@app.get("/get-by-name-combined/{student_id}")
def get_student_combined(*, student_id: int, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "No hay datos"}

# Post
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "El ID del alumno ya existe"}

    students[student_id] = student
    return students[student_id]

#Put
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "El ID del alumno no existe"}

    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.year != None:
        students[student_id].year = student.year
    return students[student_id]

# Delete
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "El ID del alumno no existe"}

    del students[student_id]
    return {"Message": "Alumno eliminado"}
