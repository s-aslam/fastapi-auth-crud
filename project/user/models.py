from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from project.base.models import BaseModel
from project.config import PASSWORD_ENCRYPTION


class User(BaseModel):
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(50), unique=True)
    username = Column(String(50), unique=True)
    password = Column(String(512), unique=True)
    last_login = Column(DateTime(timezone=True), nullable=True)

    items = relationship("Item", back_populates="user")

    def __repr__(self):
        return self.username

    def verify_password(self, password):
        return PASSWORD_ENCRYPTION.verify(password, self.password)
