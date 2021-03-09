
# Функция ниже, чтобы избежать ошибку TypeError: can't send non-None value to a just-started generator
def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper


class FSM:
    """Класс конечного автомата"""
    def __init__(self):
        """Инициализация"""
        #self.start = self._create_start()
        # инициализация состояний
        self.q0 = self._create_q0()
        self.start = self.q0
        self.q1 = self._create_q1()
        self.q2 = self._create_q2()
        self.q3 = self._create_q3()
        self.q4 = self._create_q4()
        self.q5 = self._create_q5()
        self.q6 = self._create_q6()
        # установка текущего состояния системы
        self.current_state = self.start
        # флаг остановки, для обозначения
        # остановки итерации из-за некорректного
        # входа, для которого переход не был определен.
        self.stopped = False

    def send(self, char):
        """Функция отправляет текущий ввод в current_state. В случае ошибки
        она захватывает исключение StopIteration и помечает флаг stopped."""
        try:
            self.current_state.send(char)
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
        return self.current_state == self.q6

    """@prime
    def _create_start(self):
        while True:
            # Ждем, пока ввод не будет получен.
            # после получения сохраняем ввод в `char`
            char = yield
            # изменяем текущее состояние fsm
            if char == 'a':
                # при получении `а` состояние перемещается в `q0`
                self.current_state = self.q1
            else:
                break"""

    @prime
    def _create_q0(self):
        while True:
            # Ждем, пока ввод не будет получен.
            # после получения сохраняем ввод в `char`
            char = yield
            # в зависимости от того, что мы получили в
            # качестве входных данных
            # изменяем текущее состояние fsm
            if char == 'b':
                # при получении `b` состояние перемещается в `q0`
                self.current_state = self.q0
            elif char == 'c':
                # при получении `с` состояние перемещается в `q0`
                self.current_state = self.q0
            elif char == 'a':
                # при получении `а` состояние перемещается в `q1`
                self.current_state = self.q1
            else:
                # при получении любого другого ввода, останавливаем цикл
                #  чтобы в следующий раз, когда кто-нибудь что-нибудь
                # отправит вызывать StopIteration
                break

    # Остальные функции по такому же принципу, как _create_q0
    @prime
    def _create_q1(self):
        while True:
            char = yield
            if char == 'b':
                self.current_state = self.q2
            elif char == 'c':
                self.current_state = self.q0
            elif char == 'a':
                self.current_state = self.q1
            else:
                break

    @prime
    def _create_q2(self):
        while True:
            char = yield
            if char == 'b':
                self.current_state = self.q0
            elif char == 'c':
                self.current_state = self.q0
            elif char == 'a':
                self.current_state = self.q3
            else:
                break

    @prime
    def _create_q3(self):
        while True:
            char = yield
            if char == 'b':
                self.current_state = self.q4
            elif char == 'c':
                self.current_state = self.q0
            elif char == 'a':
                self.current_state = self.q1
            else:
                break

    @prime
    def _create_q4(self):
        while True:
            char = yield
            if char == 'b':
                self.current_state = self.q0
            elif char == 'c':
                self.current_state = self.q0
            elif char == 'a':
                self.current_state = self.q5
            else:
                break

    @prime
    def _create_q5(self):
        while True:
            char = yield
            if char == 'b':
                self.current_state = self.q4
            elif char == 'c':
                self.current_state = self.q6
            elif char == 'a':
                self.current_state = self.q1
            else:
                break

    @prime
    def _create_q6(self):
        while True:
            char = yield
            break


class Validate:
    """Класс валидации выражения"""
    def grep_regex(self, text):
        """Функция проверяет полученный текст на соответствие корректным переходам"""
        # Создаём объект конечного автоматка
        evaluator = FSM()
        # перебираем каждый символ полученного выражения
        for ch in text.lower():
            # передаем в конечный автомат
            evaluator.send(ch)
        # возвращаем соответствие выражения
        return evaluator.does_match()


if __name__ == '__main__':
    # отправляем на проверку последовательность переходов
    print(Validate().grep_regex("ABABAC"))

