from flask import render_template, Flask, request, url_for

#SECTION 1 -- PYTHON DATA PARSING
def get_dispatch_times(address):
    file = open("/app/sfpd_dispatch_data_subset.csv", 'r')
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
    times =[]
    count = 0
    
    while(count < 5):
        try:
            if(len(dispatch_times[time_sum+variance]) > 0):
                count += len(dispatch_times[time_sum+variance])
                for i in dispatch_times[time_sum+variance]:
                    closest_dispatches.append(i)
                    time = ""
                    if(int((time_sum+variance)/3600) < 10):
                        time += "0"+str(int((time_sum+variance)/3600))
                    else:
                        time += str(int((time_sum+variance)/3600))
                    time += ":"
                    if(int(((time_sum+variance)%3600)/60) < 10):
                        time += "0"+str(int(((time_sum+variance)%3600)/60))
                    else:
                        time += str(int(((time_sum+variance)%3600)/60))
                    time += ":"
                    if(((time_sum+variance)%60) < 10):
                        time += "0"+str((time_sum+variance)%60)
                    else:
                        time += str((time_sum+variance)%60)
                    times.append(time)
                    
        except:
            pass
        try:
            if(len(dispatch_times[time_sum-variance]) > 0):
                count += len(dispatch_times[time_sum-variance])
                for i in dispatch_times[time_sum-variance]:
                    closest_dispatches.append(i)
                    time = ""
                    if(int((time_sum-variance)/3600) < 10):
                        time += "0"+str(int((time_sum-variance)/3600))
                    else:
                        time += str(int((time_sum-variance)/3600))
                    time += ":"
                    if(int(((time_sum-variance)%3600)/60) < 10):
                        time += "0"+str(int(((time_sum-variance)%3600)/60))
                    else:
                        time += str(int(((time_sum-variance)%3600)/60))
                    time += ":"
                    if(((time_sum-variance)%60) < 10):
                        time += "0"+str((time_sum-variance)%60)
                    else:
                        time += str((time_sum-variance)%60)
                    times.append(time)
                    
        except:
            pass
        variance += 1
        if(variance > 3600*24):
            print("NOT FOUND")
            return False, False
    
    return closest_dispatches, times

def get_most_dispatched_to():
    file = open("C:\Python34\sfpd-dispatch\sfpd-dispatch\sfpd_dispatch_data_subset.csv", 'r')
    categories = file.readline()
    location_frequencies={}
    line = "a"
    while(line):
        line = file.readline()
        if(line != ""):
            line=line.split(",")
            if(line[15] in location_frequencies.keys()):
                if(line[3] in location_frequencies[line[15]].keys()):
                    location_frequencies[line[15]][line[3]] += 1
                    location_frequencies[line[15]]["total"] += 1
                else:
                    location_frequencies[line[15]][line[3]] = 1
                    location_frequencies[line[15]]["total"] +=1
            else:
                location_frequencies[line[15]] = {}
                location_frequencies[line[15]][line[3]] = 1
                location_frequencies[line[15]]["total"] = 1
    file.close()
    return location_frequencies

def types_of_dispatches():
    file = open("C:\Python34\sfpd-dispatch\sfpd-dispatch\sfpd_dispatch_data_subset.csv", 'r')
    categories = file.readline()
    location_frequencies={}
    dispatch_type_total = {}
    call_hours_total = {}
    line = "a"
    while(line):
        line = file.readline()
        if(line != ""):
            line=line.split(",")
            #for getting the locations that are dispatched to the most
            if(line[15] in location_frequencies.keys()):
                if(line[3] in location_frequencies[line[15]].keys()):
                    location_frequencies[line[15]][line[3]] += 1
                    location_frequencies[line[15]]["total"] += 1
                else:
                    location_frequencies[line[15]][line[3]] = 1
            else:
                location_frequencies[line[15]] = {}
                location_frequencies[line[15]][line[3]] = 1
                location_frequencies[line[15]]["total"] = 1

            #for getting total values for different types of dispatches
            if(line[3] in dispatch_type_total.keys()):
                dispatch_type_total[line[3]] += 1
            else:
                dispatch_type_total[line[3]] = 1

            #for getting total values for calls made at different hours of the day
            date = line[8]
            if(int(date[11:13]) in call_hours_total.keys()):
                call_hours_total[int(date[11:13])] += 1
            else:
                call_hours_total[int(date[11:13])] = 1
    file.close()
    return location_frequencies, dispatch_type_total, call_hours_total

def maximum_location_frequencies():
    location_frequencies = get_most_dispatched_to()
    maximum_list = [-9,-8,-7,-6,-5,-4,-3,-2,-1,0]
    maximum_record = ["", "", "", "", "", "", "", "", "", ""]

    count = 0
    for i in location_frequencies.keys():
        for j in range(0,10):
            if(location_frequencies[i]["total"] > maximum_list[j]):
                if(j == 9):
                    maximum_list[j] = location_frequencies[i]["total"]
                    maximum_record[j] = i
                    break
            else:
                if(j == 0):
                    break
                if(j >= 1):
                    maximum_list[j-1] = location_frequencies[i]["total"]
                    maximum_record[j-1] = i
                    break

def longest_dispatch_time():
    file = open("C:\Python34\sfpd-dispatch\sfpd-dispatch\sfpd_dispatch_data_subset.csv", 'r')
    categories = file.readline()
    maximum_time_taken = [-9,-8,-7,-6,-5,-4,-3,-2,-1,0]
    record_line = ["","","","","","","","","",""]
    average_time_taken = {}
    average_time_taken = {}
    line = "a"
    while(line):
        line = file.readline()
        if(line != ""):
            try:
                #computing the maximum times that were taken
                line=line.split(",")
                date = line[10]
                time_sum1 = int(date[8:10])*3600*24+int(date[11:13])*3600+int(date[14:16])*60+int(date[17:19])
                date = line[8]
                time_sum2 = int(date[8:10])*3600*24+int(date[11:13])*3600+int(date[14:16])*60+int(date[17:19])
                for i in range(0,10):
                    if((time_sum1 - time_sum2) < maximum_time_taken[i]):
                        if(i == 0):
                            break
                        else:
                            maximum_time_taken[i-1] = time_sum1 - time_sum2
                            record_line[i-1] = line
                            break
                    if(((time_sum1 - time_sum2) > maximum_time_taken[i]) and i == 9):
                        maximum_time_taken[i] = time_sum1 - time_sum2
                        record_line[i] = line
                        break
            except:
                pass
                
            #computing the maximum average times taken
            average_time_taken_keys = average_time_taken.keys()
            if(line[15] in average_time_taken_keys):
                average_time_taken[line[15]].append(time_sum1 - time_sum2)
            else:
                average_time_taken[line[15]] = [time_sum1 - time_sum2]
    for i in average_time_taken.keys():
        sum_of_times = 0
        count = 0
        for j in average_time_taken[i]:
            sum_of_times += j
            count += 1
        if(count >= 5):
            average_time_taken[i] = float(sum_of_times) / count
        else:
            average_time_taken[i] = 0
    file.close()
    return maximum_time_taken, record_line, average_time_taken

def average_dispatch_times():
    maximum_time_taken, record_line, average_time_taken = longest_dispatch_time()
    longest_average_times = [-9,-8,-7,-6,-5,-4,-3,-2,-1,0]
    average_places = ["","","","","","","","","",""]
    record_average_lines = ["","","","","","","","","",""]
    for i in average_time_taken.keys():
        for j in range(0,10):
            if(average_time_taken[i] > longest_average_times[j]):
                if(j == 9):
                    longest_average_times[j] = average_time_taken[i]
                    average_places[j] = i
                    break
            else:
                if(j == 0):
                    break
                else:
                    longest_average_times[j-1] = average_time_taken[i]
                    average_places[j-1] = i
                    break
    #print("AVERAGES")
    #for i in range(0,10):
        #print(average_places[i], longest_average_times[i])

    #print("MAXIMUMS")
    #for i in range(0,10):
        #print(maximum_time_taken[i], record_line[i])
        #print("--------------")
def safest_neighborhoods():
    file = open("C:\Python34\sfpd-dispatch\sfpd-dispatch\sfpd_dispatch_data_subset.csv", 'r')
    categories = file.readline()
    zipcode_dangerous_totals = {}
    line = "a"
    while(line):
        line = file.readline()
        if(line != ""):
            line=line.split(",")
            if(line[25] == "Potentially Life-Threatening"):
                if(line[17] in zipcode_dangerous_totals.keys()):
                    zipcode_dangerous_totals[line[17]]+= 1
                else:
                    zipcode_dangerous_totals[line[17]] = 1
    file.close()
    return zipcode_dangerous_totals

def list_of_addresses():
    file = open("C:\Python34\sfpd-dispatch\sfpd-dispatch\sfpd_dispatch_data_subset.csv", 'r')
    categories = file.readline()
    addresses = []
    line = "a"
    while(line):
        line = file.readline()
        if(line != ""):
            line=line.split(",")
            if(line[15] not in addresses):
                addresses.append(line[15])
    file.close()
    return addresses

def create_file_of_addresses():
    output = open("addresses.txt", "w")
    output.write("\tvar valid_addresses = [\n")
    for i in list_of_addresses():
        output.write("\t\t\"" + i +"\",\n")
    output.write("];")
    output.close()    

#SECTION 2 -- FLASK WEB APP
app = Flask(__name__)

@app.route("/")
def start():
    return render_template('index.html')

@app.route("/dataoverview/")
def dataoverview():
    return render_template('dataoverview.html')

@app.route("/dispatch_predictor/")
def dispatch_predictor():
    return render_template('dispatch_predictor.html')

@app.route("/dispatch_predictor/submit/", methods=['POST'])
def dispatch_generator():
    most_frequent_dispatch = ""
    mode = 0
    address = request.form['address']
    time = request.form['time']
    dispatch_times = get_dispatch_times(address)
    
    try:
        dispatches,times = get_most_likely_dispatch(dispatch_times,int(time[0:2]),int(time[3:5]),int(time[6:8]))
    except:
        return render_template('error.html')
    
    if(dispatches != False):
        for i in dispatches:
            if(dispatches.count(i) > mode):
                mode = dispatches.count(i)
                most_frequent_dispatch = i
        return render_template('dispatch_generated.html', dispatch1=dispatches[0] + " at " + times[0], dispatch2=dispatches[1]+ " at " + times[1], dispatch3=dispatches[2] + " at " + times[2], dispatch4=dispatches[3] + " at " + times[3], dispatch5=dispatches[4] + " at " + times[4], address = address, time= time, most_frequent_dispatch = most_frequent_dispatch, number_of_dispatches = len(dispatches))
    else:
        return render_template('insufficient_dispatch_data.html')

@app.route("/dispatch_timing/")
def dispatch_timing():
    return render_template('dispatch_timing.html')

@app.route("/zipcodes/")
def safety_of_zipcodes():
    return render_template('safety_of_zipcodes.html')

#dispatch_times = get_dispatch_times("PINE ST/POLK ST")
#print(get_most_likely_dispatch(dispatch_times,5,5,5))
#maximum_location_frequencies()
#location_frequencies, dispatch_type_total, call_hours_total = types_of_dispatches()
#print(dispatch_type_total)
#print(call_hours_total)
if __name__ == "__main__":
    app.run()
