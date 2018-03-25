from flask import render_template, Flask, request
#0:call_number
#1: unit_id
#2: incident_number
#3: call_type
#4: call_date
#5: watch_date
#received_timestamp
#entry_timestamp
#ranges from jan 13 to jan 25
def get_dispatch_times(address):
    file = open("C:\Python34\sfpd-dispatch\sfpd-dispatch\sfpd_dispatch_data_subset.csv", 'r')
    categories = file.readline()
    count = 0
    dispatch_times={}
    line = "a"
    while(line):
        line = file.readline()
        time_sum = 0
        if(line != ""):
            line=line.split(",")
            date = line[8]
            time_sum = int(date[11:13])*3600+int(date[14:16])*60+int(date[17:19])
            if(address == line[15]):
                if(time_sum in dispatch_times.keys()):
                    dispatch_times[time_sum].append(line[3])
                else:
                    dispatch_times[time_sum] = [line[3]]
    file.close()
    return dispatch_times

def get_most_likely_dispatch(dispatch_times, hour, minute, second):
    time_sum = hour*3600+minute*60+second
    variance = 0
    closest_dispatches = []
    count = 0
    #print(len(dispatch_times))
    while(count < 3):
        try:
            if(len(dispatch_times[time_sum+variance]) > 0):
                count += len(dispatch_times[time_sum+variance])
                for i in dispatch_times[time_sum+variance]:
                    closest_dispatches.append(i)
                    #print(i)
                    #print(variance)
        except:
            pass
        try:
            if(len(dispatch_times[time_sum-variance]) > 0):
                count += len(dispatch_times[time_sum-variance])
                for i in dispatch_times[time_sum-variance]:
                    closest_dispatches.append(i)
                    #print(variance)
        except:
            pass
        variance += 1
        if(variance > 3600*24):
            print("NOT FOUND")
            break
    return closest_dispatches

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('index.html')

dispatch_times = get_dispatch_times("PINE ST/POLK ST")
print(get_most_likely_dispatch(dispatch_times,5,5,5))

if __name__ == "__main__":
    app.run()
