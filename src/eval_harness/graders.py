
def exact_match(output: str, expected: str) -> bool:
    return output == expected
 
def normalized_match(output: str, expected: str) -> bool:
    return output.strip().lower() == expected.strip().lower()

def contains_match(output: str, expected: str) -> bool:
        if expected == "":
            return False
        return expected in output


