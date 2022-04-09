class box:
    rect = 0
    color = 0
    text = ""
    text_color = 0

    def __init__(self, rt, cl, tx, tx_cl):
        self.rect = rt
        self.color = cl
        self.text = tx
        self.text_color = tx_cl