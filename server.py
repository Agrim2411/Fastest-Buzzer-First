NUM_CLIENTS = 3
WIN_SCORE = 5
SERVER_PORT = 5555
import sys
import select
import socket
import time


#TCP socket Set up
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = SERVER_PORT
s.bind(('',port)) # binding the socket 
s.listen(NUM_CLIENTS) #No. of connections = No. of clients

clients = [0]*NUM_CLIENTS #Participations

for i in range(NUM_CLIENTS): 
    clients[i], addr = s.accept()
    clients[i].send(str(i)) # Sending clients playernumber
    print "Connection to client",i+1,"has been set up.Everything's going well."

time.sleep(0.001) 
tally = [0]*NUM_CLIENTS #tally = scoreboard
time.sleep
n_ques=0 # current question Number
while (n_ques<50) : #game loop 
    time.sleep(0.001)
    buzzed = -1 # playernumber of client who hits buzzer
    n_ques=n_ques+1
    question ="\nQ."+str(n_ques) + ": " + str(1)+" + "+str(n_ques) 
    print(question)
    print("\n")
    #trueAnswerStr = raw_input("Answer: ")
    trueAnswerStr = str(n_ques+1) 
    trueAnswer = (trueAnswerStr.lower()).split()#splits into an array of lowercase constituent words

    for s in clients:
        s.send(question) # sending clients question 
    for s in clients:
        s.setblocking(0)
    #buzzer listening mechanism
        #The challenge here is to simultaneously listen to three sources. Select takes a list of sources and combines them into one source. In windows, sources can only be sockets, while stdin can also be a source in Unix-based systems.
    r, w, x = select.select(clients,[],[],10)# r == the sources select monitors for reading into, w, x irrelevant for us
    if(r): # Listening from clients for buzzer for 10 second. 
        s = r[0]
        buzzed = s.recv(1024)#when buzzing, the clients send their playernumber
        #if buzzed :
        #   pass 
    else:
        buzzed = "NB" # NB = No Buzzer     
          
    if(buzzed =="NB"):
        print"No one buzzed"
        for i in range(NUM_CLIENTS):
           s=clients[i] # telling all clients that buzzer timed out
           s.send("Buzzer Timed Out ! No One Buzzed\n")
    else: # buzzer was pressed
        buzzed = int(buzzed)
        print "Player "+ str(buzzed) + " Buzzed."
        for i in range(NUM_CLIENTS):#tell the other clients who buzzed
          s = clients[i]
          if i != buzzed :
              s.send("Player "+ str(buzzed) + " Buzzed.")
          else:
              s.send("You Buzzed.")

    for s in clients:
        s.setblocking(1) #return the sockets to a sequential processing mode
    time.sleep(0.1)
    if(buzzed!="NB"): 
        givenAnswer = (clients[buzzed]).recv(1024)
        if(givenAnswer!="NAR"):
           print("\nGiven Answer   : "+str(givenAnswer))
           print("Correct Answer : "+trueAnswerStr)
        else:
           print "\nNo Answer Recieved!"
    else :
        givenAnswer="---" # No one Buzzed
    
    if(buzzed=="NB"):
        for i in range(NUM_CLIENTS):#tell the other clients the answer given by the active player
              clients[i].send(givenAnswer)
    else:
        for i in range(NUM_CLIENTS):
            if(i!=buzzed):
               clients[i].send(givenAnswer)

    time.sleep(0.01)
    if(givenAnswer!="NAR" and givenAnswer!="---"): # checking for correctness of the givenAnswer
        givenAnswer = (givenAnswer.lower()).split()
        answeredCorrectly = True
        #print trueAnswer, givenAnswer
        for i in trueAnswer :#if every word in the answer is in the given, correct. Else incorrect
            if not (i in givenAnswer):
                answeredCorrectly = False
                break
        #Sending Remarks for the givenAnswer    
        if answeredCorrectly:
            print "\nAnswered Correctly."
            for s in clients:
                s.send("Correct!\n")
            tally[buzzed] +=1 # changing scores 
        else :
            print "\nAnswered Incorrectly."
            for s in clients:
                s.send("Incorrect!\n")
            tally[buzzed] -=0.5 # changing scores    
    elif(givenAnswer=="NAR") :
        for s in clients:
            s.send("\nNo Answer Received !\n")
    else:
        for s in clients:
            s.send("No One Buzzed !\n")    
         
    tallyStr = '' #convert the tally array into a str to send across to the clients
    time.sleep(0.01)
    for i in tally:
        tallyStr += ' ' + str(i)

    for s in clients: # sending score to the clients
        #if(buzzed!="NB"):
        s.send(trueAnswerStr)
        time.sleep(0.01)
        s.send(tallyStr)

    time.sleep(0.01)
    
    if(WIN_SCORE in tally or n_ques==50):#if any player has hit WIN_SCORE or all questions are done ,then tell the players to stop the game, else, tell them to continue
        for s in clients:
            s.send("0")
    else :
        for s in clients:
            s.send("1")
time.sleep(0.01)
tallyStr = '' #convert the tally array into a str to send across to the clients
for i in tally:
        tallyStr += ' ' + str(i)
for s in clients: # sending final scores 
        time.sleep(0.01)
        s.send(tallyStr)
time.sleep(0.01)

if WIN_SCORE not in tally : # Win /Lose/ All Lose
    for i in range(NUM_CLIENTS):
        clients[i].send("\nYou Lose! All Questions Done! No One Wins!")
else:         
    for i in range(NUM_CLIENTS):
       if tally[i] == WIN_SCORE :
        clients[i].send("You Won!")
       else :   
        clients[i].send("You Lose!")    