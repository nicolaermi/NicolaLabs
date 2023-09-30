class Players:
    """This is a class where we can define a player name and assign a score
    we can then increase the score by 1, it will print out the name and the score, and it can print out only
    the name with the function get_name"""
    def __init__(self, name, score=0):
        self.name = name  # Player's name
        self.score = score  # Player's score, default is 0
        
    def increase_score(self):
        """Increase the player's score by 1"""
        self.score += 1
        
    def __str__(self):
         return f"{self.name}:{self.score}"
    
    def get_name(self):
        return self.name
    def get_score (self): 
        return self.score
