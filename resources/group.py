from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import GroupModel, UserModel
from schemas import GroupSchema


blp = Blueprint("Groups", "groups", description="Operations on groups")


@blp.route("/group/<int:group_id>")
class Group(MethodView):
    @blp.response(200, GroupSchema)
    def get(self, group_id):
        group = GroupModel.query.get_or_404(group_id)
        return group

    def delete(self, group_id):
        group = GroupModel.query.get_or_404(group_id)
        db.session.delete(group)
        db.session.commit()
        return {"message": "Group deleted"}, 200
    

@blp.route("/group/<string:name>")
class Group(MethodView):
    @blp.response(200, GroupSchema)
    def get(self, name):
        group = GroupModel.query.filter(GroupModel.name == name).first()
        return group
    
@blp.route("/localgroup")
class GroupList(MethodView):
    @blp.response(200, GroupSchema(many=True))
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        if not jwt.get("role") == "local_admin" or jwt.get("role") == "admin":
            abort(401, message="Admin privilege required")
        owner = UserModel.query.get_or_404(jwt.get("sub"))
        print(owner.username)
        return GroupModel.query.filter(GroupModel.owner == owner.username)

@blp.route("/group")
class GroupList(MethodView):
    @blp.response(200, GroupSchema(many=True))
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        if not jwt.get("role") == "admin":
            abort(401, message="Admin privilege required")
        return GroupModel.query.all()

    @blp.arguments(GroupSchema)
    @blp.response(201, GroupSchema)
    @jwt_required()
    def post(self, group_data):
        jwt = get_jwt()
        if not jwt.get("role") == "admin":
            abort(401, message="Admin privilege required")
        group = GroupModel(**group_data) #TODO Obsługa wyjątku jak owner nie istnieje
        try:
            db.session.add(group)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A group with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the group.")

        return group