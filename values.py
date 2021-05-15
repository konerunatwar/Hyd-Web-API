from pydantic import BaseModel

class value(BaseModel):
    property_size: int
    bhk: int
    property_age: int
    gym: int
    lift: int
    swimmingPool: int
    location: str
