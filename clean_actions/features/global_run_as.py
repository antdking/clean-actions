_runs_on_key = "runs-on"


def execute(obj: dict) -> None:
    default_runner = obj.get(_runs_on_key)
    if not default_runner:
        return

    for job in obj.get("jobs", {}).values():
        if _runs_on_key not in job:
            job[_runs_on_key] = default_runner

    # Clean up the left-overs
    obj.pop(_runs_on_key)
