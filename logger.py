class Logger:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def heading(self , text: str):
        print(self.HEADER + text + self.ENDC)

    def info(self , text: str):
        print(self.OKCYAN + text + self.ENDC)

    def warn(self , text: str):
        print(self.WARNING + text + self.ENDC)

    def error(self , text: str):
        print(self.FAIL + text + self.ENDC)

    def success(self , text: str):
        print(self.OKGREEN + text + self.ENDC)
        