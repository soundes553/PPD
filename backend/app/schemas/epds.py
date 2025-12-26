from pydantic import BaseModel

class OptionResponse(BaseModel):
    option_id: int
    option_text: str
    answer_value: int
    option_order: int

    model_config = {"from_attributes": True}


class QuestionResponse(BaseModel):
    question_id: int
    question_text: str
    options: list[OptionResponse] = []

    model_config = {"from_attributes": True}
