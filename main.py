# -*- coding: utf-8 -*-
import json

raw_json = input("Введите значение json: ")
JSON = json.loads(raw_json.replace("\\", '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace("\\\"","»"))
for task in JSON:
	answer_type = task["answer"]["type"]
	if answer_type == "answer/single":
		right_answer = task['answer']['right_answer']['id']
		for answer_variant in task['answer']['options']:
			if answer_variant['id'] == right_answer:
				if answer_variant['text'] != "":
						task_correct_answer = answer_variant['text']
				else:
					for array in answer_variant['content']:
						if array['type'] == 'content/math':
							task_correct_answer = array['content']
						elif array['type'] == 'content/file':
							task_correct_answer = "https://uchebnik.mos.ru/exam" + array['file']['relative_url']
				print("Задание " + str(task['taskNum']) + ") " + str(task_correct_answer))
	elif answer_type == "answer/multiple":
		right_answer = task['answer']['right_answer']['ids']
		for answer_variant in task['answer']['options']:
			if answer_variant['id'] in right_answer:
				print("Задание " + str(task['taskNum']) + ") " + str(answer_variant['text']))
	elif answer_type in ["answer/match",'answer/match/timeline']:
		right_answer = task['answer']['right_answer']['match']
		for id in right_answer:
			task_content = ""
			task_correct_answer = ""
			for answer_variant in task['answer']['options']:
				if answer_variant['id'] == id:
					if answer_variant['text'] != "":
						task_content = answer_variant['text']
					else:
						for array in answer_variant['content']:
							task_content = array['content']
				elif answer_variant['id'] == right_answer[id][0]:
					if answer_variant['text'] != "":
						task_correct_answer = answer_variant['text']
					else:
						for array in answer_variant['content']:
							task_correct_answer = array['content']
			print("Задание " + str(task['taskNum']) + ") " + str(task_content) + " - " + str(task_correct_answer))
	elif answer_type == "answer/number":
		right_answer = task['answer']['right_answer']['number']
		print("Задание " + str(task['taskNum']) + ") " + str(right_answer))
	elif answer_type == "answer/string":
		right_answer = task['answer']['right_answer']['string']
		print("Задание " + str(task['taskNum']) + ") " + str(right_answer))
	elif answer_type == "answer/table":
		right_answer = task['answer']['right_answer']['cells']
		for row in right_answer:
			for collum in right_answer[row]:
				print("Задание " + str(task['taskNum']) + ") " + str(int(collum) + 1) + "-й столбец " + str(row) + "-ая строчка - " + str(right_answer[row][collum]))
	elif answer_type == "answer/groups":
		right_answer_groups = task['answer']['right_answer']['groups']
		for group in right_answer_groups:
			task_content = ""
			task_correct_answer = []
			for answer_variant in task['answer']['options']:
				if answer_variant['id'] == group['group_id']:
					if answer_variant['text'] != "":
						task_content = answer_variant['text']
					else:
						for array in answer_variant['content']:
							task_content = array['content']
				elif answer_variant['id'] in group['options_ids']:
					if answer_variant['text'] != "":
						task_correct_answer.append(answer_variant['text'])
					else:
						for array in answer_variant['content']:
							task_correct_answer.append(['content'])
			print("Задание " + str(task['taskNum']) + ") " + str(task_content) + " - " + str(",".join(task_correct_answer)))
