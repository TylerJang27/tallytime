from typing import List

from tallytime.tally_log import (
    TallyLog,
    TallyLogSettings,
    TallySession,
    _TallySessionId,
)

__all__ = ["tallytime", "set_settings", "set_logger", "get_sessions", "get_session", "get_sessions_by_name", "get_session_by_name", "register",
           "update", "update_by_name", "delete", "delete_by_name", "display", "display_and_delete", "display_by_name", "display_and_delete_by_name"]

tallytime = TallyLog()


def set_settings(settings: TallyLogSettings) -> None:
    tallytime.set_settings(settings)


def set_logger(logger) -> None:  # TODO: ADD TYPE ANNOTATION
    tallytime.set_logger(logger)


def get_sessions() -> List[TallySession]:
    return tallytime.get_sessions()


def get_session(id: _TallySessionId) -> TallySession:
    return tallytime.get_session(id)


def get_sessions_by_name(name: str, force_all: bool = False) -> List[TallySession]:
    return tallytime.get_sessions_by_name(name, force_all)

# alias


def get_session_by_name(name: str, force_all: bool = False) -> List[TallySession]:
    return tallytime.get_session_by_name(name, force_all)


def register(name: str, force: bool = False, start_message: str = None) -> _TallySessionId:
    return tallytime.register(name, force, start_message)


def update(id: _TallySessionId, description: str = "Updated", force_create: bool = False) -> _TallySessionId:
    return tallytime.update(id, description, force_create)


def update_by_name(name: str, description: str = "Updated", force_create: bool = False, force_all: bool = False) -> List[_TallySessionId]:
    return tallytime.update_by_name(id, description, force_create, force_all)


def delete(id: _TallySessionId) -> TallySession:
    return tallytime.delete(id)


def delete_by_name(name: str, force_all: bool = False) -> List[TallySession]:
    return tallytime.delete_by_name(name, force_all)


def display(id: _TallySessionId) -> None:
    tallytime.display(id)


def display_and_delete(id: _TallySessionId, description: str = "Deleted") -> TallySession:
    return tallytime.display_and_delete(id, description)


def display_by_name(name: str, force_all: bool = False) -> None:
    tallytime.display_by_name(id, force_all)


def display_and_delete_by_name(name: str, description: str = None, force_all: bool = False) -> List[TallySession]:
    return tallytime.display_and_delete_by_name(id, description, force_all)
