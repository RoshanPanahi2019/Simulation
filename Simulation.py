import simpy
import numpy as np
import matplotlib.pyplot as plt
import math
# Developed by Roshan Panahi # Panahir@OregonState.Edu
def jobprocess(env,Stations,job):   
    for j in range(Stations_Count):         
        with Stations[j].request() as request: 
            with Workers.request() as requestWorkers:
                a= (env.now)         
                yield request 
                yield requestWorkers
                b=(env.now) 
                waitTime=b-a
                StationWaitTime[j]=StationWaitTime[j]+waitTime
                yield env.timeout(Duration[j]) 
                Stations[j].release(request)
                Workers.release(requestWorkers)                
                data=monitor(j,job,math.trunc(waitTime),Duration[j],math.trunc(env.now))
    with open(file + 'schedule.txt', 'a') as filename:
        filename.write(' Station \n Job\n WaitTime\n Duration\n CurrentTime \n  %s'%(data)+ '\n')
        
def plotter(Stations_Count):
    for j in range(Stations_Count):
        plt.bar(j, StationWaitTime[j]/Maxepoch, align='center', alpha=1)
        plt.xlabel('Station')
        plt.ylabel('WaitTime(Hours)')
        plt.title('Mean Station Waiting Time for %d Jobs %d Stations  %d iterations %d Workers'%(Jobs_Count,Stations_Count,Maxepoch,Workers.capacity)) 
    plt.grid(True)        
    plt.show()
    
def monitor(Station,job,waitTime,Duration,now):
    item=(Station,
        job,
        waitTime,
        Duration,
        now,
        )
    data.append(item)
    return(data)   
    
def trian(min,mode,max):
    return np.random.triangular(min,mode,max)
    
def Duration_Generator():
    Duration=       ([trian(208,260,312),trian(72,90,108),trian(24,30,36),trian(80,100,120),trian(48,60,72),
                    trian(48,60,72),trian(48,60,72),trian(72,90,108),trian(72,90,108),trian(168,210,252),
                    trian(168,210,252),trian(168,210,252),trian(144,180,216),trian(168,210,252),
                    trian(240,300,360),trian(168,210,252),trian(144,180,216),trian(96,120,144),trian(96,120,144)])
                    
                    #(1 Floor Build),  ,2 Plumbing      ,3 Floor Prep Flooring ,5 P-Wall Set
                     # 6          ,7              ,9               , 10               ,11,
                     # 12           13,                      ,14                 ,15          
                     # 17               18,                 19                  20                  21`)
    return np.trunc(Duration)
    
if __name__=='__main__':
    file= 'C:/Users/Roshan/Box/Courses/Winter-2020/IE563/Project/TermProject/Simulation/'
    Maxepoch=30
    Jobs_Count=10
    Stations_Count=19
    StationWaitTime=np.zeros(Stations_Count)
    for epoch in range(Maxepoch):
        data=[]
        requestWorkers=[]    
        Stations=[]
        Duration=Duration_Generator()
        env=simpy.Environment()
        for i in range(Stations_Count):
            Stations.append(simpy.Resource(env,capacity=1))           
        Workers=(simpy.Resource(env,capacity=7))         
        for job in range(Jobs_Count):       
            env.process(jobprocess(env, Stations,job))
        env.run()         
    print(((StationWaitTime))) 
    StationWaitTime[0]=0
    plotter(Stations_Count)

    