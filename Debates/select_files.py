import glob

from pathlib import Path

import xml.etree.ElementTree as ET
from collections import defaultdict

from pprint import pp

import pandas as pd

from datetime import datetime

DEBATES_DIR = Path("scrapedxml/debates")

test_file = DEBATES_DIR / "debates2023-03-02b.xml"

all_files = list(DEBATES_DIR.glob("*.xml"))

def get_speech_text(elem) -> str:
    child_text = [get_text_recursively(x) for x in elem]
    return " ".join(child_text)

def get_text_recursively(elem) -> str:
    # text before another element is found
    own_text = elem.text
    # text of parent after the other element is skipped
    extra_text = elem.tail
    # text inside the child element
    child_text = [get_text_recursively(x) for x in elem]
    text_pieces = (own_text, *child_text, extra_text)
    # puts all the text pieces together and skips if no text is found
    join_text = " ".join([x for x in text_pieces if x is not None])
    return join_text.strip()

def parse_file(filename: Path) :
    tree = ET.parse(filename)
    root = tree.getroot()

    key_sets = defaultdict(set)

    result_list = []
    minor_heading = None

    for elem in root:
        key_sets[elem.tag].update(elem.keys())

        if elem.tag == "major-heading":
            major_heading = elem.text.strip().replace("\n", " ")
            minor_heading = None
            #print(major_heading)

        if elem.tag == "minor-heading":
            minor_heading = elem.text.strip().replace("\n", " ")
            #print(minor_heading)

        if elem.tag == "speech" and "nospeaker" not in elem.keys() and major_heading not in ["Speaker’s Statement", "Prayers -"]:
            speech_text = get_speech_text(elem)
            speaker_name = elem.get("speakername")
            speaker_id = elem.get("person_id")
            #print(speaker_name, speaker_id)
            result = {"major_heading": major_heading, "minor_heading": minor_heading,
                    "text": speech_text, "speaker": speaker_name, "person_id": speaker_id}
            result_list.append(result)  

    dataset = pd.DataFrame(result_list)

    dataset["date"] = datetime.fromisoformat(filename.stem[7:-1])

    return dataset

dataset_list = []

grouped_files = defaultdict(list)

for file in all_files:
    grouped_files[file.name[0:17]].append(file)
    
for k,v in grouped_files.items():
    # the v-1 selects the last item in the list for each date
    dataset_list.append(parse_file(sorted(v)[-1]))

dataset = pd.concat(dataset_list)
print(dataset.head())

people_info = pd.read_csv("people_dataset_test.csv")
print(people_info.head())

people_info.drop(columns = ["given_name", "family_name", "surname", "lordname", "current_consituency"], inplace = True)

joined_dataset = dataset.merge(people_info, on = "person_id", how = "left")

print(joined_dataset.head())

joined_dataset.to_csv("all_debate_text.csv", index=False)