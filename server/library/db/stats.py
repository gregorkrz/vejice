import json

from server.library.db.db import db_get

class UserNotExistsException(Exception):
    pass

QUEUE_MAX_LENGTH = 35

def getUserProfile(userID: str):
    db = db_get()
    query = """SELECT user_profile FROM vejice.users WHERE id = %s """
    result = db.exec_stmt(query, (userID,))
    if len(result): return json.loads(result[0][0])
    raise UserNotExistsException("Unknown user: {}".format(userID))

def getUserStatistics(userID: str):
    try:
        profile = getUserProfile(userID)
        total = profile.get("stats.total")
        correct = profile.get("stats.correct")
    except UserNotExistsException:
        total, correct = 0, 0
    return total, correct

def updateUserProfile(userID: str, new_profile: object):
    print("updating user profile", userID)
    db = db_get()
    stmt = """insert into vejice.users (id, user_profile) 
    values (%s, %s)
    on conflict on constraint users_pkey do
    update set user_profile=%s """
    profile = json.dumps(new_profile)
    db.exec_stmt(stmt, (userID, profile, profile), commit=True, fetch=False)

def updateUserStatistics(userID: str, correct: int, sentence_id: str):
    if correct not in [0, 1]:
        raise Exception("invalid input")
    try:
        profile = getUserProfile(userID)
    except UserNotExistsException:
        profile = {
            "stats.total": 0,
            "stats.correct": 0,
            "positive_queue": [],
            "negative_queue": []
        }
    print("Profile", profile)
    profile["stats.total"] += 1
    profile["stats.correct"] += correct
    tag = "negative_queue"
    if correct:
        tag = "positive_queue"
    profile[tag].append(sentence_id)
    if len(profile[tag]) > QUEUE_MAX_LENGTH:
        profile[tag].pop(0)
    updateUserProfile(userID, profile)

def reportSentence(s):
    db = db_get()
    sentence_id = s[0].split('\t')[0]
    query = "insert into vejice.reports (sentence_id) values(%s); "
    db.exec_stmt(query, (sentence_id,), commit=True, fetch=False)
