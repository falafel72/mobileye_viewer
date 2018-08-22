from flask import Flask,Response,render_template,jsonify
import time 
import random
import subprocess

app = Flask(__name__)

@app.route('/',methods=['GET'])
def show_charts():
    return render_template('index.html')

# might want to change this so that it waits for all four packets to arrive before processing
def read_can(): 
    can_stream = subprocess.Popen(['./can_receive'],stdout=subprocess.PIPE) 
    while True: 
        packet = can_stream.stdout.readline()
        data = packet.split(' ')
        can_id = int(data[1],16)
        can_data = [int(i,16) for i in data[3:]]
        if can_id == 0x766 or can_id == 0x767 or can_id == 0x768 or can_id == 0x769: 
            yield can_id,can_data 
        else: 
            yield None,None

def parse_data():
    left_lane_p1 = []
    left_lane_p2 = []
    right_lane_p1 = []
    right_lane_p2 = []
    for can_id,data in read_can():
        if can_id == None:
            continue
        if can_id == 0x766: 
            left_lane_p1 = data
        if can_id == 0x767: 
            left_lane_p2 = data
        if can_id == 0x768: 
            right_lane_p1 = data
        if can_id == 0x769: 
            right_lane_p2 = data
            return get_lanes(left_lane_p1,left_lane_p2,right_lane_p1,right_lane_p2)
    
def get_lanes(left_p1,left_p2,right_p1,right_p2):
    lc0 = tos16((left_p1[2] << 8) + left_p1[1])
    lc1 = (((left_p2[1] << 8) + left_p2[0]) - 0x7fff)/1024.0
    lc2 = (((left_p1[4] << 8) + left_p1[3]) - 0x7fff)/1024.0 
    lc3 = (((left_p1[6] << 8) + left_p1[5]) - 0x7fff)/(1<<28) 
    left_range = (((left_p2[3] >> 1) << 8) + left_p2[2])/256.0

    rc0 = tos16((right_p1[2] << 8)+right_p1[1])
    rc1 = (((right_p2[1] << 8) + right_p2[0]) - 0x7fff)/1024.0
    rc2 = (((right_p1[4] << 8) + right_p1[3]) - 0x7fff)/1024.0 
    rc3 = (((right_p1[6] << 8) + right_p1[5]) - 0x7fff)/(1<<28) 
    right_range = (((right_p2[3] >> 1) << 8) + right_p2[2])/256.0
    
    left_y = range(int(left_range))
    right_y = range(int(right_range))
    
    ldict = {{'x':lc3*y**3 + lc2*y**2 + lc1*y + lc0,'y':y} for y in left_y}
    rdict = {{'x': rc3*y**3 + rc2*y**2 + rc1*y + rc0,'y':y} for y in right_y}
    return {'left': ldict, 'right': rdict}

def tos16(val):
    return -(val & 0x8000) | (val & 0x7fff)

app.route('/lanedata')
def get_lane_data():
    # obtain lane data from the MobileyeData class, pass it to the server by returning or using an event stream
    def stream(): 
        while True: 
            lane_data = parse_data()
            if lane_data is None: 
                yield ':'
            else: 
                yield 'data: %s' % str(lane_data) 

    return Response(stream(),mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True,port=5000,host='localhost')