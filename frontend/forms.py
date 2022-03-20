from crispy_forms import layout
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings

from .utils import get_grouped_sets


class LabelGeneratorForm(forms.Form):

    sets = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
    )

    paper_size = forms.ChoiceField(
        choices=(
            ("letter", "Letter Paper (8.5in * 11in)"),
            ("a4", "A4 Paper (210mm * 297mm)"),
        ),
        help_text="Letter paper is common in North America. A4 paper is used everywhere else.",
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        sets = get_grouped_sets()

        default_sets = []
        for set_type, set_list in sets:
            if set_type in (
                "core",
                "expansion",
                "masters",
                "commander",
                "draft innovation",
            ):
                default_sets.extend([code for code, exp in set_list])

        # Setup the default initial data
        if "initial" not in kwargs:
            kwargs["initial"] = {}
        kwargs["initial"].update(
            {
                "paper_size": "letter",
                "sets": ["mh1", "mh2", "lea"],
            }
        )

        super().__init__(*args, **kwargs)

        self.fields["sets"].choices = sets

        self.helper = FormHelper()

        # Currently, this is a stripped down Django setup
        # There's no sessions or CSRF so remove that for now
        self.helper.disable_csrf = (
            "django.middleware.csrf.CsrfViewMiddleware" not in settings.MIDDLEWARE
        )

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "",
                layout.Field("sets", template="frontend/includes/sets-field.html"),
                "paper_size",
                css_class="my-3",
            ),
            layout.HTML("<hr class='mb-4'>"),
            layout.Submit(
                "submit",
                "Generate SVGs and PDFs as a downloadable .zip",
                css_class="btn btn-primary btn-lg btn-block",
            ),
        )
