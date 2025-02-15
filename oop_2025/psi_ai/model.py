import typing_extensions
from pydantic import BaseModel, Field


class Personality(BaseModel):
    pass


class HEXACO_Personality(Personality):
    honesty_humility: float | None = None
    emotionality: float | None = None
    extraversion: float | None = None
    agreeableness: float | None = None
    conscientiousness: float | None = None
    openness: float | None = None


class ProgrammerPersonality(HEXACO_Personality):
    coding_skills: float | None = None
    system_design: float | None = None
    code_ownership: float | None = None


class PersonalityFusionEngine:

    def fuse(self, personalities: list[Personality], weights: list[float]) -> Personality:
        # weights = [0.99, 0.01]
        pass


if __name__ == '__main__':
    pass
