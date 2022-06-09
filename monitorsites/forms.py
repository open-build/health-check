from .models import MonitorSite
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset
from functools import partial
from django import forms


class MonitorSiteForm(forms.ModelForm):

    class Meta:
        model = MonitorSite
        exclude = ['create_date','edit_date']
        widgets = {'comments': forms.Textarea(attrs={'rows':4}),
        }

    def __init__(self, *args, **kwargs):
        #get the user object to check permissions with
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('montiorsite_update', kwargs={'pk': monitorsite.id})
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
                        'name','url','polling_interval','description',
                        ),
                ),
            ),

            HTML("""<br/>"""),
            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Submit('_addanother', 'Save & Add Another >>', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )

        super(MonitorSiteForm, self).__init__(*args, **kwargs)

        #override the country queryset to use request.user for country
        self.fields['owner'] = self.request.user
