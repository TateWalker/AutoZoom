from crontab import CronTab
import json
from datetime import timedelta, time, date, datetime
import os

def main(classes):
    """
    Need to make sure this works on windows as well

    """
    cron  = CronTab(user=True)
    cron.remove_all(comment='autozoom')
    cron.write()

    cwd = os.getcwd()
    # print(len(classes))
    if classes == {}:
        return
    for i in classes.keys():
        url =classes[i]['link']
        days = classes[i]['days']
        days = [i for i, elem in enumerate(days) if (elem == 1)]
        
        start_time = classes[i]['start_time']
        end_time = classes[i]['end_time']
        s_t = timedelta(hours=start_time[0],minutes=start_time[1])
        e_t = timedelta(hours=end_time[0],minutes=end_time[1])
        class_length = (e_t-s_t)// timedelta(minutes=1)
        # print(class_length)
        # print(type(class_length))
        # print(cwd)
        # print(cwd)
        cron_instructions = 'cd {} && ./realZoom.sh {} {} >> {}/std.txt 2>&1'.format(cwd,url,class_length,cwd)
        # cron_instructions = 'cd {}/../macOS && ls && ./mainWrapper --args -{} -{} >> ~/Desktop/std.txt 2>&1'.format(cwd,url,class_length)
        job = cron.new(command=cron_instructions,comment = 'autozoom')
        job.hour.on(start_time[0])
        job.minute.on(start_time[1])
        for i in range(len(days)):
            job.dow.also.on(days[i])
        cron.write()

        #FOR THE FIRST CLASS, WE CAN SET THE PMSET, BUT FOR EVERY ONE AFTER THAT, WE NEED TO MAKE A CRON THAT CHANGES PMSET AT THE END OF EACH PROGRAM RUN
    possible_days = ['U','M','T','W','R','F','S']
    ordered_times = [None]*7

    def getInstruction(j,dow):
        if j[1]-5<0:
            if j[0]-1<0:
                temp_time = time(hour=j[0]+23,minute=j[1]+55)
                cron_instructions = 'pmset wakeorpoweron {} {}'.format(possible_days[dow-1],temp_time)
            else:
                temp_time = time(hour=j[0]-1,minute=j[1]+55)
                cron_instructions = 'pmset wakeorpoweron {} {}'.format(possible_days[dow],temp_time)

        else:
            temp_time= time(hour=j[0],minute=j[1]-5)
            cron_instructions = 'pmset wakeorpoweron {} {}'.format(possible_days[dow],temp_time)
        return cron_instructions

    for i in range(7): #incrementing through days to find class order
        times = []
        end_times = []
        for j in classes.keys():
            if classes[j]['days'][i] == 1:
                times.append(classes[j]['start_time'])
                end_times.append(classes[j]['end_time'])
        times = (sorted(times))
        ordered_times[i] = times
    # print(ordered_times)
            
    for i in range(0,len(ordered_times)): #goes through each day
        h=i #things are probably going to break if there isn't anything on sunday
        if not ordered_times[h]:
            continue
        # print(i)
        for k in range(len(ordered_times[i])): #goes through each day's times
            if k != len(ordered_times[i])-1:
                # print('day = {}'.format(i))
                # print('time = {}'.format(k))
                j = ordered_times[i][k+1]
            else:
                try:
                    while not ordered_times[h+1]:
                        if h+1 == len(ordered_times)-1:
                            h = -1
                        else:
                            h+=1
                    j = ordered_times[h+1][0]
                    h+=1
                except:
                    continue

            # print(getInstruction(j,h))
            job = cron.new(command=getInstruction(j,h),comment = 'autozoom')
            job.hour.on(ordered_times[i][k][0])
            job.minute.on(ordered_times[i][k][1])
            job.dow.on(i)
            cron.write()


    def nearest(items, pivot):

        return min(items, key=lambda x: (x - pivot))

    #write the closest one now

    def fixDate(wrong_day):
        wrong_day = wrong_day+1
        if wrong_day == 7:
            wrong_day = 0
        return wrong_day

    day_of_week = fixDate(date.today().weekday())
    # print('day of week = {}'.format(day_of_week))
    while not ordered_times[day_of_week]:
        if day_of_week == 6:
            day_of_week=-1
        day_of_week+=1
    items = ordered_times[day_of_week]
    # print(items)
    if day_of_week != fixDate(date.today().weekday()):
        next_time = items[0]
    else:
        cur_time = datetime.now().time()
        cur_time = [cur_time.hour,cur_time.minute]
        # print(cur_time)

        tmp_times = items+[cur_time]
        if tmp_times.index(cur_time) == len(tmp_times)-1:
            # print('last one')
            # print(day_of_week)
            if day_of_week == 6:
                    day_of_week=-1
            day_of_week+=1
            # print(day_of_week)
            while not ordered_times[day_of_week]:
                if day_of_week == 6:
                    day_of_week=-1
                day_of_week+=1
            # print(ordered_times[day_of_week])
            next_time = ordered_times[day_of_week][0]
        else:
            next_time = temp_times[temp_times.index(cur_time)+1]

    
    job = cron.new(command=getInstruction(next_time,day_of_week),comment = 'autozoom')
    # print(getInstruction(next_time,day_of_week))
    job.hour.on(datetime.now().time().hour)
    job.minute.on(datetime.now().time().minute)
    job.dow.on(fixDate(date.today().weekday()))
    cron.write()        

            #NEED TO REWRITE SO IT KEEPS RECORD OF ALL TIMES NOT JUST DAY BY DAY
            #THEN USE CURRENT LOGIC TO GET NEXT CLASS TIME AND SET PMSET
            #FIND CLOSEST CLASSTIME TO NOW AND GO AHEAD AND SET THAT PMSET

    
    # call(["pmset repeat wakeorpoweron {} {}".format(days_string,)])



if __name__ == '__main__':
    main()


    #FIGURE OUT WHY CWD GOES TO RESOURCES AND NOT TO MACOS BECAUSE YOU CANT RUN THE PROGRAM WHEN IN THE WRONG FOLDER