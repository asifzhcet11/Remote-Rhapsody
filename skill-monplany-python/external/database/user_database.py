import pymongo
from external.device_sync.magenta_synchronizer import MagentaSyncronizer
from datetime import datetime

class UserDatabase:
    DATABASE_URL = "mongodb://localhost:27017/"
    DATABASE = "user_db"
    COLLECTION = "users"
    MAGENTA_COLLECTION = "magenta_info"

    def __init__(self):
        self.magenta_synchronizer = MagentaSyncronizer()
        self.db_client = pymongo.MongoClient(UserDatabase.DATABASE_URL)
        self.db = self.db_client[UserDatabase.DATABASE]
        self.user_collection = self.db[UserDatabase.COLLECTION]
        self.magenta_info_collection = self.db[UserDatabase.MAGENTA_COLLECTION]

    def insert_sync_info(self, magenta_id: str) -> str:
        query = {"magenta_id": magenta_id}
        res = self.magenta_info_collection.find_one(query)
        if res:
            # if res["email"]:
            #     return "Your id is already synced with {}".format(res["email"])
            # else:
            #     return "Please sync your id with your email"
            return res["sync_code"]

        else:
            sync_code = self.magenta_synchronizer.generate_sync_code()

            print(sync_code)
            # self.magenta_synchronizer.send_code(code=sync_code, to=to)

            # inserting to db
            self.magenta_info_collection.insert_one({"sync_code": sync_code, "magenta_id": magenta_id})
            return sync_code

    def insert_user_info(self, email: str, first_name: str, last_name: str, events: [], sync_code: int):
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
            }
            self.user_collection.insert_one(data)
            return "Your magenta device is synced"
        else:
            return "Some issue with the sync code. It cannot be synced. Please try again"

    def get_calendar_events_by_magenta_id(self, magenta_id: str):
        query = {"magenta_id": magenta_id}
        res = self.user_collection.find_one(query)
        return res["events"]

    def get_calendar_events_by_email(self, email: str):
        query = {"email": email}
        res = self.user_collection.find_one(query)
        return res["events"]

    def update_calendar_events_by_email(self, email: str, event: dict):
        query = {"email": email}
        # get stored events from database of specific id
        stored_events = self.user_collection.find_one(query)["events"]
        # append to the stored one
        stored_events.append(event)
        # remove duplicate events
        unique_events = [dict(t) for t in {tuple(d.items()) for d in stored_events}]
        new_events = {"$set": {"events": unique_events}}
        self.user_collection.update_one(query, new_events)

    def reset_calendar_events(self, email:str=None, magenta_id:str=None):
        if email:
            query = {"email": email}
        elif magenta_id:
            query = {"magenta_id": magenta_id}
        empty_events = {"$set": {"events": []}}
        self.user_collection.update_one(query, empty_events)

    def update_calendar_events_by_magenta_id(self, magenta_id: str, event: dict):
        query = {"magenta_id": magenta_id}
        # get stored events from database of specific id
        stored_events = self.user_collection.find_one(query)["events"]
        # append to the stored one
        stored_events.append(event)
        # remove duplicate events
        unique_events = [dict(t) for t in {tuple(d.items()) for d in stored_events}]
        new_events = {"$set": {"events": unique_events}}
        self.user_collection.update_one(query, new_events)
        #self.print_collection(self.user_collection)

    def is_user_synced(self, magenta_id: str) -> bool:
        query = {"magenta_id": magenta_id}
        res = self.user_collection.find_one(query)
        if res:
            return True
        else:
            return False

    def get_email_from_id(self, magenta_id: str):
        query = {"magenta_id": magenta_id}
        res = self.user_collection.find_one(query)
        return res["email"]

    def get_id_from_email(self, email: str):
        query = {"email": email}
        res = self.user_collection.find_one(query)
        return res["magenta_id"]

    def print_collection(self, collection):
        for col in collection.find():
            print(col)


    def get_user_first_name(self, magenta_id: str) -> str:
        query = {"magenta_id": magenta_id}
        res = self.user_collection.find_one(query)
        return res["first_name"]


###############
#### TEST #####
###############

# if __name__ == "__main__":
#     print("wghy")
#     user_database = UserDatabase()
#     #magenta_id = "jqyfJusKzSPgjt3egObvCHgLs3I6HaUIgF4R89G5lmE="
#     #user_database.insert_sync_info(magenta_id, to="+4915175834426")
#     user_database.insert_user_info(email="asifzhcet11@gmail.com", first_name="Mohammad", last_name="Asif", events=[], google_auth_code="112", sync_code=82009)
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

