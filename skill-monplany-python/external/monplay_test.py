from external.monplany_manager import MonplanyManager
from external.notification.notification_service import NotificationService
manager = MonplanyManager('./credentials/')
manager.user_database.print_collection(manager.user_database.magenta_info_collection)
magenta_id = "jqyfJusKzSPgjt3egObvCHgLs3I6HaUIgF4R89G5lmE="
manager.notification_services[magenta_id] = NotificationService()
manager.update_next_notification(magenta_id=magenta_id)


