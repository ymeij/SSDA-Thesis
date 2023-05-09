from pathlib import Path
from pprint import pp
import pandas as pd
import plotly.express as px
import numpy as np

# THIS DATA CONTAINS THE BODY OF THE TEXT AND IS THEREFORE NOT AVAILABLE 
# THE CODE HAS BEEN PROVIDED TO UNDERSTAND THE FILTERING
data = pd.read_parquet("dataset_flattened.parquet")

print(data.shape)

# section types
print(data["section"].value_counts())
## get section types
def get_section_types(section: str) -> set[str]:
    part_bef_semi = section.split(";")[0]
    return set(part_bef_semi.split(","))

data["section"].fillna("", inplace=True)

# make all section with "pg" into same placeholder
data["section"][data["section"].str.contains("Pg.")] = "Pages Placeholder"

# apply function to get the section types without clutter
data["section_types"] = data["section"].apply(get_section_types)
#print(data["section_types"].value_counts())

# save the different sections as s set
section_set = set().union(*data["section_types"].values)
print(section_set)

# save the sections in a dataframe
newspaper_topics_to_excl = pd.DataFrame(section_set)

#newspaper_topics_to_excl.to_csv("newspaper_topics_to_excl.csv", index=False)
# I WILL DELETE THE ONES I DO WANT FROM THIS CSV

# now reupload this file after removing the topics i want to include
excl_sections_data = pd.read_csv("newspaper_topics_to_excl.csv", keep_default_na=False)
#print(excl_topics.head())
excl_sections = excl_sections_data["TOPICS"].to_list()

# now remove all articles that match their section to the section in the excl_topics file
## BUT - have to account for some articles having multiple section types

# create function for matching sections
def match_sections(sections: set) -> bool:
    # look for anti section types for each article, will return false if one section are to be excluded
    if any([x in excl_sections for x in sections]):
        return False
    else:
        return True
    # the output: false means at least one sections was bad, true means all section was good

# apply the function only to the section column and create a new variable whether the section is to be included or not
data["matched_section"] = data["section_types"].apply(match_sections)
print(data.shape)

# filter on the matched column to exclude sections 
section_filtered_data = data[data["matched_section"]==True]
print(section_filtered_data.shape)

# filter to exclude the duplicates 
# removing duplicates
data_filtered = section_filtered_data.drop_duplicates(subset=["title_line", "newspaper_line", "published_date"])
print(data_filtered.shape)

# look at articles that have the placeholder section type or no section type
pageholder_data = data_filtered[(data_filtered["section_types"]==set(("Pages Placeholder",)))|(data_filtered["section_types"]==set(("",))) ].copy()
print(pageholder_data.shape)

print(pageholder_data["section_types"].value_counts())

# set keywords those articles need to match
keywords = ["industrial action", "labour dispute", "industrial dispute", "walk out"]

def check_section_match(newspaper_text: str) -> bool:
    # look for keywords at the article level
        value = newspaper_text.lower()
        for keyword in keywords:
            if keyword in value:
                return True 
        return False

# apply the function
pageholder_data["text_matched_keyword"] = pageholder_data["body"].apply(check_section_match)
pageholder_data["title_matched_keyword"] = pageholder_data["title_line"].apply(check_section_match)

# keep results that have either matched column as true
def compare_columns_by_row(df, col_a, col_b):
    """Compare two columns by row and return a list of booleans indicating whether either column contains True."""
    result = []
    for index, row in df.iterrows():
        result.append(row[col_a] or row[col_b])
    return result

# apply the function
pageholder_data["matched_keyword"] = compare_columns_by_row(pageholder_data, "text_matched_keyword", "title_matched_keyword")
print(pageholder_data.head())

# filter out the false
pageholder_data_matched = pageholder_data[pageholder_data["matched_keyword"]==True]

# put the filtered pageholder data back to the original data
## first, drop the columns no longer needed
filtered_pageholder_data =  pageholder_data_matched.drop(["text_matched_keyword", "title_matched_keyword", "matched_keyword"] , axis=1)

## then, create the dataframe with the pageholder data excluded
filtered_data_no_pageholder = data_filtered[(data_filtered["section_types"]!=set(("Pages Placeholder",)))&(data_filtered["section_types"]!=set(("",)))]
print(filtered_data_no_pageholder.shape)

## now join it back with the other filtered df
final_filtered_data = pd.concat([filtered_pageholder_data, filtered_data_no_pageholder])
print(final_filtered_data.head())
print(final_filtered_data.shape)

# look at a subsample to investigate
final_filtered_data.iloc[1000:2000].to_excel("2_filtered_newspaper_sample.xlsx", index=False)

# save the now filtered data into a parquet
final_filtered_data.to_parquet("final_filtered_data.parquet", compression='zstd') # type: ignore
