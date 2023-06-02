from src.service_layer import services
from src.domain.models import Transaction


def test_calculate_statistic():

    transactions = [
        Transaction()
    ]

    statistic = services.calculate_user_statistic()
