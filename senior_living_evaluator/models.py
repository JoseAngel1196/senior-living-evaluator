from typing import TypedDict

from pydantic import BaseModel


class SeniorLivingTaskArgs(TypedDict):
    name: str
    location: int
    cost: int
    amenities: int
    safety: int
    reviews_ratings: int


class SeniorLivingCommunity(BaseModel):
    name: str
    location: str
    cost: str
    amenities: str
    safety: str
    reviews_ratings: str


class SeniorLivingTaskResult(SeniorLivingCommunity):
    task_result_id: str
    overall_rating: int | None = None
