from .models import MonitorSite
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset
from functools import partial
from django import forms
from django.urls import reverse

# Monitor Forms
class MonitorSiteForm(forms.ModelForm):

    class Meta:
        model = MonitorSite
        exclude = ['create_date','edit_date']
        widgets = {'comments': forms.Textarea(attrs={'rows':4}),
        }

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # get rid of extra keywords before calling super
        self.helper.form_action = reverse(kwargs.pop('action_name'))
        self.request = kwargs.pop('request')
        # call super to get form fields
        super(MonitorSiteForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'monitorsite_update_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Site to Monitor',
                     Fieldset('',
                        'name','url','polling_interval','description','status'
                        ),
                ),
            ),

            HTML("""<br/>"""),
            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )
        self.fields['owner'].initial = self.request.user
        super(MonitorSiteForm, self).__init__(*args, **kwargs)
