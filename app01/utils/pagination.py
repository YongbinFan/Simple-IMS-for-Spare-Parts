"""
Pagination Components
    # 1. data_dict is the dict of the GET value
    # 2. request is the django request
    # 3. page pram is the ?page= in the url
    # 4. page_size is the quantity of each page item
    # 5. plus is the current page +- plus, for example current page is 11 then:
         6,7,8,9,10,11,12,13,14,15,16 as the page number

"""
from app01 import models
import math
from urllib.parse import urlencode


class Pagination(object):

    def __init__(self, request, data_dict, page_param="page", page_size=20, plus=5, ):
        try:
            page = int(request.GET.get(page_param, 1))
        except:
            page = 1
        if page <= 0:
            page = 1
        self.page = page
        self.page_size = page_size
        self.plus = plus

        self.start = (page - 1) * page_size
        self.end = page * page_size

        total_count = models.SpareParts.objects.filter(**data_dict).count()
        total_page = math.ceil(total_count / page_size)
        if total_page == 0: total_page = 1

        if page >= total_page:
            page = total_page

        if total_page <= 2 * plus + 1:
            # not too much page
            start_page = 1
            end_page = total_page
        else:
            # current page <= plus
            if page <= plus:
                start_page = 1
                end_page = 2 * plus + 1
            else:
                if (page + plus) > total_page:
                    end_page = total_page
                    start_page = total_page - 2 * plus
                else:
                    start_page = page - plus
                    end_page = page + plus

        self.total_page = total_page
        self.queryset = models.SpareParts.objects.filter(**data_dict)[self.start: self.end]

        page_str_list = []
        first = '<li class=><a href="?' + urlencode(data_dict) + '&page={}">First Page</a></li>'.format(1)
        prev = '<li class=><a href="?' + urlencode(data_dict) + '&page={}"><<</a></li>'.format(page - 1)
        next_page = '<li class=><a href="?' + urlencode(data_dict) + '&page={}">>></a></li>'.format(page + 1)
        last = '<li class=><a href="?' + urlencode(data_dict) + '&page={}">Last Page</a></li>'.format(total_page)
        page_str_list.append(first)
        page_str_list.append(prev)
        for i in range(start_page, end_page + 1):
            if i == page:
                ele = '<li class="active"><a href="?' + urlencode(data_dict) + '&page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a href="?' + urlencode(data_dict) + '&page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)
        page_str_list.append(next_page)
        page_str_list.append(last)

        self.page_str = "".join(page_str_list)
