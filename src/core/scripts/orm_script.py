from django.utils import timezone

from farmers import models as fm
from market import models as mm
from subsidy import models as sm


def run():
    # Fetch all questions

    mm.Market.objects.all().delete()
    mm.Produce.objects.all().delete()
    mm.ContactPerson.objects.all().delete()
    mm.PaymentMethod.objects.all().delete()
    # fm.Farmer.objects.all().delete()
    # fm.AgroVendor.objects.all().delete()
    # fm.FieldExtensionOfficer.objects.all().delete()

    print("Successfully deleted all the records")
