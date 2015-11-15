from app import db, User, Handle
import json

def add_user(username, password):
    user = User(username = username, password = password)
    db.session.add(user)
    db.session.commit()
    return user
    
def add_handle(name):
    handle = Handle(name = name, cost = 0)
    db.session.add(handle)
    db.session.commit()
    return handle

if __name__ == "__main__":
    with file('./top100.json') as f:
        handles = json.load(f)
        for handle in handles:
            print add_handle(handle)
            
    with file('users.txt', 'r') as f:
        for line in f:
            print add_user(*line.strip().split(" "))