

class Folgerungsgraph:
  activites = []
  variants = {}

  def __init__(self, act = [], var = {}):
    self.activites = act
    self.variants = var