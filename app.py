from flask import Flask,Response,render_template,jsonify
import subprocess
from json import dumps as JSONdumps
from mobileye_data import MobileyeData

app = Flask(__name__)

@app.route('/',methods=['GET'])
def show_charts():
    return render_template('index.html')

@app.route('/lanedata')
def get_lane_data():
    # obtain lane data from the MobileyeData class, pass it to the server by returning or using an event stream
    def stream(): 
        mobileye_parser = MobileyeData()
        for lane_data in mobileye_parser.parse_data():
            if lane_data is None: 
                yield ':'
            else: 
                yield 'data: %s\n\n' % JSONdumps(lane_data) 
    return Response(stream(),mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=False,port=5000,host='0.0.0.0')