class DistanceScore:
    def __init__(self, edit_distance, max_score):
        self.edit_distance = edit_distance
        self.max_score = max_score

    def __str__(self):
        return f"{self.edit_distance} {self.max_score}"

    def percentage_score(self):
        if self.edit_distance == 0:
            return 1
        else:
            return 1 - (self.edit_distance / self.max_score)
