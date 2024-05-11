from sqlalchemy import Column,Integer,String,ForeignKey
from database import base

class Items(base):
    __tablename__ = "Items"

    Item_Id = Column(String,primary_key=True)
    ItemName = Column(String,unique=True)
    Price = Column(Integer)

    # Cart = relationship("Cart",uselist=False,back_populates="Items")

class Cart(base):
    __tablename__ ="Cart"

    CartId = Column(Integer,primary_key=True,autoincrement=True)
    Item_ID = Column(String,ForeignKey("Items.Item_Id"))
    # count = Column(Integer,default=0)

class Purchase(base):
    __tablename__ = "Purchase"

    purchaseID = Column(Integer,primary_key=True,autoincrement=True)
    BarcodeID = Column(String,ForeignKey("Items.Item_Id"))