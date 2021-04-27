from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from werkzeug.exceptions import Unauthorized
from ....user.application.user_dto import UserDTO
from ...application.sn_group_dto import SNGroupDTO
from ..service.sn_group_service import SocialNetworkGroupService

snGroupFlaskBlueprint = Blueprint('Social Network Group', __name__, url_prefix="/sn/group")


@snGroupFlaskBlueprint.route('/create/', methods=["POST"])
@jwt_required()
def create_sn_group(**kw):
    user: UserDTO = get_current_user()
    if not user:
        raise Unauthorized("Only logged users can create Social Network Groups")
    snGroupDto: SNGroupDTO = request.json.get("snGroup", False)
    if user["userid"] != snGroupDto["userid"]:
        raise Unauthorized("Can not create groups for another user")
    snGroupService: SocialNetworkGroupService = SocialNetworkGroupService()
    snGroupService.createSNGroup(snGroupDto)
    return jsonify({"status": "ok"}), 200


@snGroupFlaskBlueprint.route("/user/<string:userid>/", methods=["GET"])
@jwt_required()
def get_all_by_user(userid: str, **kw):
    user: UserDTO = get_current_user()
    if not user:
        raise Unauthorized("Only logged users can get Social Network Groups")
    if user["userid"] != userid:
        raise Unauthorized("Can not get groups from another user")
    snGroupService: SocialNetworkGroupService = SocialNetworkGroupService()
    groups = snGroupService.getByUserId(userid)
    return jsonify(groups), 200
