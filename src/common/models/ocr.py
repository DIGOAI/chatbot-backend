from pydantic import BaseModel, Field


class MakeOCRForm(BaseModel):
    image: str = Field(examples=["some base64 image, or some image url `https://pbs.twimg.com/media/D8zt8pcWwAQeRZI.jpg`",
                       "https://pbs.twimg.com/media/D8zt8pcWwAQeRZI.jpg"])


class MakeOCRResponse(BaseModel):
    text: str
    image: str = Field(examples=["a base64 image"])
