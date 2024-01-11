from senior_living_evaluator.models import SeniorLivingCommunity
from senior_living_evaluator.constant import (
    LOCATION_WEIGHT,
    COST_WEIGHT,
    AMENITIES_WEIGHT,
    SAFETY_WEIGHT,
    REVIEWS_RATINGS_WEIGHT,
)


def calculate_community_rating(community: SeniorLivingCommunity) -> float:
    """
    Calculate the overall rating for a SeniorLivingCommunity based on specific weighted parameters.

    Parameters:
    - community (SeniorLivingCommunity): An instance of the SeniorLivingCommunity class containing
      location, cost, amenities, safety, and reviews_ratings attributes.

    Returns:
    - float: The computed overall rating for the community based on the weighted sum of its attributes.
    """
    overall_rating = (
        community.location * LOCATION_WEIGHT
        + community.cost * COST_WEIGHT
        + community.amenities * AMENITIES_WEIGHT
        + community.safety * SAFETY_WEIGHT
        + community.reviews_ratings * REVIEWS_RATINGS_WEIGHT
    )
    return overall_rating
