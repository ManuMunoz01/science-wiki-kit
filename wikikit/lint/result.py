"""The value every check returns."""

# Counters that describe a check's context, not a finding: they never mark the check as "fired".
_NOT_FINDINGS = ("exempt", "unfielded", "_debt", "_stale_", "check25_")


class Result:
    """label: what the check measures. counters: {counter_name: int} (names match the fixtures'
    expected_counters.txt). files: {output_filename: [lines]} written to the output directory.
    fired: how many findings the check produced (decides whether its origin pointer is printed)."""

    def __init__(self, label, counters, files=None, fired=None):
        self.label = label
        self.counters = counters
        self.files = files or {}
        if fired is None:
            fired = sum(v for k, v in counters.items()
                        if v > 0 and not any(tag in k for tag in _NOT_FINDINGS) and not k.endswith("_exempt_stale"))
        self.fired = fired
