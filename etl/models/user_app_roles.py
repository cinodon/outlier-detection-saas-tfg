from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class UserAppRole(Base):
    __tablename__ = 'UserAppRoles'
    __table_args__ = {'schema': 'api'}

    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    UserId = Column(UUID(as_uuid=True), ForeignKey('api.Users.Id'))
    WorkAppId = Column(UUID(as_uuid=True), ForeignKey('api.WorkApps.Id'))
    PermissionLevelId = Column(UUID(as_uuid=True), ForeignKey('api.PermissionLevels.Id'))

    # Relations
    user = relationship("User", back_populates="user_app_roles")
    workapp = relationship("WorkApp", back_populates="user_app_roles")
    permission_level = relationship("PermissionLevel", back_populates="user_app_roles")

