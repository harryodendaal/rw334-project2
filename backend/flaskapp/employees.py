import json
import csv

from .auth import token_required
from flask import Blueprint, jsonify, request
from .database.models.enron import Employee, Recipient, Message
from .database.models import db
employees = Blueprint('employees', __name__)


@employees.route('/allemployees', methods=['GET'])
@token_required
def get_all_employees(current_user):
    employees = Employee.query.all()
    all_employees: list = []
    for e in employees:
        all_employees.append({
            "eid": e.eid,
            "firstname": e.firstname,
            "lastname": e.lastname,
            "email_id": e.email_id
        })
    return json.dumps(all_employees), 200


@employees.route('/get_employee_info', methods=['POST'])
@token_required
def get_employee_info(current_user):
    eid = request.get_json()['data']['eid']

    employee = Employee.query.filter_by(eid=eid).all()[0]
    # number of emails sent in total

    messages = Message.query.all()
    mid_list: list = []
    emails_sent: int = 0
    for message in messages:
        if message.sender == employee.email_id:
            mid_list.append(message.mid)
            emails_sent = emails_sent + 1

    list_of_employee_dict = []
    recipients = Recipient.query.all()
    for r in recipients:
        if r.mid in mid_list:
            if r.rvalue.find('enron') != -1:
                if len(list_of_employee_dict) == 0:
                    list_of_employee_dict.append({
                        "employee": r.rvalue,
                        "messages_sent": 1
                    })
                elif not any(a['employee'] == r.rvalue for a in list_of_employee_dict):
                    # does not exist
                    list_of_employee_dict.append({
                        'employee': r.rvalue,
                        'messages_sent': 1
                    })
                else:
                    # does exist
                    # both methods take equally long so there was not reason to get fancy : []
                    # method 1
                    # d = next(
                    #     item for item in list_of_employee_dict if item['employee'] == r.rvalue)
                    # d['messages_sent'] += 1
                    # methods 2
                    for x in list_of_employee_dict:
                        if x['employee'] == r.rvalue:
                            x['messages_sent'] += 1

    # now just need to extract the top 5
    # i dont understand this code hav
    newList = sorted(list_of_employee_dict,
                     key=lambda k: k['messages_sent'], reverse=True)
    if len(newList) > 5:
        newnewlist = newList[:5]
    else:
        newnewlist = newList
    newnewlist.append({"totalMessages": emails_sent})
    return json.dumps(newnewlist), 200

    # query firstname
    # query lastname
    # add two together

    # query messages, see how many messages has sender field that's equal to employee email_id field.
    # make list of all employees this employee has sent emails to
    # retrieve top 5 employees based on amount of emails.
    employee = Employee.query.filter_by(eid=id).first()
    messages = Message.query.filter_by(sender=employee.email_id)
    messages_amount = 0
    recipient_employees = {}

    for message in messages:
        messages_amount += 1
        recipient = Recipient.query.filter_by(mid=message.mid).first()
        if recipient.eid:
            if recipient_employees[recipient.eid]:
                recipient_employees[recipient.eid] = recipient_employees[recipient.eid] + 1
            else:
                recipient_employees[recipient.eid] = 1

    sorted_keys = sorted(recipient_employees, key=recipient_employees.get)

    j = 0
    top_5 = {}
    for w in sorted_keys:
        if j == 5:
            break
        top_5[w] = recipient_employees[w]
        j += 1

    return jsonify(top_5)



@employees.route('/fillrelationships', methods=['GET'])
def fill_recipient_relationships():
    recipients = Recipient.query.all()

    print('fill relationships')
    i = 0
    for recipient in recipients:
        employee = Employee.query.filter_by(email_id=recipient.rvalue).first()
        if employee:
            if recipient.eid == None:
                recipient.eid = employee.eid
                if i % 5000 == 0:
                    db.session.commit()
                    print(recipient)
                i += 1
    db.session.commit()
    

    return json.dumps({}), 200


@employees.route('/createdata', methods=['GET'])
@token_required
def create_data(current_user):
    print('create data')
    # with open('EmployeeList.csv') as f:
    #     reader = csv.reader(f)
    #     row_number = 0
    #     for row in reader:
    #         # print(row[0])
    #         if row_number != 0:
    #             e = Employee(row[0],row[1],row[2],row[3])
    #             # print('whatsupp')
    #             db.session.add(e)
    #         row_number += 1
    #         db.session.commit()

    print('dunzos with employees')
    with open('Message.csv') as f:
        reader = csv.reader(f)
        row_number = 0

        for row in reader:
            if row_number != 0:
                m = Message(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                )
                db.session.add(m)
                if row_number % 10000 == 0:
                    db.session.commit()
                    print(m)
            row_number += 1

    with open('RecipientInfo.csv') as f:
        reader = csv.reader(f)
        row_number = 0

        for row in reader:
            if row_number != 0:
                r = Recipient(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                )
                db.session.add(r)
                if row_number % 10000 == 0:
                    db.session.commit()
            row_number += 1
    return json.dumps({}), 200
