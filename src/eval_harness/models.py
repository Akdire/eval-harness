from enum import Enum

class EvalCase:
    def __init__(self,input: str, expected: str):
        self.input = input
        self.expected = expected

    def to_dict(self) -> dict:
        return {"input": self.input, "expected": self.expected }

    @classmethod    
    def from_dict(cls, data):
        return cls(data["input"], data["expected"])    

class ResultStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"

class EvalResult:
    def __init__(self, case: EvalCase, actual_output: str, status: ResultStatus):
        self.case = case
        self.actual_output = actual_output
        self.status = status

    def to_dict(self) -> dict:
        return {"case": self.case.to_dict(), "actual_output": self.actual_output, "status": self.status.value}
    
    @classmethod    
    def from_dict(cls, data):
        return cls(data["case"], data["actual_output"], data["status"]) 