from typing import Optional, Iterable, List

from loguru import logger


def escape_json(unescaped_json: str) -> str:
    return (
        unescaped_json.replace("\\", "\\\\")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace('\\"', "»")
    )


def log_answer(task: dict, text: str) -> None:
    logger.info(f"Задание {task['taskNum']}) {text}")


def get_respective_content(answer: dict) -> Optional[str]:
    if answer["text"] != "":
        return answer["text"]

    for content_element in answer["content"]:
        if content_element["type"] == "content/math":
            return content_element["content"]
        elif content_element["type"] == "content/file":
            return (
                f"https://uchebnik.mos.ru/exam{content_element['file']['relative_url']}"
            )

    return None  # Is this even possible?


def find_correct_single_answer(
    possible_answers: List[dict], answer_id: int
) -> Optional[str]:
    for possible_answer in possible_answers:
        if possible_answer["id"] == answer_id:
            return get_respective_content(possible_answer)


def find_correct_multiple_answers(
    possible_answers: List[dict], answer_id: int
) -> Iterable[str]:
    for possible_answer in possible_answers:
        if possible_answer["id"] in answer_id:
            yield get_respective_content(possible_answer)


def find_correct_other_answer(task: dict, task_type: str):
    return task["answer"]["right_answer"][task_type.replace("answer/", "")]


def match_answers(task: dict, answer_type: str) -> Iterable[tuple]:
    correct_answer = find_correct_other_answer(task, answer_type)

    for match_id in correct_answer:
        task_content = ""
        task_correct_answer = ""
        for answer_variant in task["answer"]["options"]:
            if answer_variant["id"] == match_id:
                task_content = get_respective_content(answer_variant)
            elif answer_variant["id"] == correct_answer[match_id][0]:
                task_correct_answer = get_respective_content(answer_variant)

        yield task_content, task_correct_answer


def groups_answers(task: dict, answer_type: str = "groups") -> Iterable[tuple]:
    correct_answer_groups = find_correct_other_answer(task, answer_type)

    for group in correct_answer_groups:
        task_content = ""
        task_correct_answer = []
        for answer_variant in task["answer"]["options"]:
            if answer_variant["id"] == group["group_id"]:
                task_content = get_respective_content(answer_variant)
            elif answer_variant["id"] in group["options_ids"]:
                task_correct_answer.append(get_respective_content(answer_variant))

        yield task_content, task_correct_answer


def order_answers(task: dict, answer_type: str = "ids_order") -> Iterable[str]:
    correct_answers = find_correct_other_answer(task, answer_type)

    for correct_answer in correct_answers:
        for answer_variant in task["answer"]["options"]:
            if answer_variant["id"] == correct_answer:
                task_correct_answer = get_respective_content(answer_variant)

                yield task_correct_answer
