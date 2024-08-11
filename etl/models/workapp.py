from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class WorkApp(Base):
    __tablename__ = 'WorkApps'
    __table_args__ = {'schema': 'api'}

    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    WorkAppCategoryId = Column(Integer)

    user_app_roles = relationship("UserAppRole", back_populates="workapp")