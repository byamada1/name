class fighter:
    
    name = "blank"
    atk_min = 0
    atk_max = 10
    arm = 0
    hp = 100

    def __init__(self, nm, a_min, a_max, ar, h_p):
        self.name = nm
        self.atk_min = a_min
        self.atk_max = a_max
        self.arm = ar
        self.hp = h_p