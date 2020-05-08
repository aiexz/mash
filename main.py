# -*- coding: utf-8 -*-
import json

from utils import *

print ('''
Наш телеграмчик: @Termuxtop
• ▌ ▄ ·.  ▄▄▄· .▄▄ ·  ▄ .▄
·██ ▐███▪▐█ ▀█ ▐█ ▀. ██▪▐█
▐█ ▌▐▌▐█·▄█▀▀█ ▄▀▀▀█▄██▀▐█
██ ██▌▐█▌▐█ ▪▐▌▐█▄▪▐███▌▐▀
▀▀  █▪▀▀▀ ▀  ▀  ▀▀▀▀ ▀▀▀ ·
''')

raw_json = input("Введите значение JSON: ")
tasks = json.loads(escape_json(raw_json))

for task in tasks:
    answer_type = task["answer"]["type"]
    if answer_type == "answer/single":
        options = task["answer"]["options"]
        answer_id = task["answer"]["right_answer"]["id"]
        correct_answer = find_correct_single_answer(options, answer_id)
        log_answer(task, correct_answer)

    elif answer_type == "answer/multiple":
        options = task["answer"]["options"]
        answer_ids = task["answer"]["right_answer"]["ids"]
        for correct_answer in find_correct_multiple_answers(options, answer_ids):
            log_answer(task, correct_answer)

    elif answer_type in ["answer/match", "answer/match/timeline"]:
        for answer in match_answers(task, answer_type):
            first_part, second_part = answer
            log_answer(task, f"{first_part} - {second_part}")

    elif answer_type in ["answer/number", "answer/string"]:
        correct_answer = find_correct_other_answer(task, answer_type)
        log_answer(task, correct_answer)

    elif answer_type == "answer/groups":
        for answer in groups_answers(task):
            first_part, second_part = answer
            log_answer(task, f"{first_part} - {', '.join(second_part)}")

    elif answer_type == "answer/table":
        correct_answer = find_correct_other_answer(task, "cells")
        for row in correct_answer:
            for column in correct_answer[row]:
                log_answer(
                    task,
                    f"{int(column) + 1}-й столбец, {row}-ая строчка - {correct_answer[row][column]}",
                )

    elif answer_type == "answer/order":
        for answer in order_answers(task):
            log_answer(task, answer)
    elif answer_type == "answer/inline/choice/single":
        for position in task["answer"]["right_answer"]["text_position_answer"]:
            answer = inline_choice_single(task,position)
            log_answer(task, answer)
        
