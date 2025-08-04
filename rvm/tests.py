from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Deposit

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='rania', password='rania123',email='rania@gmail.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='token '+ self.token.key)

#signup
    def test_signup(self):
        res = self.client.post('/signup/', {
            'username': 'user',
            'password': 'userpass',
            'email': 'user@gmail.com'
        })
        self.assertEqual(res.status_code,200)
        self.assertIn('token', res.data)

    def test_signupMissing(self):
        res = self.client.post('/signup/', {
            'username': 'missing'})
        self.assertEqual(res.status_code,400)
        self.assertIn('error', res.data)
        
#login
    def test_login(self):
        res = self.client.post('/login/', {
            'username': 'rania',
            'password': 'rania123'})
        self.assertEqual(res.status_code,200)
        self.assertIn('token', res.data)

    def test_loginWrong_pass(self):
        res = self.client.post('/login/', {
            'username': 'rania',
            'password': 'wrong'})
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.data['error'], 'Incorrect password')

    def test_login_UserNotFound(self):
        res = self.client.post('/login/',{
            'username': 'nouser',
            'password': 'nopass'}
                               )
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['error'], 'User not found')
        
#deposit
    def test_deposit_ok(self):
        res = self.client.post('/deposit/', {
            'weight': 2,
            'material': 'plastic',
            'machine_id': 'x1'
        })
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['points_earned'],2)

    def test_deposit_missing(self):
        res = self.client.post('/deposit/', {
            'weight': 1,
            'machine_id': 'x2'
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn('error', res.data)

    def test_deposit_no_auth(self):
        self.client.credentials()
        res = self.client.post('/deposit/', {
            'weight': 1.5,
            'material': 'metal',
            'machine_id': 'x3'
        })
        self.assertEqual(res.status_code, 401)
        
#summary
    def test_summary(self):
        Deposit.objects.create(user=self.user, weight=1, material='metal', machine_id='a')
        Deposit.objects.create(user=self.user, weight=2, material='glass', machine_id='b')
        res = self.client.get('/summary/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['total_weight'],3)
        self.assertEqual(res.data['total_points'],7)

    def test_summary_no_auth(self):
        self.client.credentials()
        res = self.client.get('/summary/')
        self.assertEqual(res.status_code,401)
        
#user_deposits
    def test_user_deposits_pagination(self):
        for i in range(12):
            Deposit.objects.create(user=self.user, weight=1, material='glass', machine_id=f'm{i}')
        res = self.client.get('/user_deposits/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['results']),10)

    def test_user_deposits_no_auth(self):
        self.client.credentials()
        res = self.client.get('/user_deposits/')
        self.assertEqual(res.status_code,401)
