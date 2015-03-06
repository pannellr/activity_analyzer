from django import forms

class ActivityDataForm(forms.Form):

    CHOICES =(
        ('5', '5 seconds'),
        ('10', '10 seconds'),
        ('15', '15 seconds'),
        ('30', '30 seconds'),
        ('60', '60 seconds'),
    )
    
    batch_name = forms.CharField(label='Batch name', max_length=100, required=False)
    email = forms.EmailField(label='Your email', required=False)
    sample_frequency = forms.ChoiceField(label='Choose sample frequency',
                                         choices=CHOICES,
                                         required=False
                                         )
    category1 = forms.CharField(label='Category 1', max_length=100, required=False)
    category1_min = forms.IntegerField(label='Minimum Threshold', required=False)
    category1_max = forms.IntegerField(label='Maximum Threshold', required=False)
    category2 = forms.CharField(label='Category 2', max_length=100, required=False)
    category2_min = forms.IntegerField(label='Minimum Threshold', required=False)
    category2_max = forms.IntegerField(label='Maximum Threshold', required=False)
    category3 = forms.CharField(label='Category 3', max_length=100, required=False)
    category3_min = forms.IntegerField(label='Minimum Threshold', required=False)
    category3_max = forms.IntegerField(label='Maximum Threshold', required=False)
    file_name = forms.FileField(label='Upload file(s)', required=False)
