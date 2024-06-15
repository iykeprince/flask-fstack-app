import unittest
from main import create_app
from config import TestConfig
from exts import db

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(TestConfig)
        self.client=self.app.test_client()        
        with self.app.app_context():
            # db.init_app(self.app)
            db.create_all()


    def test_hello_world(self):
        hello_response=self.client.get('/recipes/hello')
        json=hello_response.get_json()
        self.assertEqual(json, {"hello": "Hello world"})
        self.assertEqual(hello_response.status_code, 200)

    def test_signup(self):
        signup_response=self.client.post('/auth/signup',
            json={"username": "testuser", "email": "testuser@gmail.com", "password": "password123"},
            
            )
        status_code=signup_response.status_code
        self.assertEqual(status_code, 201)

    def test_login(self):
        signup_response=self.client.post('/auth/signup',
            json={"username": "testuser", "email": "testuser@gmail.com", "password": "password123"},
            )
        login_response=self.client.post('/auth/login', json={"username": "testuser", "password": "password123"})
        status_code=login_response.status_code
        self.assertEqual(status_code, 200)
    
    def test_get_all_recipes(self):
        """Test getting all recipes"""
        response=self.client.get('/recipes/')
        status_code=response.status_code
        json=response.get_json()
        # print(json)
        self.assertEqual(status_code, 200)
        
    def test_get_one_recipe(self):
        id=1
        response=self.client.get(f'/recipes/{id}')
        status_code=response.status_code
        self.assertEqual(status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()