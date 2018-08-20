'''
    Class that parses data from Mobileye. 
    Will need to be threaded to run async. with server 
'''

class MobileyeData: 
    def __init__(self):
        self.can_channel = self.init_can() 
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

    def init_can(self,channel=0,openFlags=0,bitrate=0,bitrateFlags=0):
        ch = canlib.openChannel(channel,openFlags)
        ch.setBusOutputControl(bitrateFlags)
        ch.setBusParams(bitrate)
        ch.busOn()
        return ch

    def get_data(self):
        try: 
            frame = self.can_channel.read()
            msg_id = frame.id
            data = frame.data
        except (canlib.canNoMsg) as ex: 
            pass
        except (canlib.canError) as ex: 
            print(ex)
        #callback? 
        #yield json object containing graph and data
    
    def calculate_curve(self):
        pass
    
    def tear_down_channel(self):
        self.can_channel.busOff()
        self.can_channel.close() 