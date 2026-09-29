import pytest
import database.users as u
import database.connection as c
import security as sc
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def session():
    return next(c.get_session())

@pytest.fixture
def create_token(session):
    user = u.get_user_by_id(id=3, session=session)
    token = sc.create_token(user)
    return token

def test_access_without_token(): 
    response = client.get("/predict/1") 
    assert response.status_code == 401

def test_extra_field_body(create_token):
    response = client.post( "/predict", headers={ "Authorization": f"Bearer {create_token}" }, 
                           json={ "text": "Texto Aleatório", "campo_extra": "não deveria existir" } 
    ) 
    assert response.status_code == 422

def test_check_another_user_resource(create_token):
    response = client.get( "/predict/3", headers={ "Authorization": f"Bearer {create_token}" }) 
    assert response.status_code == 403


