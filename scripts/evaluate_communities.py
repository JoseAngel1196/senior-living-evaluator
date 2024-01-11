import argparse
import uuid
from uuid import UUID
import random
import string
from celery.result import AsyncResult

from senior_living_evaluator.models import SeniorLivingTaskArgs, SeniorLivingTaskResult
from senior_living_evaluator.celery.tasks import evaluate_community
from senior_living_evaluator.cache.cache import save_results


def _generate_senior_living_communities(
    num_communities: int,
) -> list[SeniorLivingTaskArgs]:
    """
    Generate a list of SeniorLivingTaskArgs with random attributes.
    """
    communities: list[SeniorLivingTaskArgs] = []
    for _ in range(num_communities):
        name = "".join(
            random.choices(string.ascii_uppercase, k=8)
        )  # Generate a random name
        location = random.randint(
            70, 100
        )  # Generate a random location score (between 70 and 100)
        cost = random.randint(
            60, 95
        )  # Generate a random cost score (between 60 and 95)
        amenities = random.randint(
            70, 100
        )  # Generate a random amenities score (between 70 and 100)
        safety = random.randint(
            80, 100
        )  # Generate a random safety score (between 80 and 100)
        reviews_ratings = round(
            random.uniform(3.5, 5.0), 1
        )  # Generate a random reviews/ratings score (between 3.5 and 5.0)

        community = SeniorLivingTaskArgs(
            name=name,
            location=location,
            cost=cost,
            amenities=amenities,
            safety=safety,
            reviews_ratings=reviews_ratings,
        )
        communities.append(community)

    return communities


def _run_celery_tasks(group_id: UUID, communities: list[SeniorLivingTaskArgs]) -> None:
    """
    Execute Celery tasks to evaluate the overall rating for each senior living community in the provided list.

    Parameters:
    - group_id (uuid.UUID): A unique identifier for grouping the result of the communities.
    - communities (list): A list containing dictionaries representing SeniorLivingTaskArgs with attributes
      such as 'name', 'location', 'cost', 'amenities', 'safety', and 'reviews_ratings' for each community.

    Returns:
    - None.
    """
    celery_results: list[SeniorLivingTaskResult] = []
    for community in communities:
        async_result: AsyncResult = evaluate_community.apply_async(args=[community])
        celery_results.append(
            SeniorLivingTaskResult(
                task_result_id=async_result.id,
                name=community.name,
                location=community.location,
                cost=community.cost,
                amenities=community.amenities,
                safety=community.safety,
                reviews_ratings=community.reviews_ratings,
            )
        )
    print(f"Save pending results for {group_id}...")
    save_results(group_id, celery_results)
    print(f"Saved results for {group_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Setup script to evaluate senior living communities"
    )
    parser.add_argument(
        "-n",
        "--num_communities",
        default="num_communities",
        help="Number of communities to generate.",
    )
    args = parser.parse_args()

    print(f"Number of senior living communities to generate: {args.num_communities}")

    print("Generating senior living communities...")
    group_id = uuid.uuid4()
    communities = _generate_senior_living_communities(group_id, args.num_communities)

    print("Running set of tasks to evaluate overall rating...")
    _run_celery_tasks(communities)
    print("Communities are being evaluated...")

    print(f"Please use this ID {group_id} to load the results")
