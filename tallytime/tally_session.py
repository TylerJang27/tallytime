from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import uuid4

from tallytime._utils import _coalesce


@dataclass
class _TallyStatus():
    """Class for a recorded status snapshot, maintained by a TallySession instance"""
    description: str
    time: datetime  # TODO: INVESTIGATE ATOMIC TIME


class _TallySessionId():
    """Class for uniquely identifying a TallySession"""
    name: str
    uuid: uuid4

    def __init__(self, name: str = "None"):
        self.name = name
        self.uuid = uuid4()

    def __repr__(self):
        return _coalesce(self.name, self.uuid.__repr__())

    def __lt__(self, other):
        return self.uuid < other.uuid

    def __eq__(self, other):
        return self.uuid == other

    def __hash__(self):
        return self.uuid.__hash__()


class TallySession():
    """Class for an individual tracker, maintained by a TallyLog instance"""
    id: _TallySessionId
    expire_time: datetime = None
    statuses: List[_TallyStatus] = []
    # TODO: ADD PLUGGABLE REPR SUPPORT

    def __init__(self, id: _TallySessionId, expire_time: datetime, start_message: str = None):
        self.id = id
        self.expire_time = expire_time
        self.statuses = [_TallyStatus(
            _coalesce(start_message, "Initialized"), datetime.utcnow())]

    def update(self, description: str) -> None:
        self.statuses.append(_TallyStatus(description, datetime.utcnow()))

    def __repr__(self):
        ret = "TallySession '{}':\t(Expires at: {})".format(self.id.name,
                                                            self.expire_time)
        for k in range(len(self.statuses)):
            s = self.statuses[k]
            diff = 0 if k == 0 else s.time - self.statuses[k - 1].time
            ret += "\n\t{} \tdiff: {} {} ".format(
                s.description, diff, s.time)

        return ret
