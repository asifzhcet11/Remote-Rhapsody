import threading
import requests
from urllib.parse import urlencode
from external.device_sync.magenta_synchronizer import MagentaSyncronizer

class NotificationMsg:

    def __init__(self, phone_no: str, body: str):
        self.phone_no = phone_no
        self.body = body

class NotificationService:

    BODY = "You have upcoming event -> {}."

    def __init__(self):
        self.timer: threading.Timer
        self.notification_msg: NotificationMsg
        self.magenta_synchronizer = MagentaSyncronizer()

    def  setup_notification(self, time, msg: NotificationMsg):
        self.notification_msg = msg
        self.timer = threading.Timer(time, self._send_notification)
        self.timer.start()

    def _send_notification(self):
        print("sending to {} : {}".format(self.notification_msg.phone_no, self.notification_msg.body))
        self.magenta_synchronizer.send_msg(to=self.notification_msg.phone_no,
                                           msg=NotificationService.BODY.format(self.notification_msg.body))
        self.timer.cancel()









