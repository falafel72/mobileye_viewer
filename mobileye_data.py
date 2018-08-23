import subprocess

class MobileyeData(): 
    def __init__(self):
        self.left_p1 = []
        self.left_p2 = []
        self.right_p1 = []
        self.right_p2 = []

    def read_can(self): 
        can_stream = subprocess.Popen(['candump','can0'],stdout=subprocess.PIPE) 
        while True: 
            packet = can_stream.stdout.readline()
            data = packet.split(' ')
            can_id = int(data[4],16)
            can_data = [int(i,16) for i in data[9:]]
            if can_id == 0x766 or can_id == 0x767 or can_id == 0x768 or can_id == 0x769: 
                yield can_id,can_data 
            else: 
                yield None,None

    def parse_data(self):
        for can_id,data in self.read_can():
            if can_id == None:
                continue
            if can_id == 0x766: 
                self.left_p1 = data
            if can_id == 0x767: 
                self.left_p2 = data
            if can_id == 0x768: 
                self.right_p1 = data
            if can_id == 0x769: 
                self.right_p2 = data
            if self.left_p1 != [] and self.left_p2 != [] and self.right_p1 != [] and self.right_p2 != []:	
                yield self.get_lanes()

    def get_lanes(self):
        tos16 = lambda(val): -(val & 0x8000) | (val & 0x7fff)

        lc0 = tos16((self.left_p1[2] << 8) + self.left_p1[1])/256.0
        lc1 = (((self.left_p2[1] << 8) + self.left_p2[0]) - 0x7fff)/1024.0
        lc2 = (((self.left_p1[4] << 8) + self.left_p1[3]) - 0x7fff)/1024.0 
        lc3 = (((self.left_p1[6] << 8) + self.left_p1[5]) - 0x7fff)/(1<<28) 
        left_range = (((self.left_p2[3] >> 1) << 8) + self.left_p2[2])/256.0
        #print 'Left: %d %f %f %f' % (lc0,lc1,lc2,lc3)

        rc0 = tos16((self.right_p1[2] << 8) + self.right_p1[1])/256.0
        rc1 = (((self.right_p2[1] << 8) + self.right_p2[0]) - 0x7fff)/1024.0
        rc2 = (((self.right_p1[4] << 8) + self.right_p1[3]) - 0x7fff)/1024.0 
        rc3 = (((self.right_p1[6] << 8) + self.right_p1[5]) - 0x7fff)/(1<<28) 
        right_range = (((self.right_p2[3] >> 1) << 8) + self.right_p2[2])/256.0
        #print 'Right: %d %f %f %f' % (rc0,rc1,rc2,rc3) 

        left_y = range(int(left_range))
        right_y = range(int(right_range))
        
        llist = [{"x":lc3*y**3 + lc2*y**2 + lc1*y + lc0,"y":y} for y in left_y]
        rlist = [{"x": rc3*y**3 + rc2*y**2 + rc1*y + rc0,"y":y} for y in right_y]
        return {"left": llist, "right": rlist}
