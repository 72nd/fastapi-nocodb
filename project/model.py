from attr import validate
from .config import settings
from typing import Any, Optional, Union

from datetime import datetime

from nocodb.nocodb import APIToken, NocoDBProject, WhereFilter
from nocodb.infra.requests_client import NocoDBRequestsClient
from pydantic import BaseModel, ConfigDict, Field, FieldValidationInfo, model_validator, RootModel


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
    root: list[NocoPerson]

    @classmethod
    def from_nocodb(cls):
        raw = get_nocodb_data("Person")
        return cls.model_validate(raw["list"])


class NocoCourse(BaseModel):
    noco_id: int = Field(alias="Id")
    created_at: datetime = Field(alias="CreatedAt")
    updated_at: datetime = Field(alias="UpdatedAt")
    name: str = Field(alias="Name")
    students: Optional[NocoPersons] = None

    @model_validator(mode="after")
    def load_linked_students(self):
        client = get_nocodb_client()
        raw = client.table_row_nested_relations_list(
            get_nocodb_project(),
            "Course",
            "mm",
            self.noco_id,
            "Students"
        )
        self.students = NocoPersons.model_validate(raw["list"])
        return self


class NocoCourses(RootModel[list[NocoPerson]]):
    root: list[NocoCourse]

    @classmethod
    def from_nocodb(cls):
        raw = get_nocodb_data("Course")
        return cls.model_validate(raw["list"], strict=False)