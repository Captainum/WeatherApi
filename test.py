from unittest.mock import patch

def meww(self):
    return 'no'

class Cat:
    def __init__(self, name):
        self._name = name

    def meow(self):
        print('meow')

    @patch('meow', meww)
    def do_smth(self, to_do='meow'):
        if to_do == 'meow':
            self.meow()

cat = Cat('Petya')
cat.do_smth()
