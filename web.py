# -*- coding: utf-8 -*-
import json, os
from flask import Flask, request

app = Flask(__name__)

from utils import *


def answer_for_test(raw_json):
    tasks = json.loads(escape_json(raw_json))
    answers = []
    for task in tasks:
        answer_type = task["answer"]["type"]
        if answer_type == "answer/single":
            options = task["answer"]["options"]
            answer_id = task["answer"]["right_answer"]["id"]
            correct_answer = find_correct_single_answer(options, answer_id)
            answers.append(log_answer(task, correct_answer))

        elif answer_type == "answer/multiple":
            options = task["answer"]["options"]
            answer_ids = task["answer"]["right_answer"]["ids"]
            for correct_answer in find_correct_multiple_answers(options, answer_ids):
                answers.append(log_answer(task, correct_answer))

        elif answer_type in ["answer/match", "answer/match/timeline"]:
            for answer in match_answers(task, answer_type):
                first_part, second_part = answer
                answers.append(log_answer(task, f"{first_part} - {second_part}"))

        elif answer_type in ["answer/number", "answer/string"]:
            correct_answer = find_correct_other_answer(task, answer_type)
            answers.append(log_answer(task, correct_answer))

        elif answer_type == "answer/groups":
            for answer in groups_answers(task):
                first_part, second_part = answer
                answers.append(
                    log_answer(task, f"{first_part} - {', '.join(second_part)}")
                )

        elif answer_type == "answer/table":
            correct_answer = find_correct_other_answer(task, "cells")
            for row in correct_answer:
                for column in correct_answer[row]:
                    answers.append(
                        log_answer(
                            task,
                            f"{int(column) + 1}-й столбец, {row}-ая строчка - {correct_answer[row][column]}",
                        )
                    )

        elif answer_type == "answer/order":
            for answer in order_answers(task):
                answers.append(log_answer(task, answer))
        elif answer_type == "answer/inline/choice/single":
            for position in task["answer"]["right_answer"]["text_position_answer"]:
                answer = inline_choice_single(task, position)
                answers.append(log_answer(task, answer))
        elif answer_type == "answer/gap/match/text":
            for position in task["answer"]["right_answer"]["text_position_answer"]:
                answer = gap_match(task, position)
                answers.append(log_answer(task, answer))

    return answers


@app.route("/", methods=["POST"])
def login():
    answer = ""
    try:
        json = request.form["json"]
        answers = answer_for_test(json)
        for i in answers:
            answer += str(i) + "&#13;&#10;"
        answer = answer[0:-10]
    except Exception as e:
        answer = str(e)

    return (
        """
    <html>
    <head>
    <title>МЭШ</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    </head>
    <body>
    <form action="">
    <label for="tweet">Я помогу тебе получить ответы для МЭШ</label>
    <textarea id="tweet" rows="3" disabled name="json" style="height: 25em;">"""
        + answer
        + """</textarea>
    <div class="bottom">
    </form>
    </div>
    <footer class="mt-auto py-3 footer">
    <span class="text-muted">Made by <a href="https://github.com/aiexz">aiexz</a> with ❤️</span>
    </footer>
    <body>
    <style>
    *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}
body, button, textarea {
    font-family: "Helvetica Neue", Helvetica, sans-serif;
    font-size: 18px;
}
body, textarea {
    color: #222;
}
body {
    height: 100vh;
    overflow: hidden;
}
form {
    position: absolute;
}
/* Tweet form */
form {
    margin: auto;
    top: 50%;
    left: 50%;
    width: calc(100% - 3em);
    max-width: 30em;
    transform: translate(-50%,-50%);
}
button, button span {
    border-radius: 1.5em;
}
button {
    background-color: #55abee;
    border: 0;
    color: #fff;
    display: inline-block;
    font-weight: bold;
}
button span {
    display: block;
    padding: 0.75em 1.5em;
    transition: all 0.1s linear;
}
button:hover span {
    background-color: rgba(255,255,255,0.2);
}
button:active span {
    background-color: rgba(0,0,0,0.2);
}
button span:focus {
    outline: 0;
}
button:disabled {
    opacity: 0.5;
}
button:disabled:hover span, 
button:disabled:active span {
    background-color: transparent;
}
label {
    display: block;
    margin-bottom: 0.75em;
}
textarea {
    border: 0;
    border-radius: 0.5em;
    box-shadow: 0 0 0 0.1em #a8ceee inset;
    margin: 0 auto 0.75em auto;
    padding: 0.75em;
    resize: none;
    width: 100%;
    height: 25em;
}
textarea:focus {
    box-shadow: 0 0 0 0.1em #55abee inset;
    outline: 0;
}
textarea::placeholder {
    color: #aaa;
}
.bottom {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}
.bottom > span {
    margin-right: 0.75em;
}
.footer {
    background: #f5f5f5;
    position: fixed;
    height: 50px;
    bottom: 0;
    width: 100%;
    text-align: center;
}
    </style>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/gsap/1.20.3/TweenMax.min.js'></script>
    <script src='https://s3-us-west-2.amazonaws.com/s.cdpn.io/16327/MorphSVGPlugin.min.js'></script>
    <script>
    document.addEventListener("DOMContentLoaded", function(){
    this.querySelector("textarea").addEventListener("keydown",ctChars);
});

function ctChars() {
    let el = this,
        to = setTimeout(function() {
            let len = el.value.length,
            btn = document.querySelector("button")
            btn.disabled = len == 0 ? true : false;
            clearTimeout(to);
        }, 1);
}
    </script>
     
</html>
    """
    )


@app.route("/", methods=["GET"])
def main():
    return """
    <html>
    <head>
    <title>МЭШ</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    </head>
    <body>
    <form action="" method="post">
    <label for="tweet">Я помогу тебе получить ответы для МЭШ</label>
    <textarea id="tweet" rows="3" name="json" placeholder="Вставляй их сюда"></textarea>
    <div class="bottom">
        <button type="submit" tabindex="0" disabled>
            <span tabindex="-1">Расшифруй</span>
        </button>
    </div>
    </form>
    <footer class="mt-auto py-3 footer">
    <span class="text-muted">Made by <a href="https://github.com/aiexz">aiexz</a> with ❤️</span>
    </footer>
    <body>
    <style>
    *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}
body, button, textarea {
    font-family: "Helvetica Neue", Helvetica, sans-serif;
    font-size: 18px;
}
body, textarea {
    color: #222;
}
body {
    height: 100vh;
    overflow: hidden;
}
form {
    position: absolute;
}
/* Tweet form */
form {
    margin: auto;
    top: 50%;
    left: 50%;
    width: calc(100% - 3em);
    max-width: 30em;
    transform: translate(-50%,-50%);
}
button, button span {
    border-radius: 1.5em;
}
button {
    background-color: #55abee;
    border: 0;
    color: #fff;
    display: inline-block;
    font-weight: bold;
}
button span {
    display: block;
    padding: 0.75em 1.5em;
    transition: all 0.1s linear;
}
button:hover span {
    background-color: rgba(255,255,255,0.2);
}
button:active span {
    background-color: rgba(0,0,0,0.2);
}
button span:focus {
    outline: 0;
}
button:disabled {
    opacity: 0.5;
}
button:disabled:hover span, 
button:disabled:active span {
    background-color: transparent;
}
label {
    display: block;
    margin-bottom: 0.75em;
}
textarea {
    border: 0;
    border-radius: 0.5em;
    box-shadow: 0 0 0 0.1em #a8ceee inset;
    margin: 0 auto 0.75em auto;
    padding: 0.75em;
    resize: none;
    width: 100%;
    height: 5em;
}
textarea:focus {
    box-shadow: 0 0 0 0.1em #55abee inset;
    outline: 0;
}
textarea::placeholder {
    color: #aaa;
}
.bottom {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}
.bottom > span {
    margin-right: 0.75em;
}
.footer {
    background: #f5f5f5;
    position: fixed;
    height: 50px;
    bottom: 0;
    width: 100%;
    text-align: center;
}
    </style>
    </script>
     <script src='https://cdnjs.cloudflare.com/ajax/libs/gsap/1.20.3/TweenMax.min.js'></script>
    <script src='https://s3-us-west-2.amazonaws.com/s.cdpn.io/16327/MorphSVGPlugin.min.js'>
    </script>
    <script>
    document.addEventListener("DOMContentLoaded", function(){
    this.querySelector("textarea").addEventListener("change",ctChars);
});

function ctChars() {
    let el = this,
        to = setTimeout(function() {
            let len = el.value.length,
            btn = document.querySelector("button")
            btn.disabled = len == 0 ? true : false;
            clearTimeout(to);
        }, 1);
}
    </script>
</html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

