import re
from collections import OrderedDict

mention_finder = re.compile(r'\<@!(\d+)\>').findall

class CacheDict(OrderedDict):
    def __init__(self, *args, **kwds):
        self.max = kwds.pop("max", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.max is not None:
            while len(self) > self.max:
                self.popitem(last=False)

# Sniping rules
def anarchy(rolled,user,message):
    return True

def partial_restriction(rolled, user, message):
    # Locked only if *roller* has a wish on character
    if user == rolled:
        return True
    wished_for = mention_finder(message)
    if wished_for and rolled in wished_for:
        return False
    return True

def full_restriction(rolled,user,message):
    # Roller only
    return user == rolled

def wish_restriction_2(rolled,user,message):
    # Locked if wished character to only wishers
    wished_for = mention_finder(message)
    if (not wished_for) or user['id'] in wished_for:
        return True
    # Wished character, and we haven't wished
    return False

def wish_restriction_1(rolled,user,message):
    # Locked if wished character to roller and wishers
    return user == rolled or wish_restriction_2(rolled,user,message)

def combined_restriction_2(rolled,user,message):
    # Locked to wishers -- if not wished for, locked to roller
    wished_for = mention_finder(message)
    if not wished_for:
        # Not wished character, must be roller
        return user == rolled
    elif user['id'] in wished_for:
        # We've wished for it
        return True
    # Neither wisher nor roller
    return False
    
def combined_restriction_1(rolled,user,message):
    # Locked to wishers and roller.
    return user == rolled or combined_restriction_2(rolled,user,message)

snipe_logic = {0:anarchy, 1:partial_restriction, 2:full_restriction, 3:wish_restriction_1, 4:wish_restriction_2, 5:combined_restriction_1, 6:combined_restriction_2}
