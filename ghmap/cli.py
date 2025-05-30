"""Command-line interface for the GitHub Event Mapping Tool."""

import argparse
from importlib.resources import files
from .preprocess.event_processor import EventProcessor
from .mapping.action_mapper import ActionMapper
from .mapping.activity_mapper import ActivityMapper
from .utils import load_json_file, save_to_jsonl_file


def main():
    """Parse arguments and run the event-to-activity mapping pipeline."""
    parser = argparse.ArgumentParser(
        description="Process GitHub events into structured activities."
    )
    parser.add_argument(
        '--raw-events',
        required=True,
        help="Path to the folder containing raw events."
    )
    parser.add_argument(
        '--output-actions',
        required=True,
        help="Path to the output file for mapped actions."
    )
    parser.add_argument(
        '--output-activities',
        required=True,
        help="Path to the output file for mapped activities."
    )
    parser.add_argument(
        '--actors-to-remove',
        nargs='*',
        default=[],
        help="List of actors to remove from the raw events."
    )
    parser.add_argument(
        '--repos-to-remove',
        nargs='*',
        default=[],
        help="List of repositories to remove from the raw events."
    )
    parser.add_argument(
        '--orgs-to-remove',
        nargs='*',
        default=[],
        help="List of organizations to remove from the raw events."
    )
    parser.add_argument(
        '--disable-progress-bar',
        action='store_false',
        dest='progress_bar',
        help="Disable the progress bar display."
    )
    parser.add_argument(
        '--custom-action-mapping',
        default=None,
        help='Path to a custom event to action mapping JSON file.'
    )
    parser.add_argument(
        '--custom-activity-mapping',
        default=None,
        help='Path to a custom action to activity mapping JSON file.'
    )
    args = parser.parse_args()

    try:
        # Step 0: Event Preprocessing
        print("Step 0: Preprocessing events...")
        processor = EventProcessor()
        events = processor.process(
            args.raw_events,
            args.actors_to_remove,
            args.repos_to_remove,
            args.orgs_to_remove
        )

        # Step 1: Event to Action Mapping
        if args.custom_action_mapping:
            event_to_action_file = args.custom_action_mapping
        else:
            event_to_action_file = files("ghmap").joinpath("config", "event_to_action.json")
        action_mapping = load_json_file(event_to_action_file)
        action_mapper = ActionMapper(action_mapping, progress_bar=args.progress_bar)
        actions = action_mapper.map(events)
        save_to_jsonl_file(actions, args.output_actions)
        print(f"Step 1 completed. Actions saved to: {args.output_actions}")

        # Step 2: Action to Activity Mapping
        if args.custom_activity_mapping:
            action_to_activity_file = args.custom_activity_mapping
        else:
            action_to_activity_file = files("ghmap").joinpath("config", "action_to_activity.json")
        activity_mapping = load_json_file(action_to_activity_file)
        activity_mapper = ActivityMapper(activity_mapping, progress_bar=args.progress_bar)
        activities = activity_mapper.map(actions)
        save_to_jsonl_file(activities, args.output_activities)
        print(f"Step 2 completed. Activities saved to: {args.output_activities}")

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
