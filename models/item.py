from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), unique=False, nullable=False)
    group = db.relationship("GroupModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
