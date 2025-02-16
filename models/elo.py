class ELOSystem:
    K_FACTOR = 32
    INITIAL_RATING = 1000

    # TODO verify calculations again
    @classmethod
    def expected_score(cls, rating_1: int, rating_2: int):
        return 1 / (1 + 10 ** ((rating_2 - rating_1) / 400))

    @classmethod
    def update_rating(cls, rating_1: int, rating_2: int, score: float) -> tuple[int, int]:
        expected_score = cls.expected_score(rating_1, rating_2)
        new_rating_1 = round( rating_1 + cls.K_FACTOR * (score - expected_score))
        new_rating_2 = round(rating_2 + cls.K_FACTOR * (1 - score - expected_score))
        return new_rating_1, new_rating_2