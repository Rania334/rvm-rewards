# ♻️ RVM Deposit & Rewards API

This is a token-authenticated Django REST API for logging recyclable material deposits and calculating reward points based on material type.

---

## 🚀 Features

- User signup & login with token authentication
- Log deposits with weight, material type, and machine ID
- Auto-calculates reward points:
  - Plastic: 1 point/kg
  - Glass: 2 points/kg
  - Metal: 3 points/kg
- User summary of total weight and points earned
- View user deposit history

---

## 🧠 Reward Logic

Handled in `utils.py`:
```python
REWARD_RATES = {
    'plastic': 1,
    'metal': 3,
    'glass': 2,
}
git clone https://github.com/rania334/rvm-rewards-api.git
cd rvm-rewards-api
