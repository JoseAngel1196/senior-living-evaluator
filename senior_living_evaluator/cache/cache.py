from redis import Redis

import json
from uuid import UUID

from senior_living_evaluator.models import SeniorLivingTaskResult
from senior_living_evaluator.settings import REDIS_ENDPOINT, REDIS_PORT
from senior_living_evaluator.logger.logging import Logger

_LOG = Logger(__name__)
_RESULT_PREFIX = "community-"
_RESULT_TTL_SEC = 60 * 60
_REDIS = Redis(host=REDIS_ENDPOINT, port=int(REDIS_PORT))


def load_results(group_id: UUID) -> list[SeniorLivingTaskResult]:
    result_json = _REDIS.get(name=f"{_RESULT_PREFIX}{group_id}")
    if not result_json:
        return []
    parsed_results: list[SeniorLivingTaskResult] = []
    for result in json.loads(result_json):
        try:
            parsed_results.append(SeniorLivingTaskResult.parse_raw(result))
        except Exception as err:
            _LOG.info(
                f"Failed to load results from cache: {err}",
            )
    return parsed_results


def save_results(group_id: UUID, results: list[SeniorLivingTaskResult]) -> None:
    json_results = [result.json() for result in results]
    _REDIS.set(
        name=f"{_RESULT_PREFIX}{group_id}",
        value=json.dumps(json_results),
        ex=_RESULT_TTL_SEC,
    )
