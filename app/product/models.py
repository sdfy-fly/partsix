from datetime import datetime
import uuid

from app.db.database import Base
from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, Float, UUID, Date, CheckConstraint
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = 'product'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article = Column(String(255), unique=True)
    name = Column(Text)
    cost = Column(Float)
    discount = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    description_simple = Column(Text, nullable=True)
    published = Column(Boolean, default=False)

    images = relationship("ProductImages", back_populates="product")
    attributes = relationship("ProductAttributes", back_populates="product")
    reviews = relationship("ProductReview", back_populates="product")
    category_id = Column(Integer, ForeignKey('category.id'))

    __table_args__ = (
        CheckConstraint('cost > 0', name='check_price_positive'),
    )


class ProductImages(Base):
    __tablename__ = 'product_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Text)

    product_id = Column(UUID, ForeignKey('product.id', ondelete='CASCADE'))
    product = relationship("Product", back_populates="images")


class ProductAttributes(Base):
    __tablename__ = 'product_attributes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    text = Column(Text)

    product_id = Column(UUID, ForeignKey('product.id', ondelete='CASCADE'))
    product = relationship('Product', back_populates="attributes")


class ProductCategories(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    name = Column(Text)


class ProductSet(Base):
    __tablename__ = 'product_set'

    id = Column(Integer, primary_key=True, autoincrement=True)
    set_id = Column(Integer)
    product_id = Column(UUID, ForeignKey('product.id'))


class ProductReview(Base):
    __tablename__ = 'product_review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=True)
    created_at = Column(Date, default=datetime.utcnow)
    rating = Column(Integer)

    # user_id = ...
    product_id = Column(UUID, ForeignKey('product.id'))
    product = relationship('Product', back_populates="reviews")

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )


models = (
    Product,
    ProductAttributes,
    ProductImages,
    ProductCategories,
    ProductSet,
    ProductReview,
)
