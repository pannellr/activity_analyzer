import time
import datetime
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from .forms import ActivityDataForm
from .analyzer import ActivityBucketSort

# Create your views here.

'''
class NewActivityBucketView(CreateView):
    
    template_name = 'activity_bucket/activity_form.html'
    form_class = ActivityDataForm

    def form_valid(self, form):
        return super(NewActivityBucketView, self).form_valid(form)
'''

    
def get_activity_data(request):
    if request.method == 'POST':
        form = ActivityDataForm(request.POST, request.FILES)

        if form.is_valid():
            filepath = handle_uploaded_file(request.FILES['file_name'])
    
            kwargs = dict()
            kwargs['in_file_path'] = filepath

            # the batch name provided by the user
            # used to name the outfile
            kwargs['batch_name'] = form.cleaned_data['batch_name']

            # get the email so we an send the results to the user
            kwargs['email'] = form.cleaned_data['email']

            # sample frequency
            # helps track sample seuence quality
            kwargs['sample_frequency'] = form.cleaned_data['sample_frequency']

            #thresholds for each category set by the uesr
            kwargs['category_thresholds'] = {
                form.cleaned_data['category1']: {'min': form.cleaned_data['category1_min'], 'max': form.cleaned_data['category1_max']},
                form.cleaned_data['category2']: {'min': form.cleaned_data['category2_min'], 'max': form.cleaned_data['category2_max']},
                form.cleaned_data['category3']: {'min': form.cleaned_data['category3_min'], 'max': form.cleaned_data['category3_max']}
            }

            # check thresholds for gaps or overlaps
            validate_thresholds(kwargs['category_thresholds'])

            abs = ActivityBucketSort(**kwargs)
            print(str(abs.sample_frequency))


            abs.analyze()

            # move into sort method
            #abs.import_activity_data(in_file)

            # return path to outfile
            #sorted = abs.sort(menu.category_thresholds)

             #create a filename based on the date time
             # TODO: ask user
            outfile_name = datetime.datetime.now().strftime("%I:%M%p%B-%d-%Y") + '.csv'            
            return HttpResponseRedirect('/')
    else:
        form = ActivityDataForm()

    return render(request, 'activity_bucket/activity_form.html', {'form': form})



def handle_uploaded_file(f):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d%-H:%M:%S')
    filename = timestamp + '.csv'
    filepath = '/home/pannellr/sandbox/python/uploads/' + filename 
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return filepath


def validate_thresholds(thresholds):
    print(str(thresholds))
    zero = False
    categories = list(thresholds.keys())
    print(str(categories))

    for i, category in enumerate(categories):

        if i < (len(categories) - 1):
            # 0 check
            if i == 0 and thresholds[categories[i]]['min'] == 0:
                zero = True

            # make sure that the min and max values are in the correct order
            if not thresholds[categories[i]]['min'] <= thresholds[categories[i]]['max']:
                return False

            # make sure that there is no overlap
            if thresholds[categories[i]]['max'] > thresholds[categories[i+1]]['min']:                
                return False

            #make sure there is no gap
            if (thresholds[categories[i+1]]['min'] - thresholds[categories[i]]['max']) != 1:
                return False  