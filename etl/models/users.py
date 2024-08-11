from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class User(Base):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'api'}

    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    TypeOfWorkId = Column(UUID(as_uuid=True), ForeignKey('api.TypeOfWorks.Id'))
    ManagerId = Column(UUID(as_uuid=True), ForeignKey('api.Users.Id'))
    RoleId = Column(UUID(as_uuid=True), ForeignKey('api.UserRoles.Id'))

    # Relations
    manager = relationship("User", remote_side=[Id])

