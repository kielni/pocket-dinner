from collections import namedtuple
import os
import random
from typing import Set

import boto3
import jinja2
import pocket


Recipe = namedtuple("Recipe", ["title", "url", "img"])


def _get_param(name: str) -> str:
    """Get a parameter from AWS Parameter store."""
    ssm = boto3.client("ssm")
    param = ssm.get_parameter(Name=name, WithDecryption=True)
    return param["Parameter"]["Value"]


def from_pocket(consumer_key: str, access_token: str) -> Set[Recipe]:
    # http://getpocket.com/developer/docs/v3/retrieve
    client = pocket.Pocket(consumer_key, access_token)
    resp = client.get(state="all", tag="recipe", detailType="simple")
    items = resp[0]["list"]
    keys = list(items.keys())
    recipes: Set[Recipe] = set()
    while len(recipes) < 10:
        item = items[random.choice(keys)]
        if not item["resolved_title"]:
            continue
        recipes.add(
            Recipe(
                url=item["resolved_url"],
                title=item["resolved_title"],
                img=item.get("top_image_url"),
            )
        )
    return recipes


def to_html(recipes: Set[Recipe]) -> str:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
    template = env.get_template("list.jinja2")
    return template.render({"recipes": recipes})


def top_list(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": to_html(
            from_pocket(
                _get_param("POCKET_CONSUMER_KEY"), _get_param("POCKET_ACCESS_TOKEN")
            )
        ),
    }


if __name__ == "__main__":
    print(
        to_html(
            from_pocket(
                os.environ["POCKET_CONSUMER_KEY"], os.environ["POCKET_ACCESS_TOKEN"]
            )
        )
    )
