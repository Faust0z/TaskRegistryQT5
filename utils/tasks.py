class Tasks():
    def __init__(self, id: int, type_id: int, minutes_spent: int, date: str, description: str):
        self.id = id
        self.type_id = type_id
        self.minutes_spent = minutes_spent
        self.date = date
        self.description = description if description else "No description"