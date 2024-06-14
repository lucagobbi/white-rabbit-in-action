# White Rabbit In Action

<img src="./assets/white-rabbit-in-action.png" width=400>

[![awesome plugin](https://custom-icon-badges.demolab.com/static/v1?label=&message=awesome+plugin&color=F4F4F5&style=for-the-badge&logo=cheshire_cat_black)](https://)

White Rabbit In Action is a Cheshire Cat plugin that seamlessly integrates scheduling capabilities into your plugins and tools without requiring you to write specific scheduling code.

Let the White Rabbit decide when your tools are executed!

## Overview

The White Rabbit In Action introduces a new Python annotation into the framework called `@white_rabbit_tool`, an enhanced version of the standard Cheshire Cat `@tool`. The `@white_rabbit_tool` allows you to bypass writing specific scheduling code by utilizing the White Rabbit component within the Cheshire Cat framework. It wraps your function similarly to the standard `@tool`, but with added capabilities for handling scheduling functions. This means the Agent can determine whether the triggered tool needs immediate execution (as usual) or should be scheduled to run in the future or according to a specified cron expression.

## Key Features

- **Automatic Scheduling**: The White Rabbit component manages the timing of tool execution, freeing you from the complexity of scheduling code.
- **Intelligent Execution**: The Agent understands if a tool needs instant execution or should be scheduled for the future.
- **Flexible Scheduling Options**: Schedule tools to run at specific times or intervals using cron expressions.

## Usage

### How to use the annotation

To enable scheduling capabilities of White Rabbit In Action, apply the `@white_rabbit_tool` annotation to your functions, just like you would normally do with standard Cheshire Cat tools. This allows the Agent to manage their execution schedule.

```python

from white_rabbit_in_action import white_rabbit_tool

@white_rabbit_tool
def turn_on_lights(cat):
    """
    Call this tool whenever the user wants to turn on the lights.
    """
    
    cat.send_ws_message("Turning on the lights", msg_type="chat")

```

> **Warning ⚠️**
> 
> This implementation modifies some mechanisms within the Cheshire Cat framework. As a consequence, certain features, such as `return_direct`, will not work as expected. Please consider this limitation when developing your own plugins.


### Managing scheduled jobs

In addition to scheduling, White Rabbit In Action provides basic Cheshire Cat tools to manage scheduled jobs in a conversational manner. These tools include:

- **Retrieve Scheduled Jobs**: View a list of all scheduled jobs.
- **Pause a Scheduled Job**: Temporarily halt a scheduled job without removing it.
- **Resume a Scheduled Job**: Reactivate a paused job.
- **Remove a Scheduled Job**: Delete a scheduled job.

