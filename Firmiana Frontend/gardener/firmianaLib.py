#standarlib by Garfiled
import datetime


def result_filter(init_list, filters):
    for filter in filters:
        if filter['type'] == 'string':
            kwargs = {str(filter['field']) +
                      '__icontains': str(filter['value'])}
        if filter['type'] == 'numeric':
            if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                kwargs = {str(filter['field']) + '__' +
                          str(filter['comparison']): str(filter['value'])}
            else:
                kwargs = {str(filter['field']) +
                          '__exact': str(filter['value'])}
        if filter['type'] == 'date':
            ptime = str(filter['value']).split('/')
            if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
                today = str(datetime.datetime(
                    int(ptime[2]), int(ptime[0]), int(ptime[1])))
                kwargs = {str(filter['field']) + '__' +
                          str(filter['comparison']): today}
            else:
                today = datetime.datetime(int(ptime[2]), int(
                    ptime[0]), int(ptime[1])) - datetime.timedelta(days=1)
                tomorrow = today + datetime.timedelta(days=2)
                kwargs = {str(filter['field']) + '__gt': str(today)}
                init_list = init_list.filter(**kwargs)
                kwargs = {str(filter['field']) + '__lt': str(tomorrow)}
        init_list = init_list.filter(**kwargs)
    return init_list
