import json
import os
import time

import pocket


def parse_item(item: dict) -> dict:
    return {
        "title": item.get("given_title", item.get("resolved_title", "")),
        "url": item["given_url"],
        "excerpt": item["excerpt"],
        "tags": list(item.get("tags", {}).keys()),
    }


def write(items: list[dict]):
    print(f"Writing {len(items)} results to pocket.json")
    with open("pocket.json", "w") as f:
        json.dump(items, f, indent=2, default=str)


def main():
    # http://getpocket.com/developer/docs/v3/retrieve
    consumer_key = os.getenv("POCKET_CONSUMER_KEY")
    access_token = os.getenv("POCKET_ACCESS_TOKEN")
    client = pocket.Pocket(consumer_key, access_token)
    offset = 0
    count = 30  # Maximum items per request allowed by Pocket API
    all_items = []
    write_at = 500

    while True:
        print(f"offset: {offset}")
        try:
            resp = client.get(
                state="all", detailType="simple", count=count, offset=offset
            )
        except pocket.PocketException as e:
            print(f"Error getting items: {e}")
            break
        with open("resp.json", "w") as f:
            json.dump(resp, f, indent=2, default=str)
        items = list(resp[0]["list"].values())
        if not items:
            break
        for idx, item in enumerate(items):
            # print(f"\t{idx}/{len(items)}")
            if not item.get("given_url"):
                print(f"Skipping item without given_url: {json.dumps(item, indent=2)}")
                continue
            try:
                all_items.append(parse_item(item))
            except Exception as e:
                print(f"Error parsing item: {e} {json.dumps(item, indent=2)}")
                break
        time.sleep(1)

        offset += count
        print(f"{len(all_items)} total items")
        if len(all_items) >= write_at:
            write(all_items)
            write_at += 500

    write(all_items)


if __name__ == "__main__":
    main()
