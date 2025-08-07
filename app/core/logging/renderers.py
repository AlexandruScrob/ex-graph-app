from devtools import PrettyFormat


class PrettyFormatRenderer:
    def __init__(self) -> None:
        pass

    def __call__(self, logger, name: str, event_dict):
        """The return type of this depends on the return type of self._dumps."""
        pp = PrettyFormat(
            indent_step=2,  # default: 4
            repr_strings=True,  # default: False
            simple_cutoff=2,  # default: 10 (if line is below this length it'll be shown on one line)
            yield_from_generators=False,  # default: True (whether to evaluate generators)
        )
        return pp(event_dict, highlight=True)
