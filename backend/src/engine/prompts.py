from llama_index.core import PromptTemplate
from llama_index.core.prompts import PromptType

text_qa_template_str = (
    "Context information is"
    " below.\n---------------------\n{context_str}\n---------------------\nUsing"
    " both the context information and also using your own knowledge, answer"
    " the question: {query_str}\nIf the context isn't helpful, you can also"
    " answer the question on your own.\n"
)

kg_triplet_extract_template_str = """
    You are engineered for organising data into knowledge graphs.\n
    You should extract knowledge triplets in the form of (subject, predicate, object).extract up to "\n
    "{max_knowledge_triplets}, it can be less"\n
    - **Nodes**: Represent entities and ideas.\n
    - The objective is to ensure the knowledge graph is straightforward and intelligible for broad use.\n

    ## Node Labeling\n
    - **Uniformity**: Stick to simple labels for nodes.\n
    For instance,label any entity that is an organisation as "company",
    rather than using terms like "Facebook" or "Amazon".
    - **Identifiers for Nodes**: Opt for textual or comprehensible identifiers over numerical ones.\n
      - **Permissible Node Labels**: If there are specific allowed node labels, list them here.\n
      - **Permissible Relationship Types**: If there are specific allowed relationship types, list them here.\n

    ## Managing Numerical Data and Dates\n
    - Integrate numerical information directly as attributes of nodes.\n
    - **Integrated Dates/Numbers**: Refrain from creating distinct nodes for dates or numbers,
    attaching them instead as attributes.\n
    - **Format for Properties**: Use a key-value pairing format.\n
    - **Avoiding Quotation Marks**: Do not use escaped quotes within property values.\n
    - **Key Naming**: Adopt camelCase for naming keys, such as `dateTime`.\n

    ## Uniformity\n
    - **Entity Uniformity**: Ensure consistent identification for entities across various mentions or references.\n

    ## Adherence to Guidelines\n
    Strict adherence to these instructions is mandatory. Non-adherence will result in termination.\n
    "---------------------\n"
    "Example:"
    "Text: Alice is Bob's mother."
    "Triplets:\n(Alice, is mother of, Bob)\n"
    "---------------------\n"
    Do not produce Alice and Bob connections.
    "Text: {text}\n"
    "Triplets:\n"
    """

refine_template_str = (
    "The original question is as follows: {query_str}\nWe have provided an"
    " existing answer: {existing_answer}\nWe have the opportunity to refine"
    " the existing answer (only if needed) with some more context"
    " below.\n------------\n{context_msg}\n------------\nUsing both the new"
    " context and your own knowledge, update or repeat the existing answer.\n"
)

refine_template = PromptTemplate(refine_template_str, prompt_type=PromptType.REFINE)
text_qa_template = PromptTemplate(
    text_qa_template_str, prompt_type=PromptType.QUESTION_ANSWER
)
kg_triplets_extract_template = PromptTemplate(
    kg_triplet_extract_template_str, prompt_type=PromptType.KNOWLEDGE_TRIPLET_EXTRACT
)
