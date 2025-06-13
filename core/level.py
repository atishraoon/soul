import json 
 
class LevelManager:
    def __init__(self, display_path):

        with open(display_path, 'r') as f:
            self.data = json.load(f)
        self.current_level = 0  
    
    def get_level_data(self, level):
        for level_data in self.data['alllevels']:
            if int(level_data['level']) == level:
                return level_data
        return None
    
    def unlock_next_level(self):
        self.current_level += 1
        return self.get_level_data(self.current_level)


    def get_daily_data(self, daily):
        for daily_data in self.data['dailyquest']:
            if int(daily_data['task']) == daily:
                return daily_data
        return None

    
    def get_all_data(self):
        """Returns the complete JSON data loaded from the file"""
        return self.data