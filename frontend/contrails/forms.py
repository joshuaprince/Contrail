from django import forms


class PriceForm(forms.Form):
    OPSYS_CHOICES = (
        ('', 'All'),
        ("Linux", "Linux"),
        ("RHEL", "RHEL"),
        ("SLES", "SLES"),
        ("Windows", "Windows"),
        ("Windows with SQL Standard", "Windows with SQL Standard"),
        ("Windows with SQL Web", "Windows with SQL Web"),
        ("Windows with SQL Enterprise", "Windows with SQL Enterprise"),
        ("Linux with SQL Standard", "Linux with SQL Standard"),
        ("Linux with SQL Web", "Linux with SQL Web"),
        ("Linux with SQL Enterprise", "Linux with SQL Enterprise"),
    )

    REGION_CHOICES = (
        ('', 'All'),
        ("US East (N. Virgina)", "US East (N. Virgina)"),
        ("US East (Ohio)", "US East (Ohio)"),
        ("US West (Norther California)", "US West (Norther California)"),
        ("US West (Oregon)", "US West (Oregon)"),
        ("Asia Pacific (Mumbai)", "Asia Pacific (Mumbai)"),
        ("Asia Pacific (Seoul)", "Asia Pacific (Seoul)"),
        ("Asia Pacific (Singapore)", "Asia Pacific (Singapore)"),
        ("Asia Pacific (Sydney)", "Asia Pacific (Sydney)"),
        ("Asia Pacific (Tokyo)", "Asia Pacific (Tokyo)"),
        ("Canada (Central)", "Canada (Central)"),
        ("EU (Frankfurt)", "EU (Frankfurt)"),
        ("EU (Ireland)", "EU (Ireland)"),
        ("EU (London)", "EU (London)"),
        ("EU (Paris)", "EU (Paris)"),
        ("EU (Stockholm)", "EU (Stockholm)"),
        ("South America (Sao Paulo)", "South America (Sao Paulo)"),
        ("AWS GovCloud (US-East)", "AWS GovCloud (US-East)"),
        ("AWS GovCloud (US-West)", "AWS GovCloud (US-West)"),

    )

    operating_system = forms.ChoiceField(choices=OPSYS_CHOICES, required=False)
    aws = forms.BooleanField(required=False, initial=True)
    gcp = forms.BooleanField(required=False, initial=True)
    azure = forms.BooleanField(required=False, initial=True)
    region = forms.ChoiceField(choices=REGION_CHOICES, required=False)
    vcpus = forms.IntegerField(required=False)
    memory = forms.FloatField(required=False)
    ecu = forms.IntegerField(required=False)
