from pydantic import BaseModel


class CartRequest(BaseModel):
    item_ids: list[str]