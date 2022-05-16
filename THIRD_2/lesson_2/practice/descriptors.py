class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            raise ValueError(f'Порт должен быть в диапазоне [1024, ..., 65535]. Текущее значение {value}.')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

