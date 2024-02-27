import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import random


# Get Choice
def detectChoice(fingers):
    if (fingers == [0, 0, 0, 0, 0]):
        return "Rock"
    elif (fingers == [1, 1, 1, 1, 1]):
        return "Paper"
    elif (fingers == [0, 1, 1, 0, 0]):
        return "Scissors"
    else:
        return None


# Get computer's choice
def getComputerChoice():
    return random.choice(options)


# Update Score
def updateResult(hand, board):
    global humanChoice, computerChoice, humanScore, computerScore, updateScore, checkChoice

    if (humanChoice is None) and (checkChoice):
        fingersUp = detector.fingersUp(hand)
        humanChoice = detectChoice(fingersUp)
        if (humanChoice is None):
            checkChoice = False
            return board
    if (computerChoice is None) and (checkChoice):
        computerChoice = getComputerChoice()

    if (humanChoice is None and computerChoice is None):
        return board

    if (computerChoice == "Rock"):
        comImg = rockImg
        if (humanChoice == "Scissors") and (updateScore):
            computerScore += 1
            updateScore = False
        elif (humanChoice == "Paper") and (updateScore):
            humanScore += 1
            updateScore = False
    elif (computerChoice == "Paper"):
        comImg = paperImg
        if (humanChoice == "Scissors") and (updateScore):
            humanScore += 1
            updateScore = False
        elif (humanChoice == "Rock") and (updateScore):
            computerScore += 1
            updateScore = False
    elif (computerChoice == "Scissors"):
        comImg = scissorsImg
        if (humanChoice == "Paper") and (updateScore):
            computerScore += 1
            updateScore = False
        elif (humanChoice == "Rock") and (updateScore):
            humanScore += 1
            updateScore = False

    board[imgMarginY:imgMarginY+imgSize-1,
          imgMarginX:imgMarginX+imgSize-1] = comImg

    checkChoice = True
    return board


# Global & Const Variables
# Video Frame Width and Height
FrameWidth, FrameHeight = 680, 480
MarginTop = 50
WindowWidth, WindowHeight = 800, 400
FrameResize = (WindowWidth//2, WindowHeight)

# Initializing Hand Tracker
detector = HandDetector(maxHands=1, detectionCon=0.7)

# Board Image
whiteBoard = np.ones((WindowHeight, WindowWidth, 3), dtype=np.uint8) * 255

# Images
rockImg = cv2.imread("./assets/rock.png")
paperImg = cv2.imread("./assets/paper.png")
scissorsImg = cv2.imread("./assets/scissors.png")
imgSize = 250
imgMarginX = ((WindowWidth//2) - imgSize)//2
imgMarginY = (WindowHeight + MarginTop - imgSize)//2

# rock paper scissors options
options = ["Rock", "Paper", "Scissors"]

# Scores
computerScore = 0
humanScore = 0

# Video Capture
cap_vid = cv2.VideoCapture(1)
cap_vid.set(cv2.CAP_PROP_FRAME_WIDTH, FrameWidth)
cap_vid.set(cv2.CAP_PROP_FRAME_HEIGHT, FrameHeight)
windowName = "Rock Paper Scissors"

updateScore = True
checkChoice = True
humanChoice = None
computerChoice = None

print("\nGame ON!")
while cap_vid.isOpened():
    ret, img = cap_vid.read()
    if not ret:
        continue

    paddX = (img.shape[1] - (WindowWidth//2)) // 2
    paddY = (img.shape[0] - (WindowHeight-MarginTop)) // 2
    img = img[paddY:img.shape[0]-paddY, paddX:img.shape[1]-paddX]
    board = whiteBoard.copy()
    # print(board.shape)
    img = cv2.flip(img, cv2.CAP_PROP_XI_DECIMATION_HORIZONTAL)
    board[MarginTop:WindowHeight, WindowWidth//2:WindowWidth] = img

    hands, _ = detector.findHands(img, flipType=True, draw=False)

    if (hands):
        board = updateResult(hands[0], board)

        # checkChoice = False
    elif (not hands):
        updateScore = True
        checkChoice = True
        humanChoice = None
        computerChoice = None

    # Draw Text Place
    board = cv2.rectangle(
        board, (0, 0), (WindowWidth, MarginTop), (255, 0, 255), -1)
    # Write Score
    board = cv2.putText(board, "Computer: " + str(computerScore),
                        (20, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    board = cv2.putText(board, "You: " + str(humanScore), ((WindowWidth//2) +
                        20, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    # Draw middle line
    board = cv2.line(board, ((WindowWidth//2)-3, 0),
                     ((WindowWidth//2)-3, WindowHeight), (0, 255, 0), 5)

    if (humanChoice is not None and computerChoice is not None):
        board = cv2.putText(board, computerChoice,
                            ((WindowWidth//2)-120, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        board = cv2.putText(board, humanChoice,
                            ((WindowWidth)-120, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow(windowName, board)
    if (cv2.waitKey(1) & 0xFF == 27):
        break
    if (cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1):
        break


print("\nGame Ended with Score -> ")
print(f"Computer: {computerScore}    ||    You: {humanScore}\n")
print("You Won!" if humanScore >
      computerScore else "Computer Won!" if computerScore > humanScore else "It's a Tie!")
# Release Camera
cap_vid.release()
cv2.destroyAllWindows()
