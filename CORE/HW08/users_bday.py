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
