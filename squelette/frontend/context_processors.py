def add_menu_to_context(request):
    return {"menu": [
    {"name": "Connexion", "url": "front_login", "logged": False},
    {"name": "Ma fiche", "url": "front_synthesis", "logged": True},    
    {"name": "Conditions de diplomation", "url": "front_obligations", "logged": True},
    {"name": "Compétences", "url": "front_skills", "logged": True},
    {"name": "UEs", "url": "front_courses", "logged": True},
    {"name": "Déconnexion", "url": "front_logout", "logged": True},
]}
