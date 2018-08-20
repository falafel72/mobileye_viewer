from flask import Flask,Response,render_template
from mobileye_data import MobileyeData

app = Flask(__name__)

@app.route('/',methods=['GET'])
def show_charts():
    # p1 = figure(plot_width=500,plot_height=750,title='Lane Plot')
    # p2 = figure(plot_width=400,plot_height=250,title='Current Speed')
    # p3 = figure(plot_width=400,plot_height=250,title='Current Heading')
    # p4 = figure(plot_width=400,plot_height=250,title='Current Distance')

    # group = row(p1,column(p2,p3,p4))

    # script,div = components(group)
    
    return render_template('index.html')


@app.route('/lanedata')
def get_lane_data():
    # obtain lane data from the MobileyeData class, pass it to the server by returning or using an event stream
    def stream(): 
        yield 'data: HI\n\n'
    return Response(stream(),mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True,port=5000,host='localhost')