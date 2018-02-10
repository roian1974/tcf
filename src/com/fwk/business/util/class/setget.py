class Example(object):
    def __init__(self, value):
        self.setx(value)

    def getx(self):
        return self.x

    def setx(self, value) :
        self.x = value


class Example2(object):
    def __init__(self, value):
        self.x = value


instance2 = Example2(42)
print (instance2.x)  # gives 42
instance2.setx(23)

instance = Example(42)
print (instance.getx())  # gives 42
instance.setx(23)
print (instance.getx())  # gives 42

