from model import *


@typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)
def foo(x):
    print(x)


if __name__ == '__main__':
    x = HEXACO_Personality(honesty_humility=0.5, emotionality=0.5, extraversion=0.5,
                           agreeableness=0.5, conscientiousness=0.5)

    print(isinstance(x, HEXACO_Personality))  # True
    print(isinstance(x, Personality))  # True
    print(x.model_dump_json())
    s = x.model_dump_json()
    y = HEXACO_Personality.model_validate_json(s)
    print(y)
    # foo(12) # todo: how to emit warning in console, when this function is used...

    zz = '{"honesty_humility": 0.36, "emotionality": 0.71, "extraversion": 0.43, "agreeableness": 0.43, "conscientiousness": 0.93, "openness": 1.0    }'

    elon = HEXACO_Personality.model_validate_json(zz)
    print(elon)