from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import WalkOrder, SessionLocal
from schemas import WalkOrderCreate
from datetime import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/orders/", response_class=HTMLResponse)
def get_orders(date: str, request: Request, db: Session = Depends(get_db)):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    orders = db.query(WalkOrder).filter(WalkOrder.walk_date == date_obj).all()

    if not orders:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": "No orders found for this date.",
            "orders": []
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "orders": [order.to_dict() for order in orders],
        "selected_date": date
    })


@app.post("/orders/", response_class=HTMLResponse)
async def create_order(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    try:
        # Преобразование данных формы в объект WalkOrderCreate
        order = WalkOrderCreate(
            apartment_number=form_data.get("apartment_number"),
            pet_name=form_data.get("pet_name"),
            pet_breed=form_data.get("pet_breed"),
            walk_date=datetime.strptime(
                form_data.get("walk_date"), "%Y-%m-%d"),
            walk_time=datetime.strptime(
                form_data.get("walk_time"), "%H:%M").time()
        )

        walk_time = order.walk_time
        walk_date = order.walk_date
        orders = db.query(WalkOrder).filter(WalkOrder.walk_date == walk_date).filter(
            WalkOrder.walk_time == walk_time).all()

        if len(orders) >= 2:
            raise HTTPException(
                status_code=400, detail="This time slot is fully booked.")

        new_order = WalkOrder(
            apartment_number=order.apartment_number,
            pet_name=order.pet_name,
            pet_breed=order.pet_breed,
            walk_date=walk_date,
            walk_time=walk_time
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return templates.TemplateResponse("success.html", {"request": request, "message": "Order created successfully!"})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
