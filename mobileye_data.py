import subprocess
import math 

class MobileyeData(): 
    def __init__(self):
        self.left_p1 = []
        self.left_p2 = []
        self.right_p1 = []
        self.right_p2 = []
        self.dcu_speed_p = []
        self.past_lx = []
        self.past_ly = []
        self.past_rx = []
        self.past_ry = []
        self.current_lx = []
        self.current_ly= []
        self.current_rx = []
        self.current_ry = []
        self.past_speed = 0
        self.current_speed = 0
        self.current_heading = 0
        self.past_heading = 0

    def read_can(self): 
        can_stream = subprocess.Popen(['candump','can0'],stdout=subprocess.PIPE) 
        while True: 
            packet = can_stream.stdout.readline()
            if packet != '':
                data = packet.split(' ')
                can_id = int(data[4],16)
                can_data = [int(i,16) for i in data[9:]]
                if can_id == 0x766 or can_id == 0x767 or can_id == 0x768 or can_id == 0x769 or can_id == 0x600: 
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
            if can_id == 0x600: 
                self.dcu_speed_p = data
                if self.left_p1 != [] and self.left_p2 != [] and self.right_p1 != [] and self.right_p2 != [] and self.dcu_speed_p != []:	
                    yield self.get_lanes()

    def get_lanes(self):
        tos16 = lambda(val): -(val & 0x8000) | (val & 0x7fff)

        lc0 = tos16((self.left_p1[2] << 8) + self.left_p1[1])/256.0
        lc1 = (((self.left_p2[1] << 8) + self.left_p2[0]) - 0x7fff)/1024.0
        lc2 = (((self.left_p1[4] << 8) + self.left_p1[3]) - 0x7fff)/1024.0/1000.0
        lc3 = (((self.left_p1[6] << 8) + self.left_p1[5]) - 0x7fff)/(1<<28) 
        left_range = (((self.left_p2[3] >> 1) << 8) + self.left_p2[2])/256.0
        #print 'Left: %d %f %f %f' % (lc0,lc1,lc2,lc3)

        rc0 = tos16((self.right_p1[2] << 8) + self.right_p1[1])/256.0
        rc1 = (((self.right_p2[1] << 8) + self.right_p2[0]) - 0x7fff)/1024.0
        rc2 = (((self.right_p1[4] << 8) + self.right_p1[3]) - 0x7fff)/1024.0/1000.0 
        rc3 = (((self.right_p1[6] << 8) + self.right_p1[5]) - 0x7fff)/(1<<28) 
        right_range = (((self.right_p2[3] >> 1) << 8) + self.right_p2[2])/256.0
        #print 'Right: %d %f %f %f' % (rc0,rc1,rc2,rc3) 

        self.past_lx = self.current_lx
        self.past_ly = self.current_ly
        self.past_rx = self.current_rx
        self.past_ry = self.current_ry
        self.current_ly = range(int(left_range))
        self.current_ry = range(int(right_range))
        self.current_lx = [lc3*y**3 + lc2*y**2 + lc1*y + lc0 for y in self.current_ly]
        self.current_rx = [rc3*y**3 + rc2*y**2 + rc1*y + rc0 for y in self.current_ry]
        self.past_speed = self.current_speed
        self.current_speed = ((self.dcu_speed_p[1] << 8) + self.dcu_speed_p[0])/256.0
        self.past_heading = self.current_heading
        self.current_heading = (lc1 + rc1)/2

        l_xtrans,l_ytrans,r_xtrans,r_ytrans = [],[],[],[]
        if self.past_lx != [] and self.past_rx != []:
            dist_per_frame = self.past_speed/3.6/10
            dx = math.sin(self.current_heading)*dist_per_frame
            dy = math.cos(self.current_heading)*dist_per_frame
            ltrans_len = len([y for y in self.past_ly if y < dy])
            rtrans_len = len([y for y in self.past_ry if y < dy])
            l_xtrans,l_ytrans = self.transform_coords(self.past_lx[:ltrans_len],self.past_ly[:ltrans_len],self.current_heading,dx,dy)
            r_xtrans,r_ytrans = self.transform_coords(self.past_rx[:rtrans_len],self.past_ry[:rtrans_len],self.current_heading,dx,dy)

            self.current_lx = l_xtrans + self.current_lx
            self.current_ly = l_ytrans + self.current_ly
            self.current_rx = r_xtrans + self.current_rx
            self.current_ry = r_ytrans + self.current_ry
            
            if len(self.current_lx) > 240:
                self.current_lx = self.current_lx[len(self.current_lx)-240:]
            if len(self.current_ly) > 240:
                self.current_ly= self.current_ly[len(self.current_ly)-240:]
            if len(self.current_rx) > 240:
                self.current_rx = self.current_rx[len(self.current_rx)-240:]
            if len(self.current_ry) > 240:
                self.current_ry = self.current_ry[len(self.current_ry)-240:]

        llist = [{"x":self.current_lx[i],"y":self.current_ly[i]} for i in range(len(self.current_lx))]
        rlist = [{"x":self.current_rx[i],"y":self.current_ry[i]} for i in range(len(self.current_rx))]

        return {"left": llist, "right": rlist, "speed":[self.current_speed], "heading":[self.current_heading*180/math.pi]}
    
    def transform_coords(self,inx,iny,theta,dx,dy):
        outx,outy = [],[]
        for i in range(len(iny)):
            outx.append(math.cos(theta)*inx[i] - math.sin(theta)*iny[i] - dx)
            outy.append(math.cos(theta)*iny[i] + math.sin(theta)*inx[i] - dy)
        return outx,outy