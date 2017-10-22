from flask import Flask, render_template, make_response, request, session
from datetime import datetime
import random as rand
import glob


app = Flask(__name__)


@app.before_request
def before_request():
	global QUESTION_INFO
	QUESTION_INFO = getQuestionInfo()

@app.route('/question')
def index():
	question = makeQuestion() 
	statusFile = readStatus()
	numQuestion = int(statusFile[0]) + 1
	return render_template('question.html', select=question, numQuestion=numQuestion, answerPic=ANSWER_PIC)

@app.route('/result', methods = ['POST', 'GET'])
def setcookie():
	if request.method == 'POST':
		statusFile = readStatus()
		numCorrect = int(statusFile[1])
		numQuestion = int(statusFile[0])
		numQuestion += 1
		userAns = request.form['select']
		result = ""
		if(numQuestion < 5):
			if userAns == ANSWER:
				numCorrect += 1
				result = "Correct!"
				resp = make_response(render_template('normal_correct.html', userAns=userAns, result=result, numQuestion=numQuestion, numCorrect=numCorrect*20, answerPic=ANSWER_PIC))

			else:
				result = "Incorrect!"
				resp = make_response(render_template('normal_incorrect.html', userAns=userAns, result=result, numQuestion=numQuestion, numCorrect=numCorrect*20, correctAns=ANSWER, answerPic=ANSWER_PIC))

			writeStatus(ANSWER, numCorrect, numQuestion)

		else:	#when final question
			if userAns == ANSWER:
				numCorrect += 1
				result = "Correct!"
				resp = make_response(render_template('final_correct.html', userAns=userAns, result=result, numQuestion=numQuestion, numCorrect=numCorrect*20, answerPic=ANSWER_PIC))

			else:
				result = "Incorrect!"
				resp = make_response(render_template('final_incorrect.html', userAns=userAns, result=result, numQuestion=numQuestion, numCorrect=numCorrect*20, correctAns=ANSWER, answerPic=ANSWER_PIC))

			initializeStatus()

	return resp


def getQuestionInfo():
	infoPath = glob.glob('static/img/*')
	questionInfo = []
	for line in infoPath:
		path = line.replace("static/img\\", "")
		animal = path.replace(".jpg", "")
		animal = animal.replace("_", " ")
		info = [animal, path]
		questionInfo.append(info)
	return questionInfo

def makeQuestion():
	questionInfo = QUESTION_INFO
	questNumbers = [[],[]]
	for i in range(4):
		num = rand.randint(1, len(questionInfo))
		if(i == 0):
			global ANSWER
			global ANSWER_PIC
			ANSWER = questionInfo[num-1][0]
			ANSWER_PIC = questionInfo[num-1][1]
			questNumbers[0].append(questionInfo[num-1][1])
			questNumbers[1].append(questionInfo[num-1][0])
		else:
			questNumbers[1].append(questionInfo[num-1][0])
		del questionInfo[num-1]

	rand.shuffle(questNumbers[1])
	return questNumbers

def readStatus():
	f = open('static/status/status.txt', 'r')
	fileInfo = []
	for line in f:
		fileInfo.append(line)
	f.close()
	return fileInfo

# def removeUsedQuestion():
# 	for i in range(len(QUESTION_INFO)):
# 		if ANSWER in QUESTION_INFO[i]:
# 			del QUESTION_INFO[i][0]
# 			del QUESTION_INFO[i][1]


def writeStatus(ANSWER, numCorrect, numQuestion):
	currentStatus = readStatus()
	currentStatus[0] = numQuestion
	currentStatus[1] = numCorrect
	currentStatus.append(ANSWER)

	f = open('static/status/status.txt', 'w')
	for line in currentStatus:
		f.write(str(line) + '\n')
	f.close()
	#removeUsedQuestion()
	ANSWER = ''
	ANSWER_PIC = ''

def initializeStatus():
	f = open('static/status/status.txt', 'w')
	initializedStatus = [0, 0]
	for line in initializedStatus:
		f.write(str(line) + '\n')
	f.close()
	QUESTION_INFO = getQuestionInfo()




## magic
if __name__ == "__main__":
    app.run(debug=True)