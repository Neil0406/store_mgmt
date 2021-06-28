from datetime import datetime, timedelta, date
from store_mgmt.models import PurchaseInfo, CompanyProductInfo, SaleInfo
from django.forms.models import model_to_dict
from django.db.models.functions import Concat
import os
from django.db.models import Sum, F, Func, Count
from django.db import models
from dateutil.relativedelta import relativedelta


class HomeModel():
    def get_datetime(self):
        time_ = datetime.now()
        return time_
    def datetime_to_str(self, date_time):
        # time_ = date_time.strftime("%Y/%m/%d, %H:%M:%S")
        time_ = date_time.strftime("%Y-%m-%d")
        return time_
    def str_to_datetime(self, date_time):
        time_ = datetime.strptime(date_time, '%Y-%m-%d')
        return time_

    def realtime_content(self, realtime_content): 
        def func(start_time, end_time):
            ret = {}
            #商品銷售額
            sale_sum = SaleInfo.objects.filter(sale_date__gte = start_time).filter(sale_date__lt = end_time).aggregate(total=Sum(F('sale_price') * F('sale_amount')))['total']
            if sale_sum == None:
                sale_sum = 0
            #商品銷售總數
            sale_amount_sum = SaleInfo.objects.filter(sale_date__gte = start_time).filter(sale_date__lte = end_time).aggregate(total=Sum('sale_amount'))['total']
            if sale_amount_sum == None:
                sale_amount_sum = 0
            #扣除成本營收   
            revenue = SaleInfo.objects.filter(sale_date__gte = start_time).filter(sale_date__lte = end_time)
            revenue_sum = 0
            for i in revenue:
                revenue_sum += (i.sale_price - i.purchase.purchase_price) * i.sale_amount
            #進貨成本
            purchase_sum = PurchaseInfo.objects.filter(purchase_date__gte = start_time).filter(purchase_date__lte = end_time).aggregate(total=Sum(F('purchase_price') * F('amount')))['total']
            if purchase_sum == None:
                purchase_sum = 0
            #進貨總數
            purchase_amount_sum = PurchaseInfo.objects.filter(purchase_date__gte = start_time).filter(purchase_date__lte = end_time).aggregate(total=Sum('amount'))['total']
            if purchase_amount_sum == None:
                purchase_amount_sum = 0
            #庫存商品總數
            purchase_in_stock_sum = PurchaseInfo.objects.filter(amount__gt = 0).aggregate(total=Sum('product_in_stock'))['total']
            if purchase_in_stock_sum == None:
                purchase_in_stock_sum = 0

            time_ = self.datetime_to_str(start_time) + ' ～ ' +self.datetime_to_str(end_time)
            ret['date'] = time_
            ret['sale_sum'] = format(int(sale_sum),',')
            ret['sale_amount_sum'] = format(int(sale_amount_sum),',')
            ret['revenue_sum'] = format(int(revenue_sum),',')
            ret['purchase_sum'] = format(int(purchase_sum),',')
            ret['purchase_amount_sum'] = format(int(purchase_amount_sum),',')
            ret['purchase_in_stock_sum'] = format(int(purchase_in_stock_sum),',')
            return ret

        date_ = date.today()
        # date_ = date_ - timedelta(days=3)   
        if realtime_content == 'realtime_by_date':
            #商品銷售額
            day_start = date_
            day_end = date_ + timedelta(days=1)
            ret = func(day_start, day_end)
            ret['date'] = self.datetime_to_str(day_start)

        if realtime_content == 'realtime_by_week':
            # 本周第一天和最后一天
            week_start = date_ - timedelta(days=date_.weekday() +1)
            week_end = date_ + timedelta(days=5 - date_.weekday())
            ret = func(week_start, week_end)

        if realtime_content == 'realtime_by_month':
            # 本月第一天和最后一天
            month_start = datetime(date_.year, date_.month, 1)
            month_end = datetime(date_.year, date_.month + 1, 1) - timedelta(days=1)
            ret = func(month_start, month_end)

        if realtime_content == 'realtime_by_year':
            # 本年第一天和最后一天
            year_start = datetime(date_.year, 1, 1)
            year_end = datetime(date_.year + 1, 1, 1) - timedelta(days=1)
            ret = func(year_start, year_end)

        return ret

    def revenue_status_content(self, revenue_status_content):
        #Bar
        class Day(Func):
            function = 'EXTRACT'
            template = '%(function)s(Day from %(expressions)s)'
            output_field = models.IntegerField()
        class Month(Func):
            function = 'EXTRACT'
            template = '%(function)s(MONTH from %(expressions)s)'
            output_field = models.IntegerField()

        date_ = date.today()

        ret = {}
        bgc = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"] * 10
        if revenue_status_content == 'revenue_status_week':
            start_time = date_ - timedelta(days= 6)
            end_time = date_
            week_data = SaleInfo.objects.filter(sale_date__gte = start_time).filter(sale_date__lte = end_time).annotate(day=Day('sale_date')).values('day').annotate(total=Sum(F('sale_price') * F('sale_amount')))
            dic = {'Sunday':'週日', 'Monday':'週一', 'Tuesday':'週二', 'Wednesday':'週三', 'Thursday':'週四', 'Friday':'週五', 'Saturday':'週六'}
            day = []
            labels = []
            data = []
            for i in range(7):
                labels.append(dic[(date_ - timedelta(days= i)).strftime('%A')])
                data.append(0)
                day.append((date_ - timedelta(days= i)).day)
            day = list(reversed(day))
            labels = list(reversed(labels))
            for i in week_data:
                if i['day'] in day: 
                    data[day.index(i['day'])] = int(i['total']) 

            # date_ = date.today()
            # week_start = date_ - timedelta(days=date_.weekday() +1)
            # week_end = date_ + timedelta(days=5 - date_.weekday())
            # week_data = SaleInfo.objects.filter(sale_date__gte = week_start).filter(sale_date__lte = week_end).annotate(day=Day('sale_date')).values('day').annotate(total=Sum(F('sale_price') * F('sale_amount')))
            
            # labels = ['日', '一', '二', '三','四', '五', '六']                               #文字
            # week_l = [week_start.day + i for i in range(date_.day - week_start.day + 1)]   #今天 - 本週開始時間 例如本週開始 20號 今天21號因為是兩天所以需加1, 再把開始時間20號 + i(0~x) 得出 [20, 21]  
            # data = [0 for i in range(date_.day - week_start.day + 1)]                      #同上方法先將 data 補 0 本週開至本日天數長度
            # for i in week_data:                                                            #query出來的資料 [{'day':20, 'sum':60000, 'day':21, 'sum':3500}]
            #     if i['day'] in week_l:                                                     #檢查是否在week_l裡 [20, 21]
            #         data[week_l.index(i['day'])] = int(i['total'])                         #如果存在將方補 0 的data list 利用同樣長度 week_l 將 0 改成計算出來的數值 

        if revenue_status_content == 'revenue_status_month':
            start_time = date_ - timedelta(days= 30)
            end_time = date_
            month_data = SaleInfo.objects.filter(sale_date__gte = start_time).filter(sale_date__lte = end_time).annotate(day=Day('sale_date')).values('day').annotate(total=Sum(F('sale_price') * F('sale_amount')))
            labels = []
            data = []
            for i in range(30):
                labels.append((date_ - timedelta(days= i)).day)
                data.append(0)
            labels = list(reversed(labels))
            for i in month_data:
                if i['day'] in labels: 
                    data[labels.index(i['day'])] = int(i['total'])    

            # date_ = date.today()
            # month_start = datetime(date_.year, date_.month, 1)
            # month_end = datetime(date_.year, date_.month + 1, 1) - timedelta(days=1)
            # month_data = SaleInfo.objects.filter(sale_date__gte = month_start).filter(sale_date__lte = month_end).annotate(day=Day('sale_date')).values('day').annotate(total=Sum(F('sale_price') * F('sale_amount')))

            # labels = [i for i in range(1,32)] 
            # month_l = [month_start.day + i for i in range(date_.day - month_start.day + 1)]
            # data = [0 for i in range(date_.day - month_start.day + 1)]                      
            # for i in month_data:                                                        
            #     if i['day'] in month_l:                                                    
            #         data[month_l.index(i['day'])] = int(i['total'])                   

        if revenue_status_content == 'revenue_status_year':
            start_time = date_ - relativedelta(months=12)
            end_time = date_
            year_data = SaleInfo.objects.filter(sale_date__gte = start_time).filter(sale_date__lte = end_time).annotate(month=Month('sale_date')).values('month').annotate(total=Sum(F('sale_price') * F('sale_amount')))
            dic = {1:'一月', 2:'二月', 3:'三月', 4:'四月', 5:'五月', 6:'六月', 7:'七月', 8:'八月', 9:'九月', 10:'十月', 11:'十一月', 12:'十二月'}
            month = []
            labels = []
            data = []

            for i in range(12):
                labels.append(dic[(date_ - relativedelta(months=i)).month])
                data.append(0)
                month.append((date_ - relativedelta(months=i)).month)
            month = list(reversed(month))
            labels = list(reversed(labels))
            for i in year_data:
                if i['month'] in month: 
                    data[month.index(i['month'])] = int(i['total']) 

            # date_ = date.today()
            # year_start = datetime(date_.year, 1, 1)
            # year_end = datetime(date_.year + 1, 1, 1) - timedelta(days=1)
            # year_data = SaleInfo.objects.filter(sale_date__gte = year_start).filter(sale_date__lte = year_end).annotate(month=Month('sale_date')).values('month').annotate(total=Sum(F('sale_price') * F('sale_amount')))

            # labels = ['一月', '二月', '三月','四月', '五月', '六月','七月', '八月', '九月','十月', '十一月', '十二月']
            # year_l = [year_start.month + i for i in range(date_.month - year_start.month + 1)]
            # data = [0 for i in range(date_.month - year_start.month + 1)]                      
            # for i in year_data:                                                        
            #     if i['month'] in year_l:                                                    
            #         data[year_l.index(i['month'])] = int(i['total'])  

        ret['labels'] = labels[:len(data)]
        ret['data'] = data
        ret['bgc'] = bgc[:len(data)]
        return ret

    def hot_sale_content(self, hot_sale_content):
        date_ = date.today()
        bgc = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"] * 3
        ret = {}
        if hot_sale_content == 'hot_sale_week':
            start_time = date_ - timedelta(days= 6)
            end_time = date_

        if hot_sale_content == 'hot_sale_month':
            start_time = date_ - timedelta(days= 30)
            end_time = date_
        
        sale_data = SaleInfo.objects.filter(sale_date__gte = start_time).filter(sale_date__lte = end_time).values('product').annotate(sale_amount=Sum('sale_amount')).order_by('-sale_amount')
        labels = []
        data = []
        for i in sale_data:
            cp = CompanyProductInfo.objects.get(id=i['product'])
            if cp.types not in labels:
                labels.append(cp.types)
                data.append(int(i['sale_amount']))
            else:
                data[labels.index(cp.types)] += int(i['sale_amount'])
        try:
            zipped_lists = zip(data, labels)
            sorted_pairs = sorted(zipped_lists, reverse=True)
            tuples = zip(*sorted_pairs)
            data, labels = [ list(tuple) for tuple in  tuples]
        except:
            data = []
            labels = []
            
        ret['labels'] = labels[:5]
        ret['data'] = data[:5]
        ret['bgc'] = bgc[:len(data)]
        return ret

    def main_revenue_content(self, main_revenue_content):
        date_ = date.today()
        bgc = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"] * 3
        ret = {}
        if main_revenue_content == 'main_revenue_week':
            start_time = date_ - timedelta(days= 6)
            end_time = date_

        if main_revenue_content == 'main_revenue_month':
            start_time = date_ - timedelta(days= 30)
            end_time = date_

        sale_data = SaleInfo.objects.filter(sale_date__gte = start_time).filter(sale_date__lte = end_time)
        sale_amount = sale_data.values('purchase').annotate(sale_amount=Sum('sale_amount'))
        sale_price = sale_data.values('purchase').annotate(sale_price=Sum(F('sale_price') * F('sale_amount')))
        # print(sale_amount, sale_price)
        sale_data = zip(sale_amount, sale_price)
        labels = []
        data = []
        for sale_amount,  sale_price in sale_data:
            s = sale_price['sale_price'] / sale_amount['sale_amount']    #銷售單價 = 總銷售額 / 總銷售數量
            purchase = PurchaseInfo.objects.get(id=sale_amount['purchase'])
            revenue = (s - purchase.purchase_price) * sale_amount['sale_amount']
            # print(purchase.product.types, sale_amount, sale_price['sale_price'], '營收：', int(revenue))    #錄音介面 {'purchase': 2, 'sale_amount': 3.0} 69500.0 營收： 14000
            if purchase.product.types not in labels:
                labels.append(purchase.product.types)
                data.append(int(revenue))
            else:
                data[labels.index(purchase.product.types)] += int(revenue)
        try:
            zipped_lists = zip(data, labels)
            sorted_pairs = sorted(zipped_lists, reverse=True)
            tuples = zip(*sorted_pairs)
            data, labels = [ list(tuple) for tuple in  tuples]
        except:
            data = []
            labels = []
        ret['labels'] = labels[:5]
        ret['data'] = data[:5]
        ret['bgc'] = bgc[:len(data)]
        return ret


