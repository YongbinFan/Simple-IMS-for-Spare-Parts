from app01 import models

from django.db.models import Sum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import copy

bar_chart_data = {
    "title": {
        "text": ' Inventory Distribution'
    },
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": {
            "type": 'shadow'
        }
    },
    "grid": {
        "left": '3%',
        "right": '4%',
        "bottom": '3%',
        "containLabel": True
    },
    "xAxis": [
        {
            "type": 'category',
            "data": [],  # update
            "axisTick": {
                "alignWithLabel": True
            },
            "axisLabel": {
                "rotate": 45
            },
        }
    ],
    "yAxis": [
        {
            "type": 'value'
        }
    ],
    "series": [
        {
            "name": 'Quantity',
            "type": 'bar',
            "barWidth": '60%',
            "data": []  # update
        }

    ]
}


def inventory_distribution():
    highest = 9999999
    histogram_split = [(0, 20), (21, 50), (51, 100), (101, 200), (201, 300), (301, 400), (401, highest)]
    inventory_data = []
    distribution_category = []
    for low, high in histogram_split:
        count = models.SpareParts.objects.filter(quantity__gte=low, quantity__lte=high).count()
        inventory_data.append(count)
        if high == highest:
            distribution_category.append(str(low) + "-More")
        else:
            distribution_category.append(str(low) + "-" + str(high))

    data = copy.deepcopy(bar_chart_data)
    data["title"]["text"] = 'Inventory Distribution'
    data["xAxis"][0]["data"] = distribution_category
    data["series"][0]["data"] = inventory_data

    return data


class SaleData:
    def __init__(self):
        now = datetime.now()
        year_1_range = (now - relativedelta(years=1), now)
        self.inventory_queryset = models.SpareParts.objects.all()

        querysets = models.Trade.objects.filter(trade_time__range=year_1_range, quantity__lte=0)
        self.current_year_sale_sum = querysets.values("spareparts_id_id").annotate(
            total_quantity=Sum("quantity")).order_by("total_quantity")

    def get_sale_data(self, num_show=9999):
        now = datetime.now()
        # make the start date as long as possible
        all_time = (now - relativedelta(years=30), now, "Top " + str(num_show) + " Historical Sales")
        year_1 = (now - relativedelta(years=1), now, "Top " + str(num_show) + " Sales in the Past Year")
        month_3 = (now - relativedelta(months=3), now, "Top " + str(num_show) + " Sales in the Past 3 Months")
        month_1 = (now - relativedelta(months=1), now, "Top " + str(num_show) + " Sales in the Past Month")

        duration_list = [all_time, year_1, month_3, month_1]

        data_list = []
        for i in duration_list:
            start_time, end_time, title = i
            querysets = models.Trade.objects.filter(trade_time__range=(start_time, end_time), quantity__lte=0)
            group_querysets = querysets.values("spareparts_id_id").annotate(total_quantity=Sum("quantity")).order_by(
                "total_quantity")

            id_list = [i["spareparts_id_id"] for i in list(group_querysets)]
            part_list = [models.SpareParts.objects.filter(id=i).first().part_no for i in id_list]
            value_list = [-i["total_quantity"] for i in list(group_querysets)]
            part_value_dict = dict(zip(id_list, value_list))

            data = copy.deepcopy(bar_chart_data)
            data["title"]["text"] = title
            data["xAxis"][0]["data"] = part_list[:num_show]
            data["series"][0]["data"] = value_list[:num_show]

            data_list.append(data)

        return data_list

    def get_sale_vs_inventory(self, num_show=9999):
        # group sum value
        sale_id_list = [i["spareparts_id_id"] for i in list(self.current_year_sale_sum)]
        value_list = [-i["total_quantity"] for i in list(self.current_year_sale_sum)]
        part_value_dict = dict(zip(sale_id_list, value_list))

        # get id, part_no, sum_sales/inventory
        inventory_id_part_quantity_list = [
            (i.id, i.part_no, part_value_dict.get(i.id, 0) / 1) if i.quantity == 0 else (
                i.id, i.part_no, part_value_dict.get(i.id, 0) / i.quantity) for i in self.inventory_queryset]
        sorted_data = sorted(inventory_id_part_quantity_list, key=lambda x: x[2], reverse=True)

        part_list = [i[1] for i in sorted_data]
        value_list = [i[2] for i in sorted_data]
        value_list = [{"value": i, "itemStyle": {"color": '#a90000'}} if i >= 1 else i for i in value_list]

        data = copy.deepcopy(bar_chart_data)
        data["title"]["text"] = "Annual Sales vs. Current Inventory Top " + str(num_show)
        data["xAxis"][0]["data"] = part_list[:num_show]
        data["series"][0]["data"] = value_list[:num_show]
        data["series"][0]["name"] = "Current Year Sale/Inventory"

        return data

    def get_current_inventory(self, num_show=9999, sort="asc"):
        if sort == "asc":
            order_by = "quantity"
            title = "Lowest " + str(num_show) + " Current Inventory"
        else:
            order_by = "-quantity"
            title = "Highest " + str(num_show) + " Current Inventory"
        sort_inventory_queryset = self.inventory_queryset.order_by(order_by)
        part_list = [i.part_no for i in sort_inventory_queryset]
        value_list = [i.quantity for i in sort_inventory_queryset]

        data = copy.deepcopy(bar_chart_data)
        data["title"]["text"] = title
        data["xAxis"][0]["data"] = part_list[:num_show]
        data["series"][0]["data"] = value_list[:num_show]
        return data
