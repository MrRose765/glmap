import argparse
import os
import tempfile
from importlib.resources import files
from ghmap.preprocess.event_processor import EventProcessor
from ghmap.mapping.action_mapper import ActionMapper
from ghmap.mapping.activity_mapper import ActivityMapper
from ghmap.utils import load_json_file, save_to_jsonl_file, load_jsonl_file


def main():
    parser = argparse.ArgumentParser(description="Process GitHub events into structured activities.")
    parser.add_argument('--raw-events', required=True, help="Path to the folder containing raw events.")
    parser.add_argument('--output-actions', required=True, help="Path to the output file for mapped actions.")
    parser.add_argument('--output-activities', required=True, help="Path to the output file for mapped activities.")
    parser.add_argument('--orgs-to-remove', nargs='*', default=[], help="List of organizations to remove from the raw events.")
    args = parser.parse_args()

    # Use tempfile to create a temporary directory for processed events
    with tempfile.TemporaryDirectory() as processed_folder:
        event_to_action_mapping_file = files("ghmap").joinpath("config", "event_to_action.json")
        action_to_activity_mapping_file = files("ghmap").joinpath("config", "action_to_activity.json")

        try:
            # Step 0: Event Preprocessing
            print("Step 0: Preprocessing events...")
            processor = EventProcessor(args.orgs_to_remove, args.raw_events, processed_folder)
            processor.process()

            # Step 1: Event to Action Mapping
            action_mapping = load_json_file(event_to_action_mapping_file)
            action_mapper = ActionMapper(action_mapping)

            processed_event_files = sorted(
                [os.path.join(processed_folder, f) for f in os.listdir(processed_folder) if f.endswith('.json')]
            )
            all_mapped_actions = []
            for event_file in processed_event_files:
                event_records = load_json_file(event_file)
                mapped_actions = [action_mapper.map(event) for event in event_records]
                all_mapped_actions.extend(mapped_actions)

            save_to_jsonl_file(all_mapped_actions, args.output_actions)
            print(f"Step 1 completed. Actions saved to: {args.output_actions}")

            # Step 2: Actions to Activities
            actions = load_jsonl_file(args.output_actions)
            activity_mapping = load_json_file(action_to_activity_mapping_file)
            activity_mapper = ActivityMapper(actions, activity_mapping)

            activities = activity_mapper.map()
            save_to_jsonl_file(activities, args.output_activities)
            print(f"Step 2 completed. Activities saved to: {args.output_activities}")

        except Exception as e:
            print(f"An error occurred: {e}")

        # No need for manual cleanup, tempfile will handle it

if __name__ == '__main__':
    main()