from pydantic import BaseModel, Field


class PersonalityTraits(BaseModel):
    honesty_humility: float = Field(ge=0, le=10, description="Score for sincerity, fairness, and modesty")
    emotionality: float = Field(ge=0, le=10, description="Score for anxiety, dependence, and sentimentality")
    # extraversion: float = Field(ge=0, le=10, description="Score for sociability, liveliness, and expressiveness")
    # agreeableness: float = Field(ge=0, le=10, description="Score for patience, tolerance, and gentleness")
    # conscientiousness: float = Field(ge=0, le=10, description="Score for organization, diligence, and perfectionism")
    # openness: float = Field(ge=0, le=10, description="Score for creativity, inquisitiveness, and unconventionality")


if __name__ == '__main__':
    x = PersonalityTraits(honesty_humility=5.0, emotionality=5.0)
    print(x)