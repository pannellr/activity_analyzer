import sys
import csv
import re
import datetime
import time
from django.core.mail import EmailMessage

# class for an activity record
# three values, a date, time, and intensity
class Activity:

    def __init__(self, record):
        self.time = ''
        self.date = ''
        self.intensity = ''
        
        if not self.validate(record):
            print('Object could not be created for ' + str(record)) 

    def __str__(self):
        return 'Time: ' + datetime.datetime.strftime((datetime.datetime.fromtimestamp(time.mktime(self.time))), '%H:%M:%H' ) + ' Date: ' + str(self.date) + ' Intensity: ' + str(self.intensity)

    def empty(self):
        if self.time == '':
            return True

        if self.date == '':
            return True

        if self.intensity == '':
            return True
            
    def validate(self, record):
        result = True
        integer_re = '^[0-9]+$'
        
        if len(record) != 3:
            print('data malformed 3 fields required')
            return False

        for value in record:
            if value == '':
                return False
        
        # make sure the date is valid
        try:
            self.date = datetime.datetime.strptime(record[0], "%m/%d/%Y").date()
        except ValueError as e:
            print('Date: ' + record[0] + ' could not be coerced into Date object')
            result = False
        # make sure the time is valid
        try:
            self.time = time.strptime(record[1], "%H:%M:%S %p")
        except ValueError as e:
            print('Time: ' + str(record[1]) + ' could not be coerced into Time object')
            result = False

        # make suer the intensity is only an integer
        if re.match(integer_re, record[2]):
            self.intensity = int(record[2])
        else:
            print('intensity not an integer')
            result = False

        return result

    
class ActivityBucketSort:

    def __init__(self, **kwargs):
        self.in_file_path = kwargs['in_file_path']
        self.batch_name = kwargs['batch_name']
        self.email = kwargs['email']
        self.sample_frequency = kwargs['sample_frequency']
        self.category_thresholds = kwargs['category_thresholds']
        self.prepared_data = []
        #self.intensity_threshold = 1100

    def analyze(self):
        self.import_activity_data()
        #print(str(self.prepared_data))
        sorted = self.sort()
        print(str(sorted))
        outfile = self.write_output(sorted)
        self.send_file()
        pass

    def write_output(self, results):
        outfile_path = '/home/pannellr/sandbox/python/uploads/' + str(self.batch_name) + '.csv'
        with open(outfile_path, 'w') as output_fh:
            filewriter = csv.writer(output_fh, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for category in results:
            
                filewriter.writerow([category,])
                row_values = list()
                headers = list()
                for header in results[category]:
                    headers.append(header)
                    row_values.append(results[category][header])

                filewriter.writerow(headers)
                filewriter.writerow(row_values)
                filewriter.writerow(list())
        print(outfile_path)
        return outfile_path

    def send_file(self):
        print('sending email')
        subject = 'Analysis Complete!'
        content = 'Your activity data has been analyzed.  The results are attached to this message' 

        from_email = 'no-reply@silklab.dal.ca'
        to = self.email

        msg = EmailMessage(subject, content, from_email, [to])
        msg.send(fail_silently=False)



    #imports and cleans data
    def prepare(self, filename):
        self.import_activity_data()
        self.clean_data()

    # imports data from given file    
    def import_activity_data(self):
        with open(self.in_file_path, 'r') as activity_file:
            activity_data = csv.reader(activity_file)

            for record in activity_data:
               activity = Activity(record)
               self.prepared_data.append(activity)

    # checks previous and subseuent records to make sure
    # they occur according to the provided sample fruency
    def in_sequence(self, prev, current):
        return True

    # test to see if the given record is above the
    # threshold
    # TODO: remove?  no longer used? 
    def above_threshold(self, record):
        if record.intensity >= self.intensity_threshold:
            return True
        return False

    # checks record threshold to see if it falls within
    # the min and max provided by the user
    def within_threshold(self, record, thresholds):
        if record.intensity >= thresholds['min'] and record.intensity < thresholds['max']:
            return True
        return False

    # sorts the data into buckets whos keys are the number of records
    # that are within the threshold and are in sequence
    def sort(self):
        empty = 0
        buckets = dict()
        prev = ''
        current_bucket = 0

        #create the keys for the user categories
        for category in self.category_thresholds:
            buckets[category] = dict()

        #loop through categories
        for category in self.category_thresholds:
            #loop through records once for each category
            for record in self.prepared_data:
                # count empty records
                if record.empty():
                    empty += 1
                else:

                    # if there is a previous record is set
                    # only fails on first row
                    if prev:
                        #if this record meets the criteria
                        if (self.in_sequence(prev, record) and
                            self.within_threshold(record, self.category_thresholds[category])):
                            # increase the bucket key
                            current_bucket += 1
                            prev = record
                     
                        # break in sequence or threshold
                        else:
                            if current_bucket != 0:
                                # if the bucket esists then increment it
                                if current_bucket in buckets[category]:
                                    buckets[category][current_bucket] += 1
                                # otherwise create it
                                else:
                                    buckets[category][current_bucket] = 1
                            
                            # reset the bucket and prev
                            current_bucket = 0
                            prev = 0
                    # set prev
                    # should only happen on first row
                    else:
                        prev = record
                    
        return buckets

# collects job parameters from user
# class Menu:

#     def __init__(self):
#         self.category_thresholds = dict()

#     def get_processing_parameters(self):
#         num_categories = raw_input("How many categories would you like to define? ")
#         num_categories = int(num_categories)

#         i = 0
#         while i < num_categories:
#             category = raw_input("Category " + str(i+1) + ": ")
#             min = raw_input("Minimum activity threshold for " + category + ": ")
#             max = raw_input("Maximum activity threshold for " + category + ": ")
#             self.category_thresholds[category] = {'min': int(min), 'max': int(max)}
#             i += 1



        
    
