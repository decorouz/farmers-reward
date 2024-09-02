from django.shortcuts import get_object_or_404

from subsidy.models import SubsidyRate


def calculate_discounted_value(subsidy_instance):
    rate = get_object_or_404(
        SubsidyRate,
        subsidy_program=subsidy_instance.subsidy_program,
        subsidized_item=subsidy_instance.item,
    )

    return rate.subsidized_price * subsidy_instance.quantity


# Farmers eligibility
# verification status = True
# has both market purchase and input purchase
# number of points is greater than 1
#
