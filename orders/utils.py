import datetime

def genrate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #20230425242424 + pk
    order_number = current_datetime+str(pk)
    return order_number

