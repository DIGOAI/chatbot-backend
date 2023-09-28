from typing import Annotated

from fastapi import Depends, Path


async def company_parameters(company: Annotated[str, Path(description='The company name to use in the request')]):
    return company


CompanyDep = Annotated[str, Depends(company_parameters)]
