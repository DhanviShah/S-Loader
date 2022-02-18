from django import forms

class FileForm(forms.Form):
    #LHS will be visible on the website as text with " " replacing "_". 
    #file = forms.FileField()
    
    #For multiple files
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    drop_dup = forms.BooleanField(required=False)
    # display_file_content = forms.BooleanField(required=False)