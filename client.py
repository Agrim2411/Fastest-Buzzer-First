SERVER_IP = ''  
SERVER_PORT = 5555
import select
import threading
import sys
import random
import socket
import termios
import time
try: 
    
    def receiveMsg(s,killRequest):# s-socket # killRequest-threading #inter-thread communication.
        while not killRequest.isSet(): #waiting for user
            r, w, x = select.select([s], [], []) 
            data = r[0].recv(1024)
            if data :
              killRequest.set()
            print data
            

    def sendMsg(s, userid, killRequest, youBuzzed) :
        global m
        start_time=time.time()
        while not killRequest.isSet(): #Set to hit the buzzer.
            #r, w, x = select.select([sys.stdin], [], [],10)# r- sources to monitor Timeout- 0.02 sec
            #if r:#if any source gives readable data            
            r, w, x = select.select([sys.stdin], [], [],0.02)
            if r:
                s.send(str(userid))
                youBuzzed.set()
                time.sleep(0.01)
                break

    serverip = SERVER_IP
    serverport = SERVER_PORT
    clientport = random.randint(2000,3000) #chossing random client port number

    #socket set up- assigning of userid
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#make the socket reusable.
    s.bind(('',clientport)) # binding portnumber and IP
    s.connect((serverip, serverport)) # establishing connection
    userid = s.recv(1024) #userid = Player Number-1
    print "Hello gamer. Wish you luck.\nYou are player number : " + str(int(userid)+1)
    win_score = 5
    print("Rules :\n1> Press buzzer first(within 10 seconds) to answer.\n\n2> +1 for a correct answer.\n   -0.5 for wrong answer.\n    0 for NOT answering after pressing the buzzer.\n\n3> Points to win = 5\n\n4> Total questions = 50")

    #game loop
    continue_next_round = "1" 
    while continue_next_round!="0" :

        question = s.recv(1024)
        killRequest = threading.Event()
        youBuzzed = threading.Event()
        sendThread = threading.Thread(target = sendMsg, args = [s, userid, killRequest, youBuzzed]) #thread to hit the buzzer
        receiveThread = threading.Thread(target = receiveMsg, args = [s, killRequest]) #thread to hear if anyone else has hit buzzer

        time.sleep(0.1)
        print("\n"+str(question))
        print("Press Buzzer(ENTER) Within 10 Seconds To Answer\n>>>"),
        s.setblocking(0)#setblocking(0)- To set  all the socket methods non-blocking.
        sendThread.start()
        receiveThread.start()
        receiveThread.join()# Multithreading- Simultaneously waiting  
        sendThread.join()#to recieve and send . 
        s.setblocking(1)#return the sockets to a sequential processing mode
        termios.tcflush(sys.stdin, termios.TCIOFLUSH) # flushing stdin
        time.sleep(0.01)
        if youBuzzed.isSet() :
            print("Answer The Question Within 10 Seconds\n>>>"),
            i, o, e = select.select( [sys.stdin], [], [],10)
            if (i):# 10 second time for answering after buzzing. 
                givenAnswer = str(sys.stdin.readline().strip())
            
            else : # after waiting for 10 second for answer from user.
                print "\nTIME OUT"
                givenAnswer="NAR"#send to server "No Answer Recieved"
            s.send(givenAnswer)
        else : # Recieving given answer .
                givenAnswer = s.recv(1024)
                if(givenAnswer!="NAR" and givenAnswer!="---"):
                   print "\nGiven Answer  : ", givenAnswer
 
        is_correct_str = s.recv(1024)#recieving CORRECT/INCORRECT/No Answer Recieved/No one buzzed
        time.sleep(0.01)
        if(is_correct_str!="No One Buzzed !"):
           print(is_correct_str)
        trueAnswer = s.recv(1024) #Receiving Correct Answer 
        print "Correct Answer  : ",trueAnswer  
        time.sleep(0.01)
        tally = s.recv(1024) # Receiving Score
        tally = tally.split()#scoreboard split
        
        print("\nCurrent Score > ")
        print("_______________")
        for i in range(len(tally)):
            if(i==int(userid)) :
              print "|      You"+" : "+str(tally[i])
            else:
              print "| Player "+str(i+1)+" : "+str(tally[i])
        print("|______________")            
        continue_next_round = s.recv(1024)
    
    tally = s.recv(1024) # Receive Final Score
    tally = tally.split()#scoreboard split
    time.sleep(0.01)
    print "\nFinal Score >"
    print("_____________")
    for i in range(len(tally)):
        if(i==int(userid)) : 
            print "     You"+" : "+str(tally[i])
        else:
            print "Player "+str(i+1)+" : "+str(tally[i])    
    print("_____________")
    final_message = s.recv(1024) # Receiving Won/lose/All lose
    print("\n")
    print final_message
except Exception as e:
    print e #error message
finally: #At the end close the socket properly.
    s.close()
