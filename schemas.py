from pydantic import BaseModel, ConfigDict, Field

class postBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)

class CreatePost(postBase):
    pass 

class ResponsePost(postBase):
    model_config = ConfigDict(from_attributes=True)

    id:int
    date_posted:str
