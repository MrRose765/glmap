"""CLI entry point for the ghmap tool.
Processes GitHub event data and converts it into structured actions and activities.
"""

import argparse
from importlib.resources import files
from .preprocess.event_processor import EventProcessor
from .mapping.action_mapper import ActionMapper
from .mapping.activity_mapper import ActivityMapper
from .utils import load_json_file, save_to_jsonl_file

def main():
    """Parse CLI arguments and run the GH mapping pipeline."""
    parser = argparse.ArgumentParser(
        description="Process GitHub events into structured activities."
    )
    parser.add_argument(
        '--raw-events', required=True,
        help="Path to the folder containing raw events."
    )
    parser.add_argument(
        '--output-actions', required=True,
        help="Path to the output file for mapped actions."
    )
    parser.add_argument(
        '--output-activities', required=True,
        help="Path to the output file for mapped activities."
    )
    parser.add_argument(
        '--actors-to-remove', nargs='*', default=[],
        help="List of actors to remove from the raw events."
    )
    parser.add_argument(
        '--repos-to-remove', nargs='*', default=[],
        help="List of repositories to remove from the raw events."
    )
    parser.add_argument(
        '--orgs-to-remove', nargs='*', default=[],
        help="List of organizations to remove from the raw events."
    )
    args = parser.parse_args()

    try:
        print("Step 0: Preprocessing events...")
        processor = EventProcessor()
        events = processor.process(
            args.raw_events,
            args.actors_to_remove,
            args.repos_to_remove,
            args.orgs_to_remove
        )

        print("Step 1: Mapping events to actions...")
        event_to_action_mapping_file = files("ghmap").joinpath("config", "event_to_action.json")
        action_mapping = load_json_file(event_to_action_mapping_file)
        action_mapper = ActionMapper(action_mapping)
        actions = action_mapper.map(events)
        save_to_jsonl_file(actions, args.output_actions)
        print(f"Step 1 completed. Actions saved to: {args.output_actions}")

        print("Step 2: Mapping actions to activities...")
        action_to_activity_mapping_file = files("ghmap").joinpath("config", "action_to_activity.json")
        activity_mapping = load_json_file(action_to_activity_mapping_file)
        activity_mapper = ActivityMapper(activity_mapping)
        activities = activity_mapper.map(actions)
        save_to_jsonl_file(activities, args.output_activities)
        print(f"Step 2 completed. Activities saved to: {args.output_activities}")

    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"An error occurred: {err}")

if __name__ == '__main__':
    main()
