from .config import settings
from typing import Any, Optional

from datetime import datetime

from nocodb.nocodb import APIToken, NocoDBProject, WhereFilter
from nocodb.infra.requests_client import NocoDBRequestsClient
from pydantic import BaseModel, Field, RootModel


def get_nocodb_client() -> NocoDBRequestsClient:
    return NocoDBRequestsClient(
        APIToken(settings.nocodb_api_key),
        settings.nocodb_url,
    )


def get_nocodb_project() -> NocoDBProject:
    return NocoDBProject(
        settings.nocodb_org_name,
        settings.project_name,
    )

def get_nocodb_data(table_name: str, filter_obj: Optional[WhereFilter] = None) -> Any:
    client = get_nocodb_client()
    return client.table_row_list(
        get_nocodb_project(),
        table_name,
        filter_obj=filter_obj,
    )


class NocoPerson(BaseModel):
    noco_id: int = Field(alias="Id")
    created_at: datetime = Field(alias="CreatedAt")
    updated_at: datetime = Field(alias="UpdatedAt")
    name: str = Field(alias="Name")
    age: int = Field(alias="Age")


class NocoPersons(RootModel[list[NocoPerson]]):
    TABLE_NAME = "Person"
    root: list[NocoPerson]

    @classmethod
    def from_nocodb(cls):
        raw = get_nocodb_data(cls.TABLE_NAME)
        return cls.model_validate(raw["list"])


class NocoCourse(BaseModel):
    noco_id: int = Field(alias="Id")
    created_at: datetime = Field(alias="CreatedAt")
    updated_at: datetime = Field(alias="UpdatedAt")
    name: str = Field(alias="Name")


class NocoCourses(RootModel[list[NocoPerson]]):
    TABLE_NAME = "Course"
    root: list[NocoPerson]

    @classmethod
    def from_nocodb(cls):
        raw = get_nocodb_data(cls.TABLE_NAME)
        return cls.model_validate(raw["list"])