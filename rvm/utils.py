REWARD_RATES = {
    'plastic': 1,
    'metal': 3,
    'glass': 2,
}

def calculate_reward(material, weight):
    rate = REWARD_RATES.get(material, 0)
    return weight * rate
