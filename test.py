import abc


class Combiner:
    @abc.abstractmethod
    def combine(self, x: int, y: int) -> int:
        """

        :param x:
        :param y:
        :return:
        """
        raise NotImplementedError

    def __str__(self):
        return self.__class__

    def __repr__(self):
        return self.__annotations__


class Add(Combiner):
    def __init__(self):
        pass

    def combine(self, x: int, y: int) -> int:
        """

        :param x:
        :param y:
        :return:
        """
        return x + y


class Multiply(Combiner):
    def __init__(self):
        pass

    def combine(self, x: int, y: int) -> int:
        """

        :param x:
        :param y:
        :return:
        """
        return x * y


if __name__ == '__main__':
    add = Add()
    mult = Multiply()
