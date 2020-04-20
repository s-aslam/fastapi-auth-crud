from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from project.base.models import BaseModel


class Item(BaseModel):
    title = Column(String(50), unique=True)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="items")

    def __repr__(self):
        return self.title
