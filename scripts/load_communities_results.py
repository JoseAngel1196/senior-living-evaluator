import argparse
from uuid import UUID


from senior_living_evaluator.models import SeniorLivingTaskResult
from senior_living_evaluator.cache.cache import load_results
from senior_living_evaluator.celery.client import celery_client


def _poll_celery_results(group_id: UUID) -> list[SeniorLivingTaskResult]:
    print(f"Loading results from cache for {group_id}")
    results: list[SeniorLivingTaskResult] = load_results(group_id)
    print(f"Loaded results for {len(results)}")
    for result in results:
        async_result = celery_client.AsyncResult(id=result.task_result_id)
        if async_result.ready():
            # https://docs.celeryq.dev/en/stable/reference/celery.result.html#:~:text=property%20queue-,ready(),-%5Bsource%5D
            task_result: float = async_result.get()
            result.overall_rating = task_result
    return results


def _print_community_scores(results: list[SeniorLivingTaskResult]) -> None:
    """
    Print the community scores for each community in the provided results list.
    """
    for idx, result in enumerate(results, start=1):
        print(f"\nCommunity {idx} - Task Result ID: {result.task_result_id}")
        print(f"Community Score: {result.overall_rating}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Setup script to load the rating results of the senior living communities."
    )
    parser.add_argument(
        "-gi",
        "--group_id",
        default="group_id",
        help="The ID to gather the rating results of the senior living communities.",
    )
    args = parser.parse_args()

    print(f"Poll senior living communities scores for {args.group_id}....")
    results = _poll_celery_results(args.group_id)

    print("Printing communities scores")
    _print_community_scores(results)
