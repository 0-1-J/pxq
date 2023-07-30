# 输入自己的token
token = 'eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9.eNqEkE-LwjAQxb_LnHtI0pimPSqKC7sIooc9SZpMsdAmkqaLf_C7m5JV9rQe5_F-b2beDZwaw_HDNg4qO3ZdBuOAPs03qNvrwhmEClbrz8MXZDCM9fwlCiYKJQmiYVTOOCukaCgvefRFcuu6yTTffy-3UemD3k_RZgK55oYqXedCEU4IoTijkpkEvrM1cM8Az6fW467t8Xl4JDcn9Cq4f2mMS7RHFX5hKkoiSpEzSXIaH7wMAfv0YMrt0eujsuFvSXF7IgvJCiYz-EE_tM5CxVKDVj0Puz8AAAD__w.hXh-kLWatgZNXHVjcxywWAbFjEXACMKYAu8ahXREgHoqZASInn7tT2smQbnwHgpt0TZe07n5Bur0SuAEJBYIVXk2juFmmet5_EZSW6OoI0bQSdfH3wGI9TbyIg3L4CWY0TXnTiqHxWsPAa6B6fdwVJLSf_LbF8y3gDwVCcP1amA'
# 项目id，必填
show_id = '64927ece3ab4520001fbb61a'
# show_id = '64b7c464bcf52a0001bb1daa'
session_sale_time = 1690950000000
# 场次 上到下 0 1 2
session = 0
# 购票数量，一定要看购票须知，不要超过上限
buy_count = 2
# 票价低到高 0 1 2
ticket_price = 2
# 指定观演人，观演人序号从0开始，人数需与票数保持一致
audience_idx = [0, 1]
# 快递送票:EXPRESS,电子票:E_TICKET,现场取票:VENUE,电子票或现场取票:VENUE_E,目前只发现这四种，如有新发现可补充
deliver_method = 'EXPRESS'
