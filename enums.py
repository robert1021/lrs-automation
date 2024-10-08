from enum import Enum


class LRSTools(Enum):
    GENERATE_BATCH_IMPORT = "Generate Batch Import"
    PARENT_FILES_RPA = "Parent Files RPA"
    SUBMISSION_FILES_RPA = "Submission Files RPA"

    @classmethod
    def get_values(cls):
        return [member.value for member in cls]

