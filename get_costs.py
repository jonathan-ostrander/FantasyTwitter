from app import db, Handle, HandleData

def do_the_cost():
    handlesdata = HandleData.query.all()
    average_retweets = sum([dat.retweets for dat in handlesdata])/float(len(handlesdata))

    handles = Handle.query.all()
    for handle in handles:
        handle.cost =  int((handle.get_latest()/average_retweets) * 20)
        if handle.cost > 50:
            handle.cost = int(50 + handle.cost / 20)
        if handle.cost == 0:
            handle.cost = 1
        db.session.commit()
    return True

if __name__=="__main__":
    do_the_cost()
