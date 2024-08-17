'''
endpoint_tracker, created = EndpointTracker.objects.get_or_create(
        name=enpoint_name, category=category, endpoint=endpoint
    ) 
    # if endpoint request exists
    if not created:
        # and if last request time > 1 day, clear all countries data
        if timezone.now() - endpoint_tracker.last_requested > timedelta(days=1):
            Season.objects.all().delete()
            print('deleting old data')
        else:
            # if last requested time <1 day no need to fetch data
            return HttpResponse('Data upto date')
''' 