# -*- coding: utf-8 -*-
import json

JSON = input("Введите значение json: ")
raw_json = json.loads(JSON.replace("\\", '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace("\\\"","»"))
for i in raw_json:
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
		for id in right_answer:
			task_content = ""
			task_correct_answer = ""
			for answer_variant in i['answer']['options']:
				if answer_variant['id'] == id:
					if answer_variant['text'] != "":
						task_content = answer_variant['text']
					else:
						for array in answer_variant['content']:
							task_content = array['content']
				if answer_variant['id'] == right_answer[id][0]:
					if answer_variant['text'] != "":
						task_correct_answer = answer_variant['text']
					else:
						for array in answer_variant['content']:
							task_correct_answer = array['content']
			print("Задание " + str(i['taskNum']) + ") " + str(task_content) + " - " + str(task_correct_answer))
	elif answer_type == "answer/number":
		right_answer = i['answer']['right_answer']['number']
		print("Задание " + str(i['taskNum']) + ") " + str(right_answer))
	elif answer_type == "answer/string":
		right_answer = i['answer']['right_answer']['string']
		print("Задание " + str(i['taskNum']) + ") " + str(right_answer))
