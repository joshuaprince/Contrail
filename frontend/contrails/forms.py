from django import forms


class PriceForm(forms.Form):
    # OPSYS_CHOICES = (
    #     ('', 'All'),
    #     ("Linux", "Linux"),
    #     ("RHEL", "RHEL"),
    #     ("SLES", "SLES"),
    #     ("Windows", "Windows"),
    #     ("Windows with SQL Standard", "Windows with SQL Standard"),
    #     ("Windows with SQL Web", "Windows with SQL Web"),
    #     ("Windows with SQL Enterprise", "Windows with SQL Enterprise"),
    #     ("Linux with SQL Standard", "Linux with SQL Standard"),
    #     ("Linux with SQL Web", "Linux with SQL Web"),
    #     ("Linux with SQL Enterprise", "Linux with SQL Enterprise"),
    # )

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

    amazon_web_services = forms.BooleanField(required=False, initial=True)
    google_cloud_platform = forms.BooleanField(required=False, disabled=True)#, initial=True)
    microsoft_azure = forms.BooleanField(required=False, disabled=True)#, initial=True)
    region = forms.ChoiceField(choices=REGION_CHOICES, required=False)
    memory_from = forms.CharField(required=False)
    memory_to = forms.CharField(required=False)

    vcpu_from = forms.CharField(required=False)
    vcpu_to = forms.CharField(required=False)

    price_from = forms.CharField(required=False)
    price_to = forms.CharField(required=False)

    pricehr_from = forms.CharField(required=False)
    pricehr_to = forms.CharField(required=False)
