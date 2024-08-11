from sqlalchemy import Column, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from .base import Base

class PermissionLevel(Base):
    __tablename__ = 'PermissionLevels'
    __table_args__ = {'schema': 'api'}

    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    IsPrivileged = Column(Boolean)

    user_app_roles = relationship("UserAppRole", back_populates="permission_level")