#!/usr/bin/env python3
"""
A simple demo for working with tallytime using the root TallyLog
Run with `python3 demo.py` from the repo root.
"""

from tallytime import delete, register, update


def run():
    # Returns a id used to update this TallySession
    id = register("A simple user session")
    # Adds an update log to the TallySession
    id = update(id)
    # Deletes the TallySession form the TallyLog, returning the removed object
    # Deleting is not treated as an update event
    # Use display_and_delete to output to a logger object
    tally_session = delete(id)
    # Print the returned TallySession
    print(tally_session)


if __name__ == "__main__":
    run()
