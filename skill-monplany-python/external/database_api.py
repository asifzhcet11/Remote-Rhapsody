import pymongo
from external.magenta_synchronization import MagentaSyncronization

class UserDatabase:
    DATABASE_URL = "mongodb://localhost:27017/"
    DATABASE = "user_db"
    COLLECTION = "users"
    MAGENTA_COLLECTION = "magenta_info"

    def __init__(self):
        self.magenta_synchronizer = MagentaSyncronization()
        self.db_client = pymongo.MongoClient(UserDatabase.DATABASE_URL)
        self.db = self.db_client[UserDatabase.DATABASE]
        self.user_collection = self.db[UserDatabase.COLLECTION]
        self.magenta_info_collection = self.db[UserDatabase.MAGENTA_COLLECTION]

    def insert_sync_info(self, magenta_id: str, to: str) -> str:
        query = {"magenta_id": magenta_id}
        res = self.magenta_info_collection.find_one(query)
        if res:
            # if res["email"]:
            #     return "Your id is already synced with {}".format(res["email"])
            # else:
            #     return "Please sync your id with your email"
            return "Sync is in progress. Please wait."

        else:
            sync_code = self.magenta_synchronizer.generate_sync_code()
            self.magenta_synchronizer.send_code(code=sync_code, to=to)

            # inserting to db
            self.magenta_info_collection.insert_one({"sync_code": sync_code, "magenta_id": magenta_id})
            return "Your code {}, is also sent to your number. Please sync on our web application".format(sync_code)

    def insert_user_info(self, email: str, first_name: str, last_name: str, events: [], google_auth_code: str, sync_code: int):
        query = {"sync_code": sync_code}
        res = self.magenta_info_collection.find_one(query)
        print(res)
        if res:
            res["sync_code"] = -1
            data = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "events": events,
                "magenta_info": res,
                "magenta_id": res["magenta_id"],
                "google_auth_code": google_auth_code
            }
            self.user_collection.insert_one(data)
            return "Your magenta device is synced"
        else:
            return "Some issue with the sync code. It cannot be synced. Please try again"

    def get_calendar_events(self, email: str):
        query = {"email": email}
        res = self.user_collection.find_one(query)
        return res["events"]

    def update_calendar_events(self, email: str, events: []):
        query = {"email": email}
        new_events = {"$set": {"events": events}}
        self.user_collection.update_one(query, new_events)

    def is_user_synced(self, magenta_id: str) -> bool:
        query = {"magenta_id": magenta_id}
        res = self.user_collection.find_one(query)
        if res:
            return True
        else:
            return False

    def print_collection(self, collection):
        for col in collection.find():
            print(col)


###############
#### TEST #####
###############

if __name__ == "__main__":
    print("wghy")
    user_database = UserDatabase()
    magenta_id = "jqyfJusKzSPgjt3egObvCHgLs3I6HaUIgF4R89G5lmE="
    user_database.insert_sync_info(magenta_id, to="+4915175834426")
    # user_database.print_collection(user_database.magenta_info_collection)
    #
    #
    # print(user_database.insert_user_info(email="abc@email",
    #                                      first_name="abc",
    #                                      last_name="xyz",
    #                                      events=[{'date': 1}],
    #                                      google_auth_code="asdf",
    #                                      sync_code=20736))
    # user_database.print_collection(user_database.user_collection)

#     if not (user_database.is_user_synced(magenta_id)):
#         print("------Sync code sent-----")
#         print(user_database.insert_sync_info(magenta_id, to="+4915175834426"))
#         user_database.print_collection(user_database.magenta_info_collection)
#     print("------User info added and magenta synced-----")
#     print(user_database.insert_user_info(email="abc@email",
#                                          first_name="abc",
#                                          last_name="xyz",
#                                          events=[{'date': 1}],
#                                          sync_code=12345))
#     user_database.print_collection(user_database.user_collection)
#     print("------Check if it really synced-----")
#     print(user_database.is_user_synced(magenta_id))
#     print("------Getting calendar events-----")
#     print(user_database.get_calendar_events(email="abc@email"))
#     user_database.print_collection(user_database.user_collection)
#     print("------Update calendar events-----")
#     print(user_database.update_calendar_events(email="abc@email", events=[{'date': 1},
#                                                                           {'date': 2}]))

