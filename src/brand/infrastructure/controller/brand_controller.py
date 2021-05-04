from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from werkzeug.exceptions import Unauthorized
from ....user.application.user_dto import UserDTO
from ...application.brand_dto import BrandDTO
from ..service.brand_service import BrandService

brandFlaskBlueprint = Blueprint('Brand', __name__, url_prefix="/brand")


@brandFlaskBlueprint.route('/create/', methods=["POST"])
@jwt_required()
def create_brand(**kw):
    user: UserDTO = get_current_user()
    if not user:
        raise Unauthorized("Only logged users can create Brands")
    brandDto: BrandDTO = request.json.get("brand", False)
    if user["userid"] != brandDto["userid"]:
        raise Unauthorized("Can not create brands for another user")
    brandService: BrandService = BrandService()
    brandService.createBrand(brandDto)
    return jsonify({"status": "ok"}), 200


@brandFlaskBlueprint.route("/user/<string:userid>/", methods=["GET"])
@jwt_required()
def get_all_by_user(userid: str, **kw):
    user: UserDTO = get_current_user()
    if not user:
        raise Unauthorized("Only logged users can get Brands")
    if user["userid"] != userid:
        raise Unauthorized("Can not get brands from another user")
    brandService: BrandService = BrandService()
    brands = brandService.getByUserId(userid)
    return jsonify(brands), 200
