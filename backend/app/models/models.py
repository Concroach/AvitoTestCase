import enum

from sqlalchemy import (TIMESTAMP, Column, Enum, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship

from ..db.database import Base


class OrganizationType(enum.Enum):
    IE = 'IE'
    LLC = 'LLC'
    JSC = 'JSC'

class Employee(Base):
    __tablename__ = 'employee'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(TIMESTAMP, default="now()")
    updated_at = Column(TIMESTAMP, default="now()")

class Organization(Base):
    __tablename__ = 'organization'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    type = Column(Enum(OrganizationType))
    created_at = Column(TIMESTAMP, default="now()")
    updated_at = Column(TIMESTAMP, default="now()")

class OrganizationResponsible(Base):
    __tablename__ = 'organization_responsible'
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey('organization.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('employee.id', ondelete='CASCADE'))

class Tender(Base):
    __tablename__ = 'tender'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    service_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    version = Column(Integer, default=1)
    organization_id = Column(Integer, ForeignKey('organization.id', ondelete='CASCADE'))
    creator_username = Column(String(50), ForeignKey('employee.username', ondelete='SET NULL'))
    created_at = Column(TIMESTAMP, default="now()")
    updated_at = Column(TIMESTAMP, default="now()")

class Bid(Base):
    __tablename__ = 'bid'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), nullable=False)
    version = Column(Integer, default=1)
    tender_id = Column(Integer, ForeignKey('tender.id', ondelete='CASCADE'))
    organization_id = Column(Integer, ForeignKey('organization.id', ondelete='CASCADE'))
    creator_username = Column(String(50), ForeignKey('employee.username', ondelete='SET NULL'))
    created_at = Column(TIMESTAMP, default="now()")
    updated_at = Column(TIMESTAMP, default="now()")

class Review(Base):
    __tablename__ = 'review'
    
    id = Column(Integer, primary_key=True, index=True)
    bid_id = Column(Integer, ForeignKey('bid.id', ondelete='CASCADE'))
    author_username = Column(String(50), ForeignKey('employee.username', ondelete='CASCADE'))
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default="now()")
