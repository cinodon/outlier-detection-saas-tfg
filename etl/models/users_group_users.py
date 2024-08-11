from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class UsersGroupUser(Base):
    __tablename__ = 'UsersGroupUsers'
    __table_args__ = {'schema': 'api'}

    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    UserId = Column(UUID(as_uuid=True), ForeignKey('api.Users.Id'))
    UsersGroupId = Column(UUID(as_uuid=True), ForeignKey('api.UsersGroups.Id'))

    # Relations
    user = relationship("User", back_populates="users_group_users")

