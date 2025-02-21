from llama_index.core import PromptTemplate
from llama_index.core.prompts import PromptType

SUGGESTED_QUESTION = {
    "Contradictions": """
        Act as a Text Analysis Agent. Your goal is to identify inconsistencies within the documents/transcripts/texts containing multiple speakers.
        **Instructions:**
        1. **Ingest Transcript:** Thoroughly read the provided transcript.
        2. **Identify Speakers:**  Create a list of all distinct speakers.
        3. **Analyze for Inconsistencies:**
           * **Factual Contradictions:** Look for statements by a speaker that directly conflict with their other statements or established facts.
           * **Shifts in Opinion/Recollection:**  Note any changes in a speaker's expressed beliefs, memories, or accounts of events.
           * **Logical Discrepancies:** Identify statements that, when taken together, create illogical or nonsensical conclusions.
        4. **Extract Evidence (Quotes):**
           * For each potential inconsistency, locate and copy the exact phrases or sentences that demonstrate the discrepancy. Include timestamps or page/line numbers.
        5. **Construct Results Table:**
        | Speaker | Inconsistent Statement 1 | Inconsistent Statement 2 | Justification (Quoted Evidence) |
        |---|---|---|---|
        | ... | ... | ... | ... |
        **Example:**
        If Speaker A says, *"I never left the house on Tuesday,"* but later states, *"I remember running into a friend at the store on Tuesday afternoon,"* the table would show:
        | Speaker | Inconsistent Statement 1 | Inconsistent Statement 2 | Justification (Quoted Evidence) |
        |---|---|---|---|
        | Speaker A | "I never left the house on Tuesday" | "I remember running into a friend at the store on Tuesday afternoon" | These statements are contradictory as the speaker claims to have both stayed home and gone out on Tuesday. |
        **Additional Guidelines:**
        * **Prioritize:** Focus on inconsistencies that are most relevant to the transcript's purpose or central topic.
        * **Context:** Consider the overall context to avoid flagging minor discrepancies or statements that are later clarified.
        * **Nuance:** Distinguish between genuine inconsistencies and differences in phrasing or perspective that don't necessarily represent contradictions.
        **Output Format:**
        Your final output should be a well-formatted table as shown above, making it easy to review and understand the identified inconsistencies.
        """,
    "Expert Outline": """
            Act as a Legal Deposition Agent. Your goal is to create a detailed deposition outline for the next deposition with a new expert witness for the plaintiff’s case, based on all the provided documents and previous depositions.
            Instructions:

        1.	Review Provided Materials:
        •	Thoroughly read through all documents, transcripts, and previous depositions related to the case.
        2.	Analyze for Key Information:
        •	Identify crucial pieces of information, facts, and details from the documents and previous depositions.
        3.	Develop Questions:
        •	Formulate questions that connect and relate to the identified key information.
        •	Ensure that the questions address and build upon the data and insights from previous depositions and documents.
        4.	Structure the Outline:
        •	Organize the questions into a logical sequence that facilitates a smooth flow during the deposition.
        •	Group related questions together to maintain coherence and context.
        5.	Incorporate Relevant Details:
        •	Include specific references to previous depositions and documents to substantiate the questions.
        •	Highlight any inconsistencies or contradictions that the expert witness should address.
        6.	Prepare Follow-up Questions:
        •	Create additional questions to probe deeper into the expert witness’s responses and uncover further relevant details.
        •	Ensure these follow-up questions maintain the connection with the previous depositions and documents.

        Example:

        •	Introduction:
        •	Can you please state your name and professional background for the record?
        •	How long have you been working in your current field?
        •	Specific Inquiry:
        •	Based on the document [Document Name, Page #], it is mentioned that [specific fact]. Can you elaborate on this?
        •	In a previous deposition on [Date], [Witness Name] mentioned [specific statement]. How does this align with your findings?
        •	Clarification of Contradictions:
        •	During the deposition on [Date], [Witness Name] stated [statement 1], but later mentioned [statement 2]. Can you help clarify this discrepancy?
        •	Given the data from [Document Name], how would you interpret [specific situation or fact] in light of [previous deposition statement]?

        Additional Guidelines:

        •	Relevance: Focus on questions that are directly relevant to the case and the expert witness’s area of expertise.
        •	Clarity: Ensure that each question is clear and concise, avoiding any ambiguity.
        •	Depth: Aim to cover not just surface-level information but also delve into deeper insights and connections.

        Output Format:
        Your final output should be a well-organized and comprehensive deposition outline, structured to facilitate an effective and thorough deposition of the expert witness.
        """,
    "Timeline": """
        Act as a Legal Chronologist. Your goal is to create a detailed chain of events as described in the depositions that relate to the sequence of events involving Mr. Tolson, including dates, locations, and participants.

        Instructions:

            1.	Ingest Deposition Material:
            •	Thoroughly read through all depositions and documents related to Mr. Tolson’s case.
            2.	Extract Key Events:
            •	Identify and list all significant events, including the dates, locations, and participants involved.
            3.	Justify with Quotes:
            •	For each event, include direct quotes from the documents that justify the event’s inclusion and provide context.
            4.	Create a Timeline Table:
            •	Organize the events into a table with columns for Date, Event, Location, Participants, and Justification (Quotes).
            5.	Generate a Timeline Graph:
            •	Create a visual representation of the events over time.
            •	Ensure the graph is visually appealing and clearly shows the sequence of events.

        Output Format:

            •	Table:
            •	A well-structured table listing all events with detailed justifications from the documents.
            •	Graph:
            •	A visually appealing timeline graph representing the different events over time.

        Example:

            | Date       | Event                             | Location          | Participants               | Justification (Quotes)                                           |
            |------------|-----------------------------------|-------------------|----------------------------|------------------------------------------------------------------|
            | 2023-01-15 | Incident at the park              | Central Park      | Mr. Tolson, Witness A      | "Mr. Tolson mentioned, 'I was in Central Park on the 15th...'"   |
            | 2023-02-10 | Meeting with Dr. Smith            | City Hospital     | Mr. Tolson, Dr. Smith      | "Dr. Smith’s deposition states, 'On February 10th, Mr. Tolson...'" |
            | 2023-03-05 | Discussion with Lawyer            | Downtown Office   | Mr. Tolson, Lawyer         | "The transcript shows, 'During our meeting on March 5th...'"     |

            Timeline of Events Involving Mr. Tolson:

            2023-01-15: Incident at the park
                     |
                     |
                     v
            2023-02-10: Meeting with Dr. Smith
                     |
                     |
                     v
            2023-03-05: Discussion with Lawyer

        Additional Guidelines:

            •	Detail-Oriented: Ensure each event is thoroughly detailed with clear and specific quotes from the documents.
            •	Accuracy: Verify all dates, locations, and participant details for accuracy.
            •	Visual Appeal: Create a graph that is not only informative but also visually appealing to enhance understanding.
                """,
    "Entities": """
        Act as a Legal Entity Extraction Agent. Your goal is to extract all entities of location, places, people, dates (times), objects, and more from the case. Present this information in a table with the exact quote for each entity.

        Instructions:

        1.	Ingest Case Material:
        •	Thoroughly read through all documents and depositions related to the case.
        2.	Identify Entities:
        •	Extract all entities including locations, places, people, dates (times), objects, and other relevant entities.
        3.	Document Quotes:
        •	For each entity, find and record the exact quote from the documents or depositions that mentions the entity.
        4.	Create an Entity Table:
        •	Organize the extracted entities into a table with columns for Entity Type, Entity, Location in Document (e.g., page/line number or timestamp), and Exact Quote.

        Output Format:

        •	A well-organized table listing all entities with their types, locations in the document, and the exact quotes.

        Example:

        | Entity Type | Entity          | Location in Document  | Exact Quote                                                       |
        |-------------|-----------------|-----------------------|-------------------------------------------------------------------|
        | Location    | Central Park    | Page 12, Line 8       | "Mr. Tolson mentioned, 'I was in Central Park on the 15th...'"    |
        | Person      | Dr. Smith       | Page 45, Line 22      | "Dr. Smith’s deposition states, 'On February 10th, Mr. Tolson...'"|
        | Date        | 2023-01-15      | Page 12, Line 8       | "Mr. Tolson mentioned, 'I was in Central Park on the 15th...'"    |
        | Object      | Briefcase       | Page 30, Line 5       | "The briefcase contained all the documents related to the case.'" |

        Additional Guidelines:

        •	Comprehensive: Ensure that all relevant entities are extracted and accurately represented in the table.
        •	Precise: Verify the exact quotes and locations in the document to maintain accuracy.
        •	Clarity: Ensure the table is clear and easy to understand, with each entity properly categorized and documented.
    """,
    "Final Outline": """
        Act as a Legal Deposition Agent. Your goal is to create a detailed deposition outline for the questions the witness was asked, including the answers provided and suggested follow-up questions for further exploration.

        Instructions:

            1.	Review Deposition Material:
            •	Thoroughly read through the deposition transcripts to extract all questions asked and the corresponding answers provided by the witness.
            2.	Document Questions and Answers:
            •	List each question asked during the deposition and the answer provided by the witness.
            3.	Formulate Follow-Up Questions:
            •	For each question and answer pair, suggest a follow-up question that aims to explore and obtain more information.
            4.	Create an Outline Table:
            •	Organize the questions, answers, and follow-up questions into a table with columns for Question, Answer, and Follow-Up Question.

        Output Format:

            •	A well-organized table listing all questions, answers, and suggested follow-up questions.

        Example:

        | Question                               | Answer                                                  | Follow-Up Question                                      |
        |----------------------------------------|---------------------------------------------------------|---------------------------------------------------------|
        | What is your relationship with Mr. X?  | Mr. X is my business partner for the past 5 years.      | Can you describe a significant project you worked on together? |
        | Where were you on the night of the 5th?| I was at home watching TV.                              | Is there anyone who can verify your presence at home?   |
        | Did you see the defendant on that day? | Yes, I saw the defendant at the cafe around noon.       | Can you describe the conversation you had with the defendant? |

        Additional Guidelines:

            •	Accuracy: Ensure all questions and answers are accurately transcribed from the deposition transcripts.
            •	Relevance: Suggest follow-up questions that are relevant and likely to elicit further useful information.
            •	Clarity: Ensure the table is clear and easy to understand, with each question, answer, and follow-up question properly documented.
        """,
}

prompt_question_template = """
    Act as a Legal Analysis Agent. Your goal is to provide a detailed and structured response to the given question related to a legal case, based on the provided documents and depositions.
    \n---------------------\n{user_question}\n---------------------\n"
    Instructions:

        1.	Review Provided Materials:
        •	Thoroughly read through all relevant documents, transcripts, and depositions related to the case.
        2.	Identify Key Information:
        •	Extract and list all pertinent details, facts, and insights from the provided materials.
        3.	Formulate Response:
        •	Develop a comprehensive and well-structured response to the given question, ensuring all key information is included.
        4.	Provide Justification:
        •	Support your response with direct quotes and references from the documents, including exact page numbers, line numbers, or timestamps.
        5.	Suggest Follow-Up Questions (if applicable):
        •	If further exploration is needed, suggest relevant follow-up questions that aim to obtain more information.

    Output Format:

        •	A detailed response to the question, structured clearly and logically, with supporting quotes and references.
        •	Suggested follow-up questions, if necessary.

    Example:
    1. **Introduction:**
        - Brief overview of the context related to the question.

    2. **Key Information:**
        - List and summarize the key information extracted from the documents.

    3. **Answer:**
        - Provide the answer to the question based on the analysis and key information.

    4. **Justification:**
        - Include specific quotes and references from the documents.
        - Example: On 2023-01-15, Mr. Smith was at Central Park. (Page 12, Line 8: "Mr. Smith mentioned, 'I was in Central Park on the 15th...'")

    5. **Follow-Up Questions:**
        - Suggest follow-up questions to explore and obtain more information.
        - Example: What specific activities was Mr. Smith engaged in while at Central Park?

        Additional Guidelines:

        •	Comprehensive: Ensure all relevant information is included in the response.
        •	Accuracy: Verify all quotes and references for accuracy.
        •	Clarity: Ensure the response is clear and logically structured, making it easy to follow and understand.

    """

question_template = PromptTemplate(prompt_question_template, prompt_type=PromptType.QUESTION_ANSWER)
