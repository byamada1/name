from tempfile import tempdir


class fighter:
    
    name = "blank"
    atk_min = 0
    atk_max = 10
    atk_str = "0 - 10"
    arm = 0
    arm_str = "0"
    hp = 100
    hp_max = 100
    sprite = 0
    weapon_atk = 0
    armor_arm = 0

    def __init__(self, nm, a_min, a_max, ar, h_p, img):
        self.name = nm
        self.atk_min = a_min
        self.atk_max = a_max
        self.arm = ar
        self.hp = h_p
        self.hp_max = h_p

        self.sprite = img
        self.update_arm()
        self.update_atk()
    
    def update_atk(self):
        if(self.atk_min > self.atk_max):
            temp = self.atk_min
            self.atk_min = self.atk_max
            self.atk_max = temp
        self.atk_str = str(self.atk_min + self.weapon_atk) + " - " + str(self.atk_max + self.weapon_atk)


    def update_arm(self):
        self.arm_str = str(self.arm + self.armor_arm)

    def update(self):
        self.update_arm()
        self.update_atk()
