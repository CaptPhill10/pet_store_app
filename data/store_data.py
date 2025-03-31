from datetime import datetime

orders = [
    {
        "id": 1,
        "pet_id": 1,
        "quantity": 2,
        "shipDate": "2024-12-23T10:00:00Z",
        "status": "placed",
        "complete": True,
    },
    {
        "id": 2,
        "pet_id": 2,
        "quantity": 1,
        "shipDate": "2024-12-25T12:00:00Z",
        "status": "approved",
        "complete": False,
    },
]

order_id_counter = len(orders) + 1
