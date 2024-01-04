# -*- coding: utf-8 -*-
import random
import string
from datetime import datetime, timedelta


def mock_str(length: int = 10):
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )
    return random_string


def mock_int(start: int = 1, end: int = 100):
    random_number = random.randint(start, end)
    return random_number


def mock_float(maxi: int = 10):
    random_float = random.random() * maxi
    return random_float


def mock_date(start_date, end_date):
    start = datetime.strptime(start_date, "%Y%m%d")
    end = datetime.strptime(end_date, "%Y%m%d")
    random_date = start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )
    return random_date.strftime("%Y%m%d")


def mock_chinese(length: int = 2):
    chinese_characters = [
        "好",
        "美",
        "你",
        "我",
        "他",
        "她",
        "是",
        "在",
        "有",
        "的",
        "一",
        "个",
        "不",
        "了",
        "人",
        "大",
        "中",
        "国",
        "上",
        "下",
        "天",
        "地",
        "时",
        "间",
        "生",
        "活",
        "家",
        "里",
        "工",
        "作",
        "学",
        "校",
        "朋",
        "友",
        "开",
        "心",
        "爱",
        "情",
        "今",
        "天",
        "明",
        "天",
        "昨",
        "天",
    ]

    random_chinese = "".join(random.choice(chinese_characters) for _ in range(length))
    return random_chinese


def mock_data():
    _id = str(mock_int(1, 100))
    _text = mock_str(10)
    _integer = mock_int(1, 10000)
    _float = mock_float(10000)
    _standard = mock_date("20240101", "20240131")
    _concept = mock_chinese(2)
    _confidence_concept = mock_float(1)
    _lead_to_concept2 = mock_chinese(2)
    _lead_to_concept3 = mock_chinese(2)
    _event = str(mock_int(1, 100))
    _confidence_event = mock_float(1)
    _source_event = mock_str(10)
    _entity = str(mock_int(100, 200))
    _entity_relation = str(mock_int(100, 200))
    return [
        _id,
        _text,
        _integer,
        _float,
        _standard,
        _concept,
        _confidence_concept,
        _lead_to_concept2,
        _lead_to_concept3,
        _event,
        _confidence_event,
        _source_event,
        _entity,
        _entity_relation,
    ]


if __name__ == "__main__":
    """
    ["id", "text", "integer", "float", "standard",
     "concept", "confidence_concept", "lead_to_concept2", "lead_to_concept3"
     "event", "confidence_event", "source_event",
     "entity", "entity_relation"],
    """
    import csv

    data_count = 1

    with open("data.csv", "a", newline="") as file:
        for _ in range(data_count):
            row_to_insert = mock_data()
            writer = csv.writer(file)
            writer.writerow(row_to_insert)
