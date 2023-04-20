class Auto:
    def __init__(self, name):
        self.n = name

    def change_self(self, name):
        self = Auto(name)

    def __str__(self):
        return (f"car is {self.n}")


if __name__ == "__main__":
    car = Auto("cheln")
    print(car)
    car.change_self("free")
    print(car)