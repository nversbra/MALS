

import random


memory_size = 1000000
history_length = 4

class ReplayMemory:
  def __init__(self):

    self.memory_size = memory_size
    self.rolouts = [None] * memory_size
    self.count = 0
    self.current = 0


  def add(self, rolout):
    self.rolouts[self.current] = rolout
    self.count = max(self.count, self.current + 1)
    self.current = (self.current + 1) % self.memory_size



  def sample(self):
    index = random.randint(0, self.count - 1)


    return self.rolouts[index]


