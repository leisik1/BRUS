from db import db

class GroupModel(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="group", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="group", lazy="dynamic")