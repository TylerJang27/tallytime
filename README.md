# tallytime

A timeboxing and logging package for python. `tallytime` plugs into your existing logger to give you insight into your application's performance.

## Installation

- Run `python3 -m pip install tallytime`

## Usage

A root TallyLog object is available out of the box:

```python
from tallytime import display_and_delete, register, update

session_id = register("A simple user session")

// ...
update(session_id, "Finished querying database")

// ...
display_and_delete(session_id)
```

### Custom TallyLog Objects

Additional TallyLog objects can be instantiated, each with different settings.

```python
from tallytime.tally_log import TallyLog
from tallytime.settings import TallyLogSettings
from tallytime.loggers import DefaultFileLogger

settings = TallyLogSettings()
logger = DefaultFileLogger("./data/logs/tallytime.log")
tally_log = TallyLog(settings, logger)

session_id = tally_log.register("A simple user session")

// ...
tally_log.update(session_id, "Finished querying database")

// ...
tally_log.display_and_delete(session_id)
```

See _Model_ below for more details.

### Keying on Names

If you don't want to keep track of a `tallytime`-created session id, you can always pass in a unique string into the `register` invocation. Subsequent calls to `tallytime` methods should use the `_by_name` suffix, such as `update_by_name` or `display_and_delete_by_name`.

### Demo

Run `python3 demo.py` from the repository root to see an example.

## Model

`tallytime` involves 2 key data structures. A TallyLog is the primary interface, providing means of creating TallySessions, updating them with events, and displaying and deleting them. A TallySession is representative of an individual invocation (such as a user API request or a runtime of your program), which can be updated to track different events. All TallySessions are tracked by unique ids.

Currently, `tallytime`'s logging capacity is built on top of python's standard [logging library](https://docs.python.org/3/library/logging.html). TallyLog takes a logger in its constructor, which is used for information output. If you desire more extendable ways to customize the output, please reach out or add to GitHub Issues.

To work with these directly and use more configuration, import from any of the following branches:

- `tallytime.tally_log`: The core TallyLog logger
- `tallytime.tally_session`: An individual TallyLog session
- `tallytime.settings`: Configuration and defaults for a TallyLog object
- `tallytime.exceptions`: Error handling and exceptions
- `tallytime.loggers`: OOTB loggers for convenience, including DefaultConsoleLogger and DefaultFileLogger

## Configuration

By default, the following settings are in place:

- All TallySessions will expire _1 hour_ after they are first registered if not deleted
- Log level _INFO_ is used
- Times are rendered in _seconds_
- A TallySession will log its status on _each_ update call, _AND_ when `display` or `display_and_delete` is called.
- A TallyLog will log on its instantiation

## Coming Soon

- Support more configurable logger implementations
- Support more default overrides (such as setting a higher log level for a particular session)
- Better default settings
- More timezone customization
- Testing

## Credits

Implementation details inspired by the python [logging library](https://docs.python.org/3/library/logging.html).
