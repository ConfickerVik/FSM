
# Функция ниже, чтобы избежать ошибку TypeError: can't send non-None value to a just-started generator
def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper


class MP:
    """Класс конечного автомата с магазинной памятью"""
    def __init__(self):
        """Инициализация"""
        self.stack = []
        self.star_state = '!'
        # установка стартового состояния системы
        self.stack.append(self.star_state)
        # флаг остановки, для обозначения
        # остановки итерации из-за некорректного
        # входа, для которого переход не был определен.
        self.stopped = False
        # инициализация состояний
        self.zero = self._zero()
        self.one = self._one()
        self.current_state = self.zero

    def send(self, state):
        """Функция отправляет текущий ввод в current_state. В случае ошибки
        она захватывает исключение StopIteration и помечает флаг stopped."""
        try:
            self.current_state.send(state)
        except StopIteration:
            self.stopped = True

    def does_match(self):
        """Функция в любой момент времени возвращает True, если
        текущее состояние соответствует заданному конечному состоянию.
        Она также проверяет наличие флага stopped, который назначается,
        при неправильном вводе и дальнейшея итерация конечного автомата
        должна была быть остановлена."""
        if self.stopped:
            return False
        return self._top() == self.star_state

    @prime
    def _zero(self):
        """Состояние ноль"""
        while True:
            # Ждем, пока ввод не будет получен.
            # после получения сохраняем ввод в `char`
            char = yield
            # в зависимости от того, что мы получили в
            # качестве входных данных
            # изменяем текущее состояние MP
            if char == '0':
                # при получении `0` добавляем в стек сотояние
                self._push(char)
                # смотрим верхний элемент стека
                self._top()
                # смотрим сам стек
                print(self.stack)
                # состояние перемещается в `zero`
                self.current_state = self.zero
            elif char == '1':
                # при получении `1` удаляем из стека сотояние `0`
                self._pop()
                # смотрим верхний элемент стека
                self._top()
                # смотрим сам стек
                print(self.stack)
                # состояние перемещается в `one`
                self.current_state = self.one
            else:
                # self.stopped = True
                # при получении любого другого ввода, останавливаем цикл
                # чтобы в следующий раз, когда кто-нибудь что-нибудь
                # отправит вызывать StopIteration

                break

    @prime
    def _one(self):
        """Состояние ноль"""
        while True:
            # Ждем, пока ввод не будет получен.
            # после получения сохраняем ввод в `char`
            char = yield
            # в зависимости от того, что мы получили в
            # качестве входных данных
            # изменяем текущее состояние MP
            if char == '1':
                # при получении `1` удаляем из стека сотояние `0`
                self._pop()
                # смотрим верхний элемент стека
                self._top()
                # смотрим сам стек
                print(self.stack)
                # состояние перемещается в `one`
                self.current_state = self.one
            else:
                # self.stopped = True
                # при получении любого другого ввода, останавливаем цикл
                # чтобы в следующий раз, когда кто-нибудь что-нибудь
                # отправит вызывать StopIteration
                break

    def _push(self, state):
        """Добавление в стек"""
        self.stack.append(state)

    def _pop(self):
        """Удаление из стека"""
        self.stack.pop(-1)

    def _top(self):
        """Верхний элемент стека"""
        return self.stack[-1]


class Validate:
    """Класс валидации выражения"""
    def grep_regex(self, text):
        """Функция проверяет полученный текст на соответствие корректным переходам"""
        # Создаём объект конечного автоматка
        evaluator = MP()
        # перебираем каждый символ полученного выражения
        for ch in text.lower():
            # передаем в конечный автомат
            evaluator.send(ch)
        # возвращаем соответствие выражения
        return evaluator.does_match()


if __name__ == "__main__":
    print(Validate().grep_regex("00001111"))
