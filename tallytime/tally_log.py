from datetime import datetime, timedelta
from logging import Logger  # trunk-ignore(flake8/TC003)
from typing import Dict, List

# TODO: VERIFY IMPORTS WORK AS PACKAGE
from tallytime.exceptions import (
    BadEnumTallyException,
    DuplicateNameTallyException,
    DuplicateTallyException,
    FatalTallyException,
    MissingTallyErrorException,
    MissingTallyWarnException,
)
from tallytime.loggers import DefaultConsoleLogger
from tallytime.settings import LogLevel, TallyLogSettings, _log_level_map
from tallytime.tally_session import TallySession, _TallySessionId


def _log_message(logger: Logger, level: LogLevel, message: str, *args) -> None:
    if logger is not None:
        log_method_name = _log_level_map.get(level)
        if log_method_name is None:
            raise BadEnumTallyException(level, LogLevel)
        log_method = getattr(logger, log_method_name)

        log_method(message.format(*args))
    else:
        print("NONE")


class TallyLog():
    _sessions: Dict[_TallySessionId, TallySession] = {}
    _name_set: Dict[str, _TallySessionId] = {}
    _settings: TallyLogSettings
    _logger: Logger

    def __init__(self, settings: TallyLogSettings = TallyLogSettings(), logger: Logger = DefaultConsoleLogger()):
        self._settings = settings
        self._logger = logger
        if self._settings.log_on_init:
            _log_message(self._logger, self._settings.default_log_level,
                         "Initialized TallyLog object named {}", self._settings.name)

    def set_settings(self, settings: TallyLogSettings) -> None:
        self._settings = settings

    def set_logger(self, logger: Logger) -> None:
        self._logger = logger

    def __repr__(self):
        return ["{}".format(self._sessions[id]) for id in self._sessions]

    def get_sessions(self) -> List[TallySession]:
        return self._sessions

    def get_session(self, id: _TallySessionId) -> TallySession:
        session = self._sessions.get(id)
        if session is None:
            raise MissingTallyErrorException()
        return session

    def get_sessions_by_name(self, name: str, force_all: bool = False) -> List[TallySession]:
        name_match = self._name_set.get(name, [])

        if len(name_match) == 0:
            raise MissingTallyErrorException()

        elif len(name_match == 1):
            id = name_match[0]
            return [self._session[id]]

        elif (not force_all) and len(name_match) > 1:
            raise DuplicateTallyException()

        sessions = []
        for match in name_match:
            if match not in self._sessions:
                raise FatalTallyException()
            else:
                sessions.append(self._sessions[match])
        return sessions

    # alias
    def get_session_by_name(self, name: str, force_all: bool = False) -> List[TallySession]:
        return self.get_sessions_by_name(name, force_all)

    def _tidy(self) -> None:
        # TODO: UPDATE LOGIC
        items = self._sessions.items()
        for k in range(len(items))[::-1]:
            items = list(items)
            if items[k][1].expire_time < datetime.utcnow():
                del self._sessions[items[k][0]]
            else:
                break

    def register(self, name: str, force: bool = False, start_message: str = None) -> _TallySessionId:
        self._tidy()
        if name in self._name_set:
            if not force:
                raise (DuplicateNameTallyException("name {}".format(name)))

        id = _TallySessionId(name)
        access_token_expires = timedelta(
            seconds=self._settings.default_expire_time)
        expire_time = datetime.utcnow() + access_token_expires
        new_session = TallySession(id, expire_time, start_message)

        self._sessions[id.uuid] = new_session
        if name not in self._name_set:
            self._name_set[id.name] = []
        self._name_set[id.name].append(id)

        return id

    def update(self, id: _TallySessionId, description: str = "Updated", force_create: bool = False) -> _TallySessionId:
        session = self.get_session(id)
        if session is not None:
            session.update(description)
        else:
            if force_create:
                new_session = self.register(id.name)
                # TODO: DEPENDING ON SETTINGS, LOG WARNING AND CREATION
                return new_session
            else:
                raise MissingTallyWarnException()
        # TODO: DEPENDING ON SETTINGS, LOG

        return session.id

    # TODO: ADD HELP TEXT: force makes if not present, also gets first match if present
    def update_by_name(self, name: str, description: str = "Updated", force_create: bool = False, force_all: bool = False) -> List[_TallySessionId]:
        sessions = self.get_sessions_by_name(name, force_all)
        ret = []

        if len(sessions) == 1:
            ret = sessions[0].id
        elif len(sessions) > 1:
            if force_all:
                for session in sessions:
                    session.update(description)
                    ret.append(session.id)
            else:
                raise FatalTallyException()
        elif len(sessions) == 0:
            if force_create:
                ret = [self.register(name)]
            else:
                MissingTallyWarnException()

        # TODO: DEPENDING ON SETTINGS, LOG THIS
        return ret

    def delete(self, id: _TallySessionId) -> TallySession:
        self._tidy()
        session = self.get_session(id)

        if session is None:
            MissingTallyErrorException()
        del self._sessions[id]

        name_set = self._name_set[id.name]
        if len(name_set) == 1:
            del self._name_set[id.name]
        else:
            for index, name_id in enumerate(name_set):
                if name_id == id:
                    del self._name_set[id.name][index]
                    break

        return session

    # TODO: ADD HELP TEXT
    def delete_by_name(self, name: str, force_all: bool = False) -> List[TallySession]:
        self._tidy()
        sessions = self.get_sessions_by_name(name, force_all)
        ret = []

        if len(sessions) == 1:
            ret = [sessions[0]]
        elif len(sessions) > 1:
            if force_all:
                for session in sessions:
                    ret.append(session)
            else:
                raise DuplicateTallyException()
        elif len(sessions) == 0:
            raise MissingTallyErrorException()

        del self._name_set[name]
        for id in [sessions.id for session in sessions]:
            del self._sessions[id]
        return ret

    def display(self, id: _TallySessionId) -> None:
        self._tidy()
        session = self.get_session(id)
        _log_message(
            self._logger, self._settings.default_log_level, str(session))

    def display_and_delete(self, id: _TallySessionId, description: str = "Deleted") -> TallySession:
        self.update(id, description)
        self.display(id)
        return self.delete(id)

    def display_by_name(self, name: str, force_all: bool = False) -> None:
        sessions = self.get_sessions_by_name(name, force_all)
        for session in sessions:
            self.display(session.id)

    def display_and_delete_by_name(self, name: str, description: str = None, force_all: bool = False) -> List[TallySession]:
        sessions = self.get_sessions_by_name(name, force_all)
        ret = []
        for session in sessions:
            ret.append(self.display_and_delete(session.id, description))
        return ret
