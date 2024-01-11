from senior_living_evaluator.celery.client import celery_client
from senior_living_evaluator.models import SeniorLivingTaskArgs, SeniorLivingCommunity
from senior_living_evaluator.logger.logging import Logger
from senior_living_evaluator.rating_calculator import (
    calculate_community_rating,
)

_LOG = Logger(__name__)


@celery_client.task
def evaluate_community(task_args: SeniorLivingTaskArgs) -> float:
    """
    Evaluate the overall rating of a SeniorLivingCommunity based on the provided task arguments.

    Parameters:
    - task_args (SeniorLivingTaskArgs): An instance of SeniorLivingTaskArgs containing the necessary parameters
      to initialize a SeniorLivingCommunity instance.

    Returns:
    - float: The overall rating of the community.
    """
    args = SeniorLivingCommunity(**task_args)
    _LOG.info("Starting evaluate community task", extra={"args": args.dict()})
    overall_rating = calculate_community_rating(community=args)
    _LOG.info(
        "Finished evaluate community task", extra={"overall_rating": overall_rating}
    )
    return overall_rating
