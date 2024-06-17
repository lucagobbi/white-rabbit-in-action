from typing import Callable, Union, List

from cat.plugins.white_rabbit_in_action.utils import extract_int_from_string, parse_cron_expression, \
    extract_args_as_kwargs
from cat.mad_hatter.decorators.tool import CatTool
from cat.mad_hatter.decorators import tool
from cat.log import log

from cat.looking_glass.stray_cat import StrayCat


def classify_schedule(stray_cat: StrayCat) -> str:
    user_message = stray_cat.working_memory.user_message_json.text
    example_labels = {
        "fixed_date": ["Turn on the light in 30 seconds"],
        "cron_based": ["Turn on the light every morning at 7am"],
        "unscheduled": ["Turn on the light"]
    }
    schedule_type = stray_cat.classify(f"Extract the exact schedule from the following message: {user_message}",
                                       example_labels)
    return schedule_type


def schedule_function(type_of_schedule: str, func: Callable[[str], str], *args, **kwargs) -> Callable[[], None]:
    stray_cat = kwargs["cat"]
    user_message = stray_cat.working_memory.user_message_json.text

    def extract_seconds() -> int:
        seconds_expression = stray_cat.llm(
            f"Extract the exact number of seconds from the following message: {user_message}")
        return extract_int_from_string(seconds_expression)

    if type_of_schedule == "fixed_date":
        seconds = extract_seconds()
        log.debug(f"WhiteRabbitInAction - Schedule date: {seconds}")
        return stray_cat.white_rabbit.schedule_job(func, seconds=seconds, *args, **extract_args_as_kwargs(func, *args, **kwargs))
    elif type_of_schedule == "cron_based":
        cron_expression = stray_cat.llm(f"Deduce the exact cron expression (e.g. 0 7 * * *) from this message: {user_message}")
        log.debug(f"WhiteRabbitInAction - Schedule cron: {cron_expression}")
        return stray_cat.white_rabbit.schedule_cron_job(func, **parse_cron_expression(cron_expression), **extract_args_as_kwargs(func, *args, **kwargs))
    else:
        raise ValueError(f"WhiteRabbitInAction - Unknown schedule type: {type_of_schedule}")


def white_rabbit_tool(*args: Union[str, Callable], return_direct: bool = False, examples: List[str] = []) -> Callable:
    def _make_with_name(tool_name: str) -> Callable:
        def _make_tool(func: Callable[[str], str]) -> CatTool:

            def white_rabbit_func(*in_args, **kwargs):
                stray_cat = kwargs['cat']
                schedule_type = classify_schedule(stray_cat)
                log.debug(f"WhiteRabbitInAction - Classified schedule_type: {schedule_type}")

                if schedule_type == "unscheduled":
                    log.debug(f"WhiteRabbitInAction - Running function {func.__name__}")
                    return func(*in_args, **kwargs)

                log.debug(f"WhiteRabbitInAction - Scheduling function {func.__name__}")
                schedule_function(schedule_type, func, *in_args, **kwargs)
                return "Roger that. I'll run it later."

            assert func.__doc__, "Function must have a docstring"
            white_rabbit_func.__doc__ = func.__doc__

            tool_ = CatTool(
                name=tool_name,
                func=white_rabbit_func,
                return_direct=return_direct,
                examples=examples,
            )

            return tool_

        return _make_tool

    if len(args) == 1 and isinstance(args[0], str):
        return _make_with_name(args[0])
    elif len(args) == 1 and callable(args[0]):
        return _make_with_name(args[0].__name__)(args[0])
    elif len(args) == 0:
        def _partial(func: Callable[[str], str]) -> CatTool:
            return _make_with_name(func.__name__)(func)

        return _partial
    else:
        raise ValueError("Too many arguments for tool decorator")


@tool
def get_running_jobs(user_input, cat: StrayCat):
    """
    Call this tool whenever the user wants to get the running scheduled jobs.
    """
    return [{"id": job["id"], "name": job["name"], "next_run": job["next_run"].isoformat() if job["next_run"] else None}
            for job in cat.white_rabbit.get_jobs()]


@tool(return_direct=True)
def remove_job_by_id(job_id: str, cat: StrayCat):
    """
    Call this tool whenever the user wants to remove a scheduled job by id.
    """
    return cat.white_rabbit.remove_job(job_id)


@tool(return_direct=True)
def pause_job_by_id(job_id: str, cat: StrayCat):
    """
    Call this tool whenever the user wants to pause a scheduled job by id.
    """
    return cat.white_rabbit.pause_job(job_id)


@tool(return_direct=True)
def resume_job_by_id(job_id: str, cat: StrayCat):
    """
    Call this tool whenever the user wants to resume a scheduled job by id.
    """
    return cat.white_rabbit.resume_job(job_id)


# Example usage of the white rabbit tool
#
# @white_rabbit_tool
# def turn_on_lights(user_input, cat: StrayCat):
#     """
#     Call this tool whenever the user wants to turn on the lights.
#     """
#     cat.send_ws_message("Turning on the lights", msg_type="chat")
