from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from werkzeug.exceptions import Unauthorized
from ...application.brand_dto import BrandDTO
from ..service.brand_service import BrandService

brandFlaskBlueprint = Blueprint('Brand', __name__, url_prefix="/brand")


@brandFlaskBlueprint.route('/create/', methods=["POST"])
@jwt_required()
def create_brand(**kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can create Brands")
    brandDto: BrandDTO = request.json.get("brand", False)
    if currentUserId != brandDto["userId"]:
        raise Unauthorized("Can not create brands for another user")
    brandService: BrandService = BrandService()
    brandService.createBrand(brandDto)
    return jsonify({"status": "ok"}), 200


@brandFlaskBlueprint.route("/user/<string:userId>/", methods=["GET"])
@jwt_required()
def get_all_by_user(userId: str, **kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can get Brands")
    if currentUserId != userId:
        raise Unauthorized("Can not get brands from another user")
    brandService: BrandService = BrandService()
    brands = brandService.getByUserId(userId)
    return jsonify(brands), 200
