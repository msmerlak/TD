import numpy as np
import matplotlib.pyplot as plt

#-------------------------------------------
#-------------------------------------------
#-----------------FUNCTIONS-----------------
#-------------------------------------------
#-------------------------------------------


#-------------------------------------------
#TRAVELER'S DILEMMA PAYOFF SCHEME
#-------------------------------------------
#Defines the payoff of the player taking into account its own claim,
    # the other player's claim and the reward
#Param: cI player i's claim
#Param: cJ player j's claim
#Param: R reward/punishment in the payoff scheme
#Return: pay_pI payoff of player i
def payoff(cI, cJ, R):
    #Dummy Variable
    pay_pI=-1

    #If I get higher claim,
        #I get other's claim - R
    if cI > cJ:
        pay_pI = cJ-R

    #If I get lower claim,
        #I get my claim + R
    elif cI < cJ:
        pay_pI = cI+R

    #If claims are equal,
        #I get my claim
    elif cI == cJ:
        pay_pI = cI

    return pay_pI

#-------------------------------------------
#INSTROSPECTION PROCESS
#-------------------------------------------
#Generates the whole introspection process for one player: it generates a
    # new random alternative strategy, calculates payoffs, compares payoffs using the
    # Fermi function to obtain the probability of adoption and finally evaluates if
    # the new random strategy is adopted or not
#Param: cI realized strategy of player i
#Param: cJ realized strategy of player j
#Param: R reward/punishment in the payoff scheme
#Param: B selection intensity coefficient
#Return: cI new realized strategy of player i
# (strategy adopted after instrospection process)
def introspection(cI,cJ,R,B):

    #Strategy space interval definition [L,U]
    #Lower bound
    L = 2.0
    #Upper bound
    U = 100.0

    #Random alternative strategy claim
    #The strategy is rounded to the next integer
    c_rand = round(np.random.uniform(L,U))

    #Payoff of player i's realized claim
    Pay_I =payoff(cI,cJ,R)

    #Payoff of random alternative claim
    Pay_rand =payoff(c_rand,cJ,R)

    #Probability of adoption of random alternative claim
    #Fermi function
    Delta_Payoff = Pay_rand-Pay_I
    deno = 1 + np.exp(-B*Delta_Payoff)
    P_adop =1/deno

    #Generate random number to evaluate the probability of adoption
    Q = np.random.random()

    #If Q falls below the probability of adoption threshold
        # then the random alternative strategy is adopted
    if Q<P_adop:
        #random one adopted
        cI = c_rand
    #else:
        #Current one kept

    return cI

#-------------------------------------------
#EXECUTE THE SIMULATION
#-------------------------------------------
#Execute the simulation for a given number of timesteps,
    # for each time step both players carry out the introspection process, first
    # player i and then player j
#Param: ini_I initial claim for player i
#Param: ini_J initial claim for player j
#Param: R reward/punishment in the payoff scheme
#Param: B selection intensity coefficient
#Param: t number of timesteps for the simulation
#Return: EvoI, EvoJ numpy arrays with the information of the claims for player i
# and j for the whole simulation
def exe(ini_I,ini_J,R,B,t):

    #Initialize the evolution arrays with the initial conditions
    EvoI = np.array([ini_I])
    EvoJ = np.array([ini_J])

    #Perform the introspection process for the players
    player_i = introspection(ini_I,ini_J,R,B)
    other_player = introspection(ini_J,ini_I,R,B)

    #Append step information to the evolution arrays
    EvoI = np.append(EvoI,player_i)
    EvoJ = np.append(EvoJ,other_player)

    ini_I=player_i
    ini_J=other_player

    #Perform the process for t-1 timesteps
    # t-1 because the initialization already took 1 timestep
    for i in range(t-1):

        #Perform the introspection process for the players
        player_i = introspection(ini_I,ini_J,R,B)
        other_player = introspection(ini_J,ini_I,R,B)

        #Append step information to the evolution arrays
        EvoI = np.append(EvoI,player_i)
        EvoJ = np.append(EvoJ,other_player)

        ini_I=player_i
        ini_J=other_player

    return EvoI, EvoJ

#-------------------------------------------
#GRAPH THE SIMULATION
#-------------------------------------------
#Graph the simulation
#Param: EvoI evolution array player i
#Param: EvoJ evolution array player J
#Return: File with graph
def graph(EvoI, EvoJ):

    #Plot the evolution arrays (Player 1 and 2)
    plt.plot(EvoI, color ="blue")
    plt.plot(EvoJ, color ="orange")

    #Calculate average claim for each player
    #Avg1=round(np.average(EvoI[100:]),3)
    #Avg2=round(np.average(EvoJ[100:]),3)
    #Plot the averages
    #plt.axhline(y=Avg1, color ="blue",linestyle="--", label=str(Avg1))
    #plt.axhline(y=Avg2, color ="orange",linestyle="--", label=str(Avg2))

    #Textbox with info about B
    textstr = r"$\beta =$" + str(B)
    props = dict(boxstyle='round', facecolor='lightgray', alpha=0.5)
    plt.text(4550, 110, textstr, fontsize=12,
        verticalalignment='top', bbox=props)

    #Aesthetics of the graph
    #plt.title("Claim evolution for the Traveler's Dilemma")
    plt.xlabel("Time Steps", fontsize = 13)
    plt.ylabel("Claim Value", fontsize = 13)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    #plt.legend(loc=7)
    plt.ylim((-3,103))
    plt.savefig("Pre_Results_2.png")
    plt.clf()

#-------------------------------------------
#-------------------------------------------
#-----------RUN THE SIMULATION--------------
#-------------------------------------------
#-------------------------------------------


#-------------------------------------------
#PARAMETERS FOR THE SIMULATION
#-------------------------------------------

#Claims should be in the interval [L,U]
#Initial claim player 1
ini_I = 2
#Initial claim player 2
ini_J = 2
#Reward/punishment in the payoff scheme
R = 2
#Selection intensity coefficient
B = 1.0
#Timesteps
t = 5000
#t=10

#-------------------------------------------
#RUN THE SIMULATION
#-------------------------------------------
EvoI, EvoJ = exe(ini_I,ini_J,R,B,t)
graph(EvoI, EvoJ)

#-------------------------------------------

#Message useful to quickly examine output of simulation
print("------------")
print(EvoI)
print(EvoJ)
print("------------")
print(np.std(EvoI))
print(np.std(EvoJ))
print(np.average(EvoI))
print(np.average(EvoJ))
print(np.median(EvoI))
print(np.median(EvoJ))
