from util.logging_config import logger
from fastapi import APIRouter, HTTPException
from data.store_data import orders, order_id_counter
from data.pets_data import pets

router = APIRouter()
# logger = structlog.get_logger(__name__)


@router.post("/store/order", status_code=201)
def place_order(order: dict):
    global order_id_counter
    logger.info("Placing new order", order=order)
    order["id"] = order_id_counter
    order_id_counter += 1
    orders.append(order)
    logger.info("Order placed successfully", order_id=order["id"])
    return order


@router.get("/store/order/{order_id}")
def get_order(order_id: int):
    logger.info("Getting order by ID", order_id=order_id)
    for order in orders:
        if order["id"] == order_id:
            logger.info("Order found", order_id=order_id)
            return order
    logger.warning("Order not found", order_id=order_id)
    raise HTTPException(status_code=404, detail="Order not found")


@router.delete("/store/order/{order_id}")
def delete_order(order_id: int):
    logger.info("Deleting order", order_id=order_id)
    for order in orders:
        if order["id"] == order_id:
            orders.remove(order)
            logger.info("Order deleted successfully", order_id=order_id)
            return {"message": f"Order with ID {order_id} has been deleted"}
    logger.warning("Order not found", order_id=order_id)
    raise HTTPException(status_code=404, detail="Order not found")


@router.get("/store/inventory")
def get_inventory():
    logger.info("Calculating inventory")
    inventory = {}
    for pet in pets:
        status = pet["status"]
        inventory[status] = inventory.get(status, 0) + 1
    logger.info("Inventory calculated", inventory=inventory)
    return inventory

# from fastapi import APIRouter, HTTPException
# from data.store_data import orders, order_id_counter
# from data.pets_data import pets
# import logging
#
# logger = logging.getLogger(__name__)
#
# router = APIRouter()
#
#
# @router.post("/store/order", status_code=201)
# def place_order(order: dict):
#     global order_id_counter
#     logger.info(f"Placing new order: {order}")
#     order["id"] = order_id_counter
#     order_id_counter += 1
#     orders.append(order)
#     logger.info(f"Order with ID {order['id']} placed successfully")
#     return order
#
#
# @router.get("/store/order/{order_id}")
# def get_order(order_id: int):
#     logger.info(f"Getting order by ID: {order_id}")
#     for order in orders:
#         if order["id"] == order_id:
#             logger.info(f"Order with ID {order_id} found")
#             return order
#     logger.warning(f"Order with ID {order_id} not found")
#     raise HTTPException(status_code=404, detail="Order not found")
#
#
# @router.delete("/store/order/{order_id}")
# def delete_order(order_id: int):
#     logger.info(f"Deleting order with ID: {order_id}")
#     for order in orders:
#         if order["id"] == order_id:
#             orders.remove(order)
#             logger.info(f"Order with ID {order_id} deleted successfully")
#             return {"message": f"Order with ID {order_id} has been deleted"}
#     logger.warning(f"Order with ID {order_id} not found")
#     raise HTTPException(status_code=404, detail="Order not found")
#
#
# @router.get("/store/inventory")
# def get_inventory():
#     logger.info("Calculating inventory")
#     inventory = {}
#     for pet in pets:
#         status = pet["status"]
#         inventory[status] = inventory.get(status, 0) + 1
#     logger.info(f"Inventory calculated: {inventory}")
#     return inventory

