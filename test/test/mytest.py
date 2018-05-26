
import time
import threading

def T1_job():
    print("T1 start\n")
    for i in range(10):
        time.sleep(3)
    print("T1 finish\n")

def T2_job():
    print("T2 start\n")
    print("T2 finish\n")

thread_1 = threading.Thread(target=T1_job, name='T1')
thread_2 = threading.Thread(target=T2_job, name='T2')
thread_1.start() # 开启T1
thread_2.start() # 开启T2
print(threading.enumerate())
thread_2.join() # notice the difference!
thread_1.join() # notice the difference!
print(threading.enumerate())
print("all done\n")