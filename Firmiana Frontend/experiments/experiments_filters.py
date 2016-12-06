import datetime

def experiments_filter(init_list, filters):
    for filter in filters:
        if filter['type'] == 'string':
            if filter['field'] == 'experiment_no':
                init_list = init_list.filter(
                    id__icontains = str(filter['value']))
            elif filter['field'] == 'experiment_name':
                init_list = init_list.filter(
                    name__icontains = str(filter['value']))
            elif filter['field'] == 'instrument':
                init_list = init_list.filter(
                    instrument_name__name__icontains = str(filter['value']))
            elif filter['field'] == 'digest_type':
                init_list = init_list.filter(
                    digest_type__name__icontains = str(filter['value']))
            elif filter['field'] == 'digest_enzyme':
                init_list = init_list.filter(
                    digest_enzyme__name__icontains = str(filter['value']))
#             elif filter['field'] == 'samples':
#                 for experiment in init_list:
#                     experiment_samples = Experiment_sample.objects.filter(experiment=experiment)
# #                 init_list = init_list.filter(
# #                     name__icontains = str(filter['value']))
#             elif filter['field'] == 'reagents':
#                 init_list = init_list.filter(
#                     name__icontains = str(filter['value']))
#             elif filter['field'] == 'separations':
#                 init_list = init_list.filter(
#                     name__icontains = str(filter['value']))
            else:
                kwargs = {str(filter['field']) +
                      '__icontains': str(filter['value'])}
                init_list = init_list.filter(**kwargs)
#         if filter['type'] == 'date':
#             ptime = str(filter['value']).split('/')
#             if filter['comparison'] == 'lt' or filter['comparison'] == 'gt':
#                 today = str(datetime.datetime(
#                     int(ptime[2]), int(ptime[0]), int(ptime[1])))
#                 kwargs = {str(filter['field']) + '__' +
#                           str(filter['comparison']): today}
#             else:
#                 today = datetime.datetime(int(ptime[2]), int(
#                     ptime[0]), int(ptime[1])) - datetime.timedelta(days=1)
#                 tomorrow = today + datetime.timedelta(days=2)
#                 kwargs = {str(filter['field']) + '__gt': str(today)}
#                 init_list = init_list.filter(**kwargs)
#                 kwargs = {str(filter['field']) + '__lt': str(tomorrow)}
#         init_list = init_list.filter(**kwargs)
    return init_list
