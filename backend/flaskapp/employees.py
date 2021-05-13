import json
from .auth import token_required
from flask import Blueprint
from .database.models.employes import employeList
employees = Blueprint('employees', __name__)


@employees.route('/allemployees', methods=['GET'])
@token_required
def get_all_employees(current_user):
    employees = employeList.query.all()
    all_employees: list = []
    for e in employees:
        all_employees.append({
            "eid": e.eid,
            "firstname": e.firstname,
            "lastname": e.lastname,
            "email_id": e.email_id
        })

    return json.dumps(all_employees), 200
