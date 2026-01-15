"""
Small utility script to set Role='admin' for a user in the app's MongoDB.
Edit the MONGO_URI below if you use a different connection string or prefer to
use environment variables.

Usage:
  python3 scripts/set_admin_role.py admin23@gmail.com

This script will set Role='admin' on the user document matching the provided
email. It prints the result and does not change the password.
"""
import sys
from pymongo import MongoClient
from pprint import pprint

# You can override this by editing or using an environment variable if needed.
MONGO_URI = "mongodb+srv://thabang23mthimkulu_db_user:iF7uaE43Q5vxuGbr@cluster0.szsqgnu.mongodb.net/driven_dynamics?retryWrites=true&w=majority"
DB_NAME = "driven_dynamics"


def set_admin(email):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    res = db.user.update_one({'Email': email}, {'$set': {'Role': 'admin'}})
    if res.matched_count == 0:
        print(f"No user found with Email={email}")
    else:
        print(f"Updated user {email} to Role=admin (modified {res.modified_count} document(s)).")
        pprint(db.user.find_one({'Email': email}))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/set_admin_role.py <email>")
        sys.exit(1)
    set_admin(sys.argv[1])
