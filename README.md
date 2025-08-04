# RVM Deposit & Rewards API

This is a token-authenticated Django REST API for logging recyclable material deposits and calculating reward points based on material type.
Live API: https://rvm-rewards.onrender.com


---

## Features

- User signup & login with token authentication
- Log deposits with weight, material type, and machine ID
- Auto-calculates reward points:
  - Plastic: 1 point/kg
  - Glass: 2 points/kg
  - Metal: 3 points/kg
- User summary of total weight and points earned
- View user deposit history

---

## Reward Logic

Handled in `utils.py`:

```python
REWARD_RATES = {
    'plastic': 1,
    'metal': 3,
    'glass': 2,
} -
```

##  Authentication

Token-based authentication using `rest_framework.authtoken`.

Protected endpoints use:

- `TokenAuthentication`
- `IsAuthenticated`

##  API Endpoints
### Base URL: https://rvm-rewards.onrender.com
### 1. `POST /signup/`
Registers a new user.
- Accepts `username`, `email`, and `password`.
- Returns an authentication token and user data.

### 2. `POST /login/`
Logs in a registered user.
- Accepts `username` and `password`.
- Verifies credentials.
- Returns authentication token and user data.

### 3. `POST /deposit/`
Logs a recyclable material deposit.
- Requires authentication (`TokenAuthentication`, `IsAuthenticated`).
- Accepts `weight`, `material`, and `machine_id`.
- Saves deposit and calculates reward points.
- Returns deposit details and points earned.

### 4. `GET /summary/`
Returns a summary for the authenticated user.
- Requires authentication.
- Returns total recycled weight, total points earned, and deposit count.

### 5. `GET /user_deposits/`
Returns paginated list of all deposits by the authenticated user.
- Requires authentication.
- Uses page size of 10 by default.
- Returns latest deposits with full details.


##  How to Run

###  Clone the repository
```bash
git clone https://github.com/Rania334/rvm-rewards.git
cd rvm-rewards
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
