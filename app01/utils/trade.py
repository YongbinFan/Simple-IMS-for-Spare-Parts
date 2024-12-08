"""
Pagination Components
    # 2. request is the django request
    # 3. page pram is the ?page= in the url
    # 4. page_size is the quantity of each page item
    # 5. plus is the current page +- plus, for example current page is 11 then:
         6,7,8,9,10,11,12,13,14,15,16 as the page number

"""
from app01 import models
import math
from urllib.parse import urlencode
import json
import re


class Trade(object):

    def __init__(self, request, trade_way, ):
        self.trade_way = trade_way
        self.request = request
        print("self.trade_way:" + self.trade_way)

    def get_response(self):
        data = json.loads(self.request.body)
        item_list = []
        id_list = []
        for item in data:
            obj_str = item.get("obj")
            try:
                item_id = int(obj_str.split("*")[0])
            except:
                response = {
                    "status": False,
                    "err_msg": "Wrong Item Format, Please double check!"
                }
                return response
            if item_id in id_list:
                response = {
                    "status": False,
                    "err_msg": "Duplicate item in the table, please double check!"
                }
                return response

            obj = models.SpareParts.objects.filter(id=item_id).first()
            # check item id exist
            if not obj:
                response = {
                    "status": False,
                    "err_msg": "Cannot find the item, please double check the ID!!"
                }
                return response

            # check quantity format
            item_quantity = 0
            try:
                item_quantity = int(item.get("quantity"))
            except ValueError:
                response = {
                    "status": False,
                    "err_msg": "Please fill with right quantity format!"
                }
                return response
            # check quantity value
            if item_quantity <= 0:
                response = {
                    "status": False,
                    "err_msg": "Quantity must be greater than 0!"
                }
                return response

            # check different trade way, purchase or sale
            if self.trade_way == "sale":
                print("sale")
                # check inventory

                if item_quantity > obj.quantity:
                    response = {
                        "status": False,
                        "err_msg": obj.__str__() + " Not enough inventory, please double check."
                    }
                    return response
                update_quantity = obj.quantity - item_quantity
                item_quantity = - item_quantity
            elif self.trade_way == "purchase":
                print("purchase")
                update_quantity = obj.quantity + item_quantity
            else:
                raise ValueError("Invalid value! 'trade_way' must be either 'sale' or 'purchase'.")

            item_list.append((item_id, update_quantity, item_quantity))
            id_list.append(item_id)

        for current_id, current_quantity, trade_quantity in item_list:
            models.SpareParts.objects.filter(id=current_id).update(quantity=current_quantity)
            models.Trade.objects.create(spareparts_id_id=current_id, quantity=trade_quantity,
                                        created_by_id=self.request.session["info"]["id"])

        response = {
            "status": True,
        }
        return response
