import json

from flask_jwt_extended import create_access_token

from ..models import User
from ..messages import *
from .helpers import (get_access_token_header, create_user, AuthMock,
                      create_authority, authorize_user)
from project.apps.utils import get_app_context
from tests.helpers import *
from tests.client import client


USERS_PATH = "project.apps.users_app"


def test_login_badparameter(client):
    resp = client.post("/auth/login/", json=dict())
    assert resp.status == BADPARAMETER


def test_login_missing_password(client):
    resp = client.post("/auth/login/", json={"username":"testuser"})
    assert resp.status == BADPARAMETER


def test_login_wrong_username(client):
    creds = {"username": "test", "password": "123"}
    resp = client.post("/auth/login/", json=creds)
    assert resp.status == WRONG_DATA


def test_login_wrong_password(client):
    create_user()
    creds = {"username": "admin", "password": "123"}
    resp = client.post("/auth/login/", json=creds)
    assert resp.status == WRONG_DATA


def test_login_change_password(client):
    create_user(password_change=True)
    creds = {"username": "admin", "password": "admin"}
    resp = client.post("/auth/login/", json=creds)
    assert resp.status == FORBIDDEN


def test_login(client):
    create_user()
    creds = {"username": "admin", "password": "admin"}
    resp = client.post("/auth/login/", json=creds)
    assert resp.status == OK


def test_logout_unauthenticated(client):
    assert client.delete("/auth/logout/").status == UNAUTHORIZED


def test_logout(client):
    header = get_access_token_header()
    resp = client.delete("/auth/logout/", headers=header)
    assert resp.status == OK  and "logout" in resp.get_json()['commands']


def test_user_list_not_authenticated(client):
    assert client.get("auth/users/").status == UNAUTHORIZED


def test_user_list_not_admin(client):
    create_user(username="testadmin", role=2, no_role=True)
    create_user(username="testuser", role=3)
    header = get_access_token_header(username="testuser")
    resp = client.get("auth/users/", headers=header)
    assert resp.status == OK and len(resp.get_json()['data']) == 1


def test_user_list_admin_role(client):
    create_user(username="testadmin", role=2, no_role=True)
    create_user(username="testuser", role=3)
    header = get_access_token_header(username="testadmin")
    resp = client.get("auth/users/", headers=header)
    result = resp.get_json()
    assert resp.status == OK and len(result['data']) == 1 and \
           not (any(x for x in result['data'] if x['username'] == 'admin'))


def test_user_list_admin_user(client):
    header = get_access_token_header()
    create_user(username="testadmin", role=2, no_role=True)
    create_user(username="testuser", role=3, no_role=True)
    resp = client.get("auth/users/", headers=header)
    result = resp.get_json()
    print(result['data'])
    assert resp.status == OK and len(result['data']) == 3 and \
           (any(x for x in result['data'] if x['username'] == 'admin'))


def test_user_detail_reporter(client):
    create_user()
    create_user(username="testadmin", role=2, no_role=True)
    create_user(username="testuser", role=3, no_role=True)
    header = get_access_token_header(username="testuser")
    resp = client.get("auth/users/testadmin/", headers=header)
    assert resp.status == FORBIDDEN and resp.get_json()['msg'] == ADMINS_ONLY


def test_user_detail_administrator_view_admin(client):
    create_user()
    create_user(username="testadmin", role=2, no_role=True)
    header = get_access_token_header(username="testadmin")
    resp = client.get("auth/users/admin/", headers=header)
    assert resp.status == FORBIDDEN and resp.get_json()['msg'] == INSUFFICIENT_CREDENTIALS


def test_user_detail_no_user_administrator(client):
    create_user()
    create_user(username="testadmin", role=2, no_role=True)
    header = get_access_token_header(username="testadmin")
    resp = client.get("auth/users/adminis/", headers=header)
    assert resp.status ==  BADPARAMETER and resp.get_json()['msg'] == NO_USER_FOUND


def test_user_detail_no_user_superuser(client):
    header = get_access_token_header()
    resp = client.get("auth/users/adminis/", headers=header)
    assert resp.status ==  BADPARAMETER and resp.get_json()['msg'] == NO_USER_FOUND


def test_user_detail_user_superuser_view_others(client):
    header = get_access_token_header()
    create_user(username="testadmin", no_role=True)
    resp = client.get("auth/users/testadmin/", headers=header)
    assert resp.status ==  OK


def test_user_detail_user_superuser(client):
    header = get_access_token_header()
    resp = client.get("auth/users/admin/", headers=header)
    assert resp.status ==  OK


def test_self_detail_no_user(client):
    header = get_access_token_header(username="tester")
    resp = client.get("auth/users/me/", headers=header)
    assert resp.status == NO_CONTENT


def test_self_detail(client):
    header = get_access_token_header()
    resp = client.get("auth/users/me/", headers=header)
    assert resp.status == OK and resp.get_json()['username'] == "admin"


def test_register_user_empty(client):
    header = get_access_token_header()
    assert client.post("auth/users/", json=dict(), headers=header).status == BADPARAMETER


def test_register_user_one_missing(client):
    header = get_access_token_header()
    data = {"username": "test", "password": "pass", "email": "mail"}
    assert client.post("auth/users/", json=data, headers=header).status == BADPARAMETER


def test_register_user_password_missmatch(client):
    header = get_access_token_header()
    data = {"username": "test", "password": "pass", "email": "mail", "role": 2,
            "confirm_password": "pas"}
    resp =  client.post("auth/users/", json=data, headers=header)
    assert resp.status == BADPARAMETER and resp.get_json()['msg'] == PASSWORD_MISSMATCH


def test_register_user_role_missmatch(client):
    header = get_access_token_header()
    data = {"username": "test", "password": "pass", "email": "mail",
            "role": "wrong", "confirm_password": "pass"}
    resp =  client.post("auth/users/", json=data, headers=header)
    assert resp.status == BADPARAMETER and resp.get_json()['msg'] == ROLE_MISSMATCH


def test_register_user_user_missmatch(client):
    header = get_access_token_header()
    data = {"username": "admin", "password": "pass", "email": "mail",
            "role": "Administrator", "confirm_password": "pass"}
    resp =  client.post("auth/users/", json=data, headers=header)
    assert resp.status == DUPLICATE and resp.get_json()['msg'] == USERNAME_ALREADY_EXISTS


def test_register_user_email_missmatch(client):
    header = get_access_token_header()
    data = {"username": "sam", "password": "pass", "email": "mail",
            "role": "Administrator", "confirm_password": "pass"}
    resp =  client.post("auth/users/", json=data, headers=header)
    assert resp.status == BADPARAMETER and resp.get_json()['msg'] == EMAIL_MISSMATCH


def test_register_user(client):
    header = get_access_token_header()
    data = {"username": "test", "password": "pass", "email": "mail@mail.com",
            "role": "Administrator", "confirm_password": "pass"}
    resp =  client.post("auth/users/", json=data, headers=header)
    assert resp.status == INSERTED


def test_remove_user_not_admin(client):
    create_user()
    create_user(username="tester", role=3, no_role=True)
    header = get_access_token_header(username="tester")
    resp = client.delete("auth/users/test/", headers=header)
    assert resp.status == FORBIDDEN and resp.get_json()['msg'] == ADMINS_ONLY


def test_remove_user_no_user(client):
    create_user()
    create_user(username="tester", role=2, no_role=True)
    header = get_access_token_header(username="tester")
    resp = client.delete("auth/users/test/", headers=header)
    assert resp.status == NO_CONTENT


def test_remove_admin_user(client):
    create_user()
    create_user(username="tester", role=2, no_role=True)
    header = get_access_token_header(username="tester")
    resp = client.delete("auth/users/admin/", headers=header)
    assert resp.status == FORBIDDEN


def test_remove_user(client):
    create_user()
    create_user(username="tester", role=2, no_role=True)
    header = get_access_token_header(username="admin")
    resp = client.delete("auth/users/tester/", headers=header)
    assert resp.status == OK


def test_edit_user_no_user(client):
    header = get_access_token_header()
    resp = client.put("auth/users/tester/", headers=header, json=dict())
    assert resp.status == BADPARAMETER and resp.get_json()['msg'] == NO_USER_FOUND


def test_edit_user_reporter_edit_someone_else(client):
    create_user()
    create_user(username="tester", role=3, no_role=True)
    header = get_access_token_header(username="tester")
    resp = client.put("auth/users/admin/", headers=header, json=dict())
    assert resp.status == FORBIDDEN and resp.get_json()['msg'] == ADMINS_ONLY


def test_edit_user_admins_edit_administrator(client):
    create_user()
    create_user(username="tester", role=2, no_role=True)
    header = get_access_token_header(username="tester")
    resp = client.put("auth/users/admin/", headers=header, json=dict())
    assert resp.status == FORBIDDEN and resp.get_json()['msg'] == INSUFFICIENT_CREDENTIALS


def test_edit_user_reporter_change_role(client):
    create_user()
    create_user(username="tester", role=3, no_role=True)
    header = get_access_token_header(username="tester")
    resp = client.put("auth/users/tester/", headers=header, json={"role": "Administrator"})
    assert resp.status == FORBIDDEN and resp.get_json()['msg'] == ADMINS_ONLY


def test_edit_user_admin_change_their_role(client):
    create_user()
    create_user(username="tester", role=2, no_role=True)
    header = get_access_token_header(username="tester")
    resp = client.put("auth/users/tester/", headers=header, json={"role": "Reporter"})
    assert resp.status == FORBIDDEN and resp.get_json()['msg'] == SOMEONE_ELSE_DO_IT


def test_edit_user_no_role(client):
    header = get_access_token_header()
    create_user(username="tester", role=2, no_role=True)
    resp = client.put("auth/users/tester/", headers=header, json={"role": "NoMatch"})
    assert resp.status == BADPARAMETER and resp.get_json()['msg'] == ROLE_MISSMATCH


def test_edit_user_change_role(client):
    header = get_access_token_header()
    create_user(username="tester", role=2, no_role=True)
    resp = client.put("auth/users/tester/", headers=header, json={"role": "Reporter"})
    header = get_access_token_header(username="tester")
    result = client.get("auth/users/me/", headers=header)
    assert resp.status == INSERTED and result.get_json()['role'] == "Reporter"


def test_edit_user_change_pass_no_match(client):
    create_user(username="tester", role=2)
    header = get_access_token_header(username="tester")
    data = {"password": "123", "confirm_password": "321"}
    resp = client.put("auth/users/tester/", headers=header, json=data)
    assert resp.status == BADPARAMETER and resp.get_json()['msg'] == PASSWORD_MISSMATCH


def test_edit_user_change_pass_bad_current(client):
    create_user(username="tester", password="321", role=2)
    header = get_access_token_header(username="tester")
    data = {"password": "123", "confirm_password": "123", "current_password": "432"}
    resp = client.put("auth/users/tester/", headers=header, json=data)
    assert resp.status == BADPARAMETER and resp.get_json()['msg'] == WRONG_OLD_PASSWORD


def test_edit_user_change_pass_new_and_current_same(client):
    create_user(username="tester", password="321", role=2)
    header = get_access_token_header(username="tester")
    data = {"password": "321", "confirm_password": "321", "current_password": "321"}
    resp = client.put("auth/users/tester/", headers=header, json=data)
    assert resp.status == BADPARAMETER and resp.get_json()['msg'] == SAME_OLD_NEW_PASSWORD


def test_edit_user_change_pass(client):
    create_user(username="tester", password="321", role=2)
    header = get_access_token_header(username="tester")
    data = {"password": "123", "confirm_password": "123", "current_password": "321"}
    resp = client.put("auth/users/tester/", headers=header, json=data)
    assert resp.status == INSERTED


def test_edit_user_change_pass_force_password(client):
    create_user(username="tester", password="321", password_change=True, role=2)
    header = get_access_token_header(username="tester")
    data = {"password": "123", "confirm_password": "123", "current_password": "321"}
    resp = client.put("auth/users/tester/", headers=header, json=data)
    result = client.get("auth/users/me/", headers=header)
    assert resp.status == INSERTED and result.get_json()['force_password_change'] == False


def test_edit_user_change_firstname(client):
    header = get_access_token_header()
    data = {"last_name": "admin"}
    resp = client.put("auth/users/admin/", headers=header, json=data)
    assert resp.status == INSERTED


def test_edit_user_change_lastname(client):
    header = get_access_token_header()
    data = {"last_name": "admin"}
    resp = client.put("auth/users/admin/", headers=header, json=data)
    assert resp.status == INSERTED
