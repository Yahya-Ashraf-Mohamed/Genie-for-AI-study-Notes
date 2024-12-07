def inv_data(user):
    return {
        "username":user["username"],
        "password": user["password"],
        "isPremium": user["isPremium"]
    }

def all_users(users):
    return [inv_data(user) for user in users]