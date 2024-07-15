class ResultManager:

    def __init__(self):
        self.result_file_path = None

    def write(self, text):
        with open(self.result_file_path, 'w') as f:
            f.write(text)
