from othellogame import *
import sys

def main():
    print(" 1.HumanPlayer\n 2.RandomPlayer\n 3.MiniMaxPlayer\n 4.MiniMax-AlphaBeta-Player\n")
    P1 = input("Please Choose P1(BLACK):")
    print("")
    P2 = input("Please Choose P2(WHITE):")
    print("")
    P1_deep,P2_deep = 0,0
    if P1 == "3" or P1 == "4":
        P1_deep = input("Please Choose P1's depth:")
        print("")
    if P2 == "3" or P2 == "4":
        P2_deep = input("Please Choose P2's depth:")
        print("")
    if P1_deep=="":
        P1_deep=2
    if P2_deep=="":
        P2_deep=2
    rounds = input("How many rounds? :")
    print("")
    t,f,tie = 0,0,0
    for i in range(0,int(rounds)):
        c = play_game(P1,P2,int(P1_deep),int(P2_deep))
        if c == True:
            t+=1
        elif c == False:
            f+=1
        else:
            tie+=1
    print("BALCK WINS is : "+str(f))
    print("WHITE WINS is : "+str(t))
    print("Tie is : "+str(tie))
    #ab_minimax_game(None,None,2)

if __name__ == '__main__':
    main()