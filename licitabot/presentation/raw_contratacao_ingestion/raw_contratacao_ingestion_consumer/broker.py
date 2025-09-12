from faststream.rabbit import RabbitBroker
from licitabot.settings import settings, logger


def get_broker():
    return RabbitBroker(settings.rabbitmq.amqp_url, logger=logger)
