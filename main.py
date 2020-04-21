# -*- coding: utf-8 -*-
import json

JSON = input("Введите значение json: ")
raw_json = json.loads(JSON.replace("\\", '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace("\\\"","»"))
for i in raw_json:
	#print(i)
	answer_type = i["answer"]["type"]
	if answer_type == "answer/single":
		right_answer = i['answer']['right_answer']['id']
		for f in i['answer']['options']:
			if f['id'] == right_answer:
				print("Задание " + str(i['taskNum']) + ") " + str(f['text']))
				break
	elif answer_type == "answer/multiple":
		right_answer = i['answer']['right_answer']['ids']
		for f in i['answer']['options']:
			if f['id'] in right_answer:
				print("Задание " + str(i['taskNum']) + ") " + str(f['text']))
	elif answer_type == "answer/match":
		right_answer = i['answer']['right_answer']['match']
		print(right_answer)
	elif answer_type == "answer/number":
		right_answer = i['answer']['right_answer']['number']
		print("Задание " + str(i['taskNum']) + ") " + str(right_answer))
	elif answer_type == "answer/string":
		right_answer = i['answer']['right_answer']['string']
		print("Задание " + str(i['taskNum']) + ") " + str(right_answer))
		
