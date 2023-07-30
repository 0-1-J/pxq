import request
import config
import time
import threading
from datetime import datetime

'''
目前仅支持【无需选座】的项目
'''
show_id = config.show_id
buy_count = config.buy_count
ticket_price = config.ticket_price
session = config.session
audience_idx = config.audience_idx
deliver_method = config.deliver_method
session_sale_time = config.session_sale_time
session_id = ''
seat_plan_id = ''
price = 0


def print_ticket():
    # 获取票价信息
    # [{
    #   "showSessionId": "64c23f56ae6f7300019b7410",
    #   "seatPlanId": "64c23f60164cd200017a54dd",
    #   "originalPrice": 380,
    #   "seatPlanName": "看台 380元",
    #   "stdSeatPlanId": "64c23f60164cd200017a54dc",
    #   "isCombo": false,
    #   "hasActivity": false,
    #   "seatPlanCategory": "BASE",
    #   "saleTags": [],
    #   "planHot": true,
    #   "items": []
    # }]
    print("seat_plans(now):" + str(request.get_seat_plans(show_id, session_id)))

    # 获取座位余票信息，默认从最低价开始
    # [{
    #   "seatPlanId": "64c23f60164cd200017a54e1",
    #   "hasActivity": false,
    #   "canBuyCount": 0
    # }]
    print("seat_count(now):" + str(request.get_seat_count(show_id, session_id)))


def get_session_item():
    # {
    #   "bizShowSessionId": "64b7c4993f338e0001091f62",
    #   "sessionStatus": "ON_SALE",
    #   "hasSessionSoldOut": false,
    #   "supportSeatPicking": false
    # }
    return request.get_sessions(show_id)[session]


try:
    sessions_item = get_session_item()
    session_id = sessions_item["bizShowSessionId"]
    session_status = sessions_item["sessionStatus"]
    print("session_id:" + session_id, "session_status:" + session_status,
          "session_sale_time:" + str(session_sale_time))
    # 获取票价信息
    # [{
    #   "showSessionId": "64c23f56ae6f7300019b7410",
    #   "seatPlanId": "64c23f60164cd200017a54dd",
    #   "originalPrice": 380,
    #   "seatPlanName": "看台 380元",
    #   "stdSeatPlanId": "64c23f60164cd200017a54dc",
    #   "isCombo": false,
    #   "hasActivity": false,
    #   "seatPlanCategory": "BASE",
    #   "saleTags": [],
    #   "planHot": true,
    #   "items": []
    # }]
    seat_plans = request.get_seat_plans(show_id, session_id)
    print("seat_plans:" + str(seat_plans))

    # 获取座位余票信息，默认从最低价开始
    # [{
    #   "seatPlanId": "64c23f60164cd200017a54e1",
    #   "hasActivity": false,
    #   "canBuyCount": 0
    # }]
    seat_count = request.get_seat_count(show_id, session_id)
    print("seat_count:" + str(seat_count))

    seat_plan_id = seat_plans[ticket_price]["seatPlanId"]
    price = seat_plans[ticket_price]["originalPrice"]
    print("seat_plan_id:" + seat_plan_id, "price:" + str(price))

    # 获取观演人信息
    audiences = request.get_audiences()
    if len(audience_idx) == 0:
        audience_idx = range(buy_count)
    audience_ids = [audiences[i]["id"] for i in audience_idx]
    print("audience_ids:" + str(audience_ids))
    # deliver_method = request.get_deliver_method(show_id, session_id, seat_plan_id, price, buy_count)
    print("deliver_method:" + deliver_method)
    # 获取默认收货地址
    address = request.get_address()
    address_id = address["addressId"]  # 地址id
    location_city_id = address["locationId"]  # 460102
    receiver = address["username"]  # 收件人
    cellphone = address["cellphone"]  # 电话
    detail_address = address["detailAddress"]  # 详细地址
    # 获取快递费用
    express_fee = request.get_express_fee(show_id, session_id, seat_plan_id, price, buy_count,
                                          location_city_id)
    print("address:" + str(address))
    print("express_fee:" + str(express_fee))

    while True:
        # 获取当前时间的时间戳
        current_time = int(time.time() * 1000)
        # TODO 当前时间大于等于开售时间
        # if current_time < session_sale_time:
        #     continue
        print("\n\nON_SALE:" + str(datetime.now()),
              "current_time:" + str(current_time))
        # 打印票信息，启动线程
        threading.Thread(target=print_ticket).start()
        break
    # 下单
    if deliver_method == "EXPRESS":
        request.create_order(show_id, session_id, seat_plan_id, price, buy_count, deliver_method,
                             express_fee["priceItemVal"], receiver,
                             cellphone, address_id, detail_address, location_city_id, audience_ids)
    elif deliver_method == "VENUE_E":
        request.create_order(show_id, session_id, seat_plan_id, price, buy_count, deliver_method, 0, None,
                             None, None, None, None, [])
    elif deliver_method == "VENUE" or deliver_method == "E_TICKET":
        request.create_order(show_id, session_id, seat_plan_id, price, buy_count, deliver_method, 0, None,
                             None, None, None, None, audience_ids)
    else:
        print("不支持的deliver_method:" + deliver_method)
    print("finish time:" + str(datetime.now()))
except Exception as e:
    print(e)
    session_id = ''
