class NonPositiveDigitException(ValueError):
    pass
class Square:
    def __uni__(self, a):

        if a <= 0:
            raise NonPositiveDigitException('Error')


