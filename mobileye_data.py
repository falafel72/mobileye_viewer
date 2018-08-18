'''
    Class that parses data from Mobileye. 
    Will need to be threaded to run async. with server 
'''

class MobileyeData: 
    def __init__(self):
        self.left_lane_x = []
        self.right_lane_x = []
        self.fd_range = []
        self.lc0 = 0
        self.rc1 = 1
        self.lc1 = 0
        self.rc1 = 0
        self.lc2 = 0
        self.rc2 = 0
        self.lc3 = 0
        self.rc3 = 0

    def init_can(self):
        pass

    def get_data(self):
        #callback? 
        pass
    
    def calculate_curve(self):
        pass