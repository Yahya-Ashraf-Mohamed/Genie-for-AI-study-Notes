def inv_data(user):
    return {
        "username":user["username"],
        "password": user["password"],
        "isPremium": user["isPremium"]
    }

def all_users(users):
    return [inv_data(user) for user in users]


#### Study Materials ####
def Material(study_material):
    return {
        "material_id": study_material["material_id"],
        "title": study_material["title"],
        "content_type": study_material["content_type"],
        "language": study_material["language"]
    }

def all_materials(study_material):
    return[Material(material) for material in study_material]
