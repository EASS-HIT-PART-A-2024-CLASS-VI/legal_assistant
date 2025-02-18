prompt = (
    "Given some initial query, generate synonyms or related keywords up to {max_keywords} in total, "
    "considering possible cases of capitalization, pluralization, common expressions, etc.\n"
    "Provide all synonyms/keywords separated by '^' symbols: 'keyword1^keyword2^...'\n"
    "Note, result should be in one-line, separated by '^' symbols."
    "----\n"
    "QUERY: {query_str}\n"
    "----\n"
    "KEYWORDS: "
)


def parse_fn(output: str) -> list[str]:
    matches = output.strip().split("^")
    return [x.strip().capitalize() for x in matches if x.strip()]
