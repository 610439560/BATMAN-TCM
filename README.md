# word_co-occurrence_analysis.py

BATMAN-TCM 2.0 is a traditional Chinese medicine (TCM) ingredients-target protein interaction(TTI) database that encompasses the most comprehensive TTI dataset available to date. During the TTI dataset collection of the BATMAN-TCM database, we utilized the following code to extract relationships between TCM ingredients and targets from the literature. Firstly, this code is used to retrieve PubMed IDs (PMID) of articles that have the compound name mentioned in their titles or abstracts from PubMed. Next, PubTator is employed to annotate the obtained article abstracts. Finally, sentences containing the TCM ingredients name, target proteins, and keywords related to their interactions are identified for further manual curation.

## Functions

### get_pmid(compound_list)

This function retrieves PubMed IDs (PMIDs) for the given list of compounds. It takes a list of compounds as input and returns a list of PMIDs.

**Parameters:**

- `compound_list` (list): A list of compounds.

**Usage:**

```python
compound_list = ["Bicyclomahanimbine", "Coumurrayin", "Musaroside"]
pmid = get_pmid(compound_list)
```

### pubtator_API(pmid)

This function retrieves entities extracted from PubTator for the given PMIDs and performs sentence parsing using the sentence_parse function. It takes a PMID as input and returns a list of lines containing the extracted information.

**Parameters:**

- `pmid` (str): The PubMed ID (PMID) to retrieve entities for.

**Usage:**

```python
pmid = "12345678"
result = pubtator_API(pmid)
```

### sentence_parse(sent)

This function parses a paragraph of text and extracts relevant information such as PMIDs, abstracts, entities (genes and compounds), and their relationships. It uses the check_sentence function to identify sentences that contain all three elements. It takes a paragraph of text as input and returns a list of lines containing the extracted information.

**Parameters:**

- `sent` (str): The paragraph of text to parse.

**Usage:**

```python
paragraph = "36914037\tActive ingredients of GXN-targets-related enzymes/transporters-metabolites network was estiblished to find out that GPX4 was a core protein involved for GXN and the top 10 active ingredients with the most relevant to renal protective effects of GXN were rosmarinic acid, caffeic acid, ferulic acid, senkyunolide E, protocatechualdehyde, protocatechuic acid, danshensu, L-Ile, vanillic acid, salvianolic acid A\tsalvianolic acid A\tMESH:C066201\tGPX4"
parsed_lines = sentence_parse(paragraph)
```

### check_sentence(sentence, a, b, c)

This function checks if a sentence contains all three elements: a compound, a gene, and a relationship. It takes a sentence, a list of compounds, a list of genes, and a list of relationships as input. It returns a boolean value indicating the presence of all elements, as well as the matched instances of each element.

**Parameters:**

- `sentence` (str): The sentence to check.
- `a` (list): A list of compounds.
- `b` (list): A list of genes.
- `c` (list): A list of relationships.

**Usage:**

```python
sentence = "Shikonin downregulated expression of NOX4, PTEN and p-p65, and upregulated p-AKT and Bcl-2 expression in HK2 cells treated with lipopolysaccharide (LPS)"
compounds = ["Shikonin"]
genes = ["p-AKT"]
relationships = ["activates", "inhibits"]
result = check_sentence(sentence, compounds, genes, relationships)
```

## Usage

1. Ensure that the "compound_list.txt" file contains a list of compounds.
2. Run the script to retrieve PMIDs related to the compounds and save them in the "related_article_pmid.txt" file.
3. The script will then retrieve entities from PubTator for each PMID and perform sentence parsing. The results will be appended to the "ingredient2gene.txt" file.

Note: The script retrieves literature related to compounds and performs co-occurrence analysis based on predefined relationships. Make sure to modify the relationship list ("relation") in the sentence_parse function according to your specific requirements.

Please ensure that you have the necessary dependencies installed