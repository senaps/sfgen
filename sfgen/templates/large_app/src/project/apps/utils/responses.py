from flask import jsonify


def make_response(data=None, status_code=200, headers=None):
    if not headers:
        resp_headers = {"msg": "SUCCESS"}
    return jsonify(data), status_code, headers


def make_pagination(data):
    return {"pagination": {"page": data.page,
            "weight": data.per_page,
            "nex_page": data.has_next,
            "total": data.total}}