from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class BGGUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary'))
    helper.form_method = 'POST'