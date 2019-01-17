from django import forms


class CommitForm(forms.Form):
    r_commit = forms.CharField(widget=forms.Textarea, required=False)
    rating = forms.IntegerField(required=False)

    def clean_r_commit(self):
        data = self.cleaned_data['r_commit']
        return data

    def clean_rating(self):
        data = self.cleaned_data['rating']
        return data
