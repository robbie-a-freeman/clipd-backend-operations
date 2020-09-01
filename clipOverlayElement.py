import re

class clipOverlayElement:

    p1 = (-1., -1.)
    p2 = (-1., -1.)
    name = ''
    # should be regex
    expectedInput = ''
    
    def __init__(self, p1, p2, name, expectedInput):
        self.p1 = p1
        self.p2 = p2
        self.name = name
        self.expectedInput = expectedInput

    def isStrCompatibleWith(self, str):
        if self.expectedInput is 'ICON':
            return False
        else:
            return re.compile(self.expectedInput).match(str)
