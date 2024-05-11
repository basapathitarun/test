import cv2
from pyzbar.pyzbar import decode
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import Items,Cart,Purchase
from schemas import CartRequest
from pydantic import BaseModel
import models




# Create database tables
models.base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/AddCart/')
def add_to_cart(cart_item: dict, db: Session = Depends(get_db)):
    barcode = cart_item.get("cart_item")

    # Check if the item exists in the database
    item = db.query(models.Items).filter(models.Items.Item_Id == barcode).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Add the item to the cart
    db_cart_item = models.Cart(Item_ID=barcode)
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)

    # Fetch updated cart items
    cart_items = db.query(models.Items).join(models.Cart, models.Items.Item_Id == models.Cart.Item_ID).all()

    return {'cart_items': cart_items}


@app.get('/Cart/')
def ListCart(db: Session =Depends(get_db)):
    cartItem = db.query(Cart).all()
    cartElement = []
    for cart in cartItem:
        items  = db.query(Items).filter(Items.Item_Id == cart.Item_ID).first()
        cartElement.append(items)
    return cartElement


@app.get('/purchase/')
async def add_to_DB(db: Session = Depends(get_db)):
    # Fetch all items from the Cart table
    cart_items = db.query(Cart).all()
    if not cart_items:
        raise HTTPException(status_code=404,detail="No  items found in the Cart")

    # Extract item Id's from the fetched items
    item_ids = [item.Item_ID for item in cart_items]

    # Insert all item IDs into the Purchase table
    for item_id in item_ids:
        db_item = Purchase(BarcodeID=item_id)
        db.add(db_item)

    db.commit()

    db.query(Cart).delete()

    db.commit()

    return {"message": "Items purchased successfully and removed from cart"}

@app.get('/total/')
def getTotalCost(db:Session =Depends(get_db)):

    purchase = db.query(Purchase).all()
    TotalCost = 0
    if purchase:
        for ID in purchase:
            items =db.query(Items).filter(Items.Item_Id==ID.BarcodeID).first()
            if items:
                TotalCost+=items.Price

        return {'TotalCost':TotalCost}


@app.get('/clearPurchase/')
def deletePurchase(db:Session = Depends(get_db)):
    purchase = db.query(Purchase).delete()
    db.commit()
    if purchase:
        return "success"


@app.get('/')
def index():
    return {"response":"about"}

@app.get('/opencv')
def scan_barcode_opencv():
    # capture webcam
    cap = cv2.VideoCapture(0)

    barcode_detected = False

    while cap.isOpened():
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        detected_barcode = decode(frame)

        if not detected_barcode:
            print("No barcode detected")
        else:
            for barcode in detected_barcode:
                if barcode.data:
                    text_barcode = barcode.data.decode('utf-8')
                    cv2.putText(frame, str(barcode.data), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 2)
                    barcode_detected = True
                    break

        if barcode_detected:
            cap.release()
            cv2.destroyAllWindows()
            return {'text_barcode':text_barcode}

        cv2.imshow('scanner', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return {'text_barcode': None}


