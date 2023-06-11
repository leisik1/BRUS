from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    group = db.relationship("GroupModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")