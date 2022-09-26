class TallyException(Exception):
    pass


class MissingTallyException(TallyException):
    pass


_MISSING_TALLY_ERROR_EXCEPTION_MSG = (
    "No TallySession exists matching your query. "
    "Check your default expire time and try again."
)


class MissingTallyErrorException(MissingTallyException):
    def __init__(self):
        super().__init__(_MISSING_TALLY_ERROR_EXCEPTION_MSG)


_MISSING_TALLY_WARN_EXCEPTION_MSG = (
    "No TallySession exists matching your query. "
    "Check your default expire time, pass `force_create=True`, and try again."
)


class MissingTallyWarnException(MissingTallyException):
    def __init__(self):
        super().__init__(_MISSING_TALLY_WARN_EXCEPTION_MSG)


_DUPLICATE_TALLY_EXCEPTION_MSG = (
    "There are multiple TallySessions matching your query. "
    "Please use a tally id or pass `force_all=True`"
)


class DuplicateTallyException(TallyException):
    def __init__(self):
        super().__init__(_DUPLICATE_TALLY_EXCEPTION_MSG)


_DUPLICATE_NAME_TALLY_EXCEPTION_MSG = (
    "A TallySession with {} already exists. "
    "Please use a unique tally name or pass `force=True` to create it anyway"
)


class DuplicateNameTallyException(TallyException):
    def __init__(self, name: str = "this name"):
        super().__init__(_DUPLICATE_NAME_TALLY_EXCEPTION_MSG.format(name))


_FATAL_TALLY_EXCEPTION_MSG = (
    "A TallyLog object has entered a bad state. "
    "Please check your function calls and try again."
)


class FatalTallyException(TallyException):
    def __init__(self):
        super().__init__(_FATAL_TALLY_EXCEPTION_MSG)
