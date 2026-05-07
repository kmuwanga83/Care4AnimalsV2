import logging

logger = logging.getLogger(__name__)


class PushService:
    """
    Push channel contract.
    Replace implementation with FCM in production deployment.
    """

    def send(self, user_id: int, message: str) -> str:
        logger.info("Push placeholder user_id=%s message=%s", user_id, message)
        return "push-not-implemented"


push_service = PushService()
