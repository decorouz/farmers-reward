from django.core.exceptions import ValidationError


def validate_farmer_eligibility(farmer, subsidy_program) -> None:
    """
    Validates the eligibility of a farmer for a subsidy program.

    Args:
        farmer (Farmer): The farmer object to check eligibility for.
        subsidy_program (SubsidyProgram): The subsidy program to check eligibility against.

    Raises:
        ValidationError: If the farmer is not eligible for the program based on state or if the farmer is blacklisted.

    """

    # Check if farmer is eligible for the program based on state
    if (
        subsidy_program.level == "STATE"
        and farmer.state_of_residence != subsidy_program.state
    ):
        raise ValidationError("Farmer is not eligible for this state program")

    # Check if the farmer is blacklisted
    if farmer.blacklisted:
        raise ValidationError("Farmer is blacklisted and not eligible for this program")
