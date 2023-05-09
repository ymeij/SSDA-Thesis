import json
from pathlib import Path
from pprint import pp
from pandas import DataFrame as df

people_file = Path("people.json")

with open(people_file, "r") as f:
    people_data: dict = json.load(f)


print(people_data.keys())
pp(people_data["persons"][0:5])

print(people_data["persons"][0].keys())


def person_interest_generator():
    for person_entry in people_data["persons"]:
        if "redirect" in person_entry.keys():
            # Skip redirect records
            continue

        given_name, family_name, surname, lordname = None, None, None, None
        try:
            for name_entry in person_entry["other_names"]:
                if "Main" == name_entry["note"]:


                    # Skip if it is an outdated name

                    if "end_date" in name_entry.keys():
                        continue

                    given_name = name_entry["given_name"]
                    family_name = name_entry.get("family_name", None)
                    surname = name_entry.get("surname", None)
                    lordname = name_entry.get("lordname", None)

            current_consituency = None
            current_party = None

            if "shortcuts" in person_entry:
                current_consituency = person_entry["shortcuts"].get(
                    "current_consituency", None
                )
                current_party = person_entry["shortcuts"].get("current_party", None)

            yield person_entry[
                "id"
            ], given_name, family_name, surname, lordname, current_consituency, current_party
        except KeyError:
            print(person_entry)


dataset = df(person_interest_generator())
print(dataset.head())

dual_names = dataset[(dataset[2].isnull()) & (dataset[3].isnull())& (dataset[4].isnull())]
print(dual_names.head())

dataset.columns = ["person_id", "given_name", "family_name", "surname", "lordname", "current_consituency", "current_party"]

dataset.to_csv("people_dataset_test.csv", index = False)