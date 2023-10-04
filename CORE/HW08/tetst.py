import datetime


# def get_birthdays_per_week(users):
#     current_date = datetime.date.today()
#     start_of_week = current_date - datetime.timedelta(days=current_date.weekday())
#     end_of_week = start_of_week + datetime.timedelta(days=6)
#     work_week = start_of_week + datetime.timedelta(days=4)

#     bday_list_this_week = []
#     bday_list_next_week = []

#     for user in users:
#         user_bday = user['birthday'].date()
#         if start_of_week <= user_bday <= work_week:
#             bday_list_this_week.append(user)
#         elif work_week <= user_bday <= end_of_week:
#             bday_list_next_week.append(user)

#     print('Users with birthday this week:')
#     for user in bday_list_this_week:
#         print(f"{user['birthday'].strftime('%m/%d/%Y')} - {user['name']}")

#     if bday_list_next_week:
#         print('Users with birthday next week:')
#         for user in bday_list_next_week:
#             print(f"{user['birthday'].strftime('%m/%d/%Y')} - {user['name']}")
#     else:
#         print('No users have birthdays next week.')


# def get_birthdays_per_week(users):
#     current_date = datetime.date.today()
#     start_of_week = current_date - datetime.timedelta(days=current_date.weekday())
#     end_of_week = start_of_week + datetime.timedelta(days=6)
#     work_week = start_of_week + datetime.timedelta(days=4)
#     wekend = end_of_week - work_week

#     bday_list_this_week = []
#     bday_list_next_week = []

#     for user in users:
#         user_bday = user['birthday'].date()
#         if start_of_week <= user_bday <= work_week:
#             bday_list_this_week.append(user)
#         if work_week <= user_bday <= end_of_week:
#             bday_list_next_week.append(user)
#         if user_bday >= end_of_week:
#             bday_list_next_week.append(user)  
#     print('User with Birthday in this week: ')
#     for user in bday_list_this_week:
#         print(user['birthday'].strftime('%D.%M.%Y'), '-', user['name'])

#     for user in bday_list_next_week:
#         print('User with Birthday in next week: ')
#         print(user['birthday'].strftime('%D.%M.%Y'), '-', user['name'])

import datetime

def get_birthdays_per_week(users):
    current_date = datetime.date.today()
    start_of_week = current_date - datetime.timedelta(days=current_date.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    work_week = start_of_week + datetime.timedelta(days=4)

    bday_list_this_week = []
    bday_list_next_week = []

    for user in users:
        user_bday = user['birthday'].date()
        if start_of_week <= user_bday <= work_week:
            bday_list_this_week.append(user)
        if work_week <= user_bday <= end_of_week:
            bday_list_next_week.append(user)
        if user_bday >= end_of_week:
            bday_list_next_week.append(user)  

    print('Users with Birthday in this week:')
    for user in bday_list_this_week:
        print(user['birthday'].strftime('%m/%d/%Y'), '-', user['name'])

    print('Users with Birthday in next week:')
    for user in bday_list_next_week:
        print(user['birthday'].strftime('%m/%d/%Y'), '-', user['name'])


# users = [
#         {'name': 'Wilkie Collins', 'birthday': '08/01/1824'}, 
#         {'name': 'James Joyce', 'birthday': '13/01/1941'}, 
#         {'name': 'Lewis Carroll', 'birthday': '14/01/1898'}, 
#         {'name': 'J. R. R. Tolkien', 'birthday': '03/01/1892'}, 
#         {'name': 'Rudyard Kipling', 'birthday': '18/01/1936'}, 
#         {'name': 'Edgar Allan Poe', 'birthday': '19/01/1809'}
# ]
 
users = [
        {'name': 'Wilkie Collins', 'birthday': datetime.datetime(1824, 8, 1)}, 
        {'name': 'James Joyce', 'birthday': datetime.datetime(1941, 1, 13)}, 
        {'name': 'Lewis Carroll', 'birthday': datetime.datetime(1898, 1, 14)}, 
        {'name': 'J. R. R. Tolkien', 'birthday': datetime.datetime(1892, 3, 3)}, 
        {'name': 'Rudyard Kipling', 'birthday': datetime.datetime(1936, 1, 18)}, 
        {'name': 'Edgar Allan Poe', 'birthday': datetime.datetime(1809, 1, 10)}
]

a = get_birthdays_per_week(users)
print(a)