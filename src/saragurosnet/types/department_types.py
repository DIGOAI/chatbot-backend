from typing import Final, TypedDict


class DepartmentDataType(TypedDict):
    NAME: str
    ID: int


class DepartmentType():
    SUPPORT: Final[DepartmentDataType] = {"NAME": "Soporte Técnico", "ID": 1}
    SALES: Final[DepartmentDataType] = {"NAME": "Ventas", "ID": 2}
    CLAIMS: Final[DepartmentDataType] = {"NAME": "Quejas y Sugerencias", "ID": 3}
