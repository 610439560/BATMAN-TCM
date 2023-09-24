import pandas as pd
import requests
from Bio import Entrez
import numpy as np


# Retrieve literature related to the compound research
def get_pmid(compound_list):
    pmid = []
    sep = 50
    circle = np.ceil(len(compound_list) / 50).astype(int)

    for i in range(1, circle + 1):
        if i == circle:
            t = len(compound_list)
        else:
            t = sep * i

        f = sep * (i - 1) + 1
        compound_query = " OR ".join(compound_list[f - 1:t])
        search_query = (
            f"({compound_query}[TIAB]) AND "
            f"((herb[TIAB]) OR (TCM[TIAB]) OR (traditional Chinese medicine[TIAB])) "
            f"AND (2020:2023[pdat]) NOT (Review[pt])"
        )

        handle = Entrez.esearch(db="pubmed", term=search_query, retmax=10000)
        search_results = Entrez.read(handle)
        handle.close()

        pmid = list(set(pmid).union(search_results["IdList"]))

    return pmid

# Main function: Retrieve entities extracted from PubTator and perform sentence parsing
def pubtator_API(pmid):
    url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator"
    params = {
        "pmids": pmid.strip(),
        "concepts": "gene,chemical"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return sentence_parse(response.text)
    else:
        print(f"Request failed, status code：{response.status_code}")
        return False


# Sentence parsing
def sentence_parse(sent):
    part = sent.strip().splitlines()

    if len(part) < 3:
        return False

    relation = ["Agonist", "activator", "Antagonist", "inhibitor", "Bind", "target", "bound", "Activate", "Augment",
                "Ameliorate", "Derepress", "Elevate", "Enhance", "Hasten", "Increase", "Induce", "Incitate",
                "Initiate",
                "Potentiate", "Promote", "Raise", "Stimulate", "Up-regulate", "Abrogate", "Abolish", "Against",
                "Attenuate", "Antagonize", "Block", "Blunt", "Down", "regulate", "Decrease", "Degrade", "Diminish",
                "Impair", "Inhibit", "Reduce", "Repress", "Suppress", "Affect", "Interact", "Disturb", "Regulate",
                "Impact", "Influence", "Interfere", "Modify", "Modulate", "Activity", "Activation", "Level",
                "Expression", "Pathway", "Cleavage", "Methylation", "Phosphorylation", "Severance", "Glycosylation",
                "Acetylation"]
    out_line = []

    pmid = part[0][:8]
    abst = part[1][11:]
    enti = part[2:]
    rows = [row.split('\t') for row in enti]
    columns = ["ID", "Start", "End", "Text", "Type", "Info"]

    if len(rows[0]) < 6:
        rows[0].append("")
    df = pd.DataFrame(rows, columns=columns)
    if not set(['Gene', 'Chemical']).issubset(df['Type'].unique()):
        return False
    df = df.drop_duplicates('Text')

    gene_rows = df[df['Type'] == 'Gene']
    com_rows = df[df['Type'] == 'Chemical']
    pair = df[["Text", "Info"]].set_index("Text").to_dict(orient='dict')["Info"]
    genes = set(gene_rows['Text'].values)
    coms = set(com_rows['Text'].values)
    sent = abst.split(". ")

    for s in sent:
        boo, match_com, match_gene, match_relat = check_sentence(s, coms, genes, relation)
        if boo:
            for i in match_com:
                for j in match_gene:
                    out_line.append(f"{pmid}\t{s}\t{i}\t{pair[i]}\t{j}\t{pair[j]}\t{'|'.join(match_relat)}")

    return out_line

# Detect co-occurrence of compound, gene, and relationship
def check_sentence(sentence, a, b, c):
    matched_a = []
    matched_b = []
    matched_c = []

    a_match = [word for word in a if word in sentence]
    b_match = [word for word in b if word in sentence]
    c_match = [word for word in c if word.lower() in sentence.lower()]

    a_exists = bool(a_match)
    b_exists = bool(b_match)
    c_exists = bool(c_match)

    if a_exists:
        matched_a.extend(a_match)
    if b_exists:
        matched_b.extend(b_match)
    if c_exists:
        matched_c.extend(c_match)

    return a_exists and b_exists and c_exists, matched_a, matched_b, matched_c


if __name__ == "__main__":


    with open("compound_list.txt", "r") as f1:
        syn = [line.strip() for line in f1.readlines()[0:50]]

    pmid = get_pmid(syn)

    with open("related_articla_pmid.txt", "w") as f2:
        f2.write("\n".join(pmid))

    with open("ingredient2gene.txt", "a+", encoding="utf-8") as f3:
        for id in pmid:
            res = pubtator_API(id)
            if res:
                s = "\n".join(res)
                f3.write(f"{s}\n")
            else:
                continue
