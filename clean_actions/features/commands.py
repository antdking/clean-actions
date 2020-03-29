def execute(obj: dict) -> None:
    for job in obj.get("jobs", {}).values():
        build_job(obj, job)


def build_job(obj: dict, job: dict) -> None:
    # get the first step that references a command
    index = next(
        (
            i
            for i, step in enumerate(job.get("steps", []))
            if step_is_calling_a_command(step)
        ),
        None,
    )

    if index is None:
        return  # No more steps have a command

    # we need to clear the old step from the steps, as it's invalid
    # in github world.
    step = job["steps"].pop(index)

    command_name = step["command"]
    command = get_command(obj, command_name)
    command_steps = command.get("steps", [])

    # We go in reverse, as we're inserting at the same index each time.
    # This will result in the steps being added in order.

    for command_step in reversed(command_steps):
        job["steps"].insert(index, command_step)

    # Move on to the next step.
    # We do this recursively, reading from the start of the steps each time,
    # as a command can reference another command.

    build_job(obj, job)


def step_is_calling_a_command(step: dict) -> bool:
    return "command" in step


def get_command(obj: dict, name: str) -> dict:
    command = obj["commands"][name]
    return command
