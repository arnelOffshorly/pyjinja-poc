# routes/forms.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class UserForm(BaseModel):
    name: str
    email: EmailStr

@router.get("/form")
async def get_form(request: Request):
    # Initial form data (could come from database)
    initial_data = {
        "name": "",
        "email": ""
    }
    return templates.TemplateResponse(
        "form.html",
        {"request": request, "initial_data": initial_data}
    )

@router.post("/submit")
async def submit_form(form_data: UserForm):
    # Here you would typically save to database
    # For this example, we'll just return success
    return JSONResponse({
        "success": True,
        "redirect": "/success"
    })