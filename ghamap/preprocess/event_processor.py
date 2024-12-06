import json
import os
from datetime import datetime, timedelta

class EventProcessor:
    def __init__(self, orgs_to_remove, input_folder, output_folder):
        self.orgs_to_remove = orgs_to_remove
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.processed_ids = set()  # Track event IDs across all files
        self.pending_events = []     # Store end-of-file events for cross-file checks

    def parse_time(self, timestamp):
        """Converts Unix timestamp (in milliseconds) to a datetime object."""
        return datetime.fromtimestamp(timestamp / 1000)

    def calculate_time_diff(self, start, end):
        """Calculates the difference in seconds between two datetime objects."""
        return (end - start).total_seconds()

    def is_within_2s_window(self, event1, event2):
        """Checks if event2 is within a 2-second window of event1."""
        time_diff = abs(self.calculate_time_diff(
            self.parse_time(event1['created_at']),
            self.parse_time(event2['created_at'])
        ))
        return time_diff <= 2

    def should_keep_event(self, current_event, events, index):
        actor_id = current_event['actor']['id']
        repo_id = current_event['repo']['id']

        # Check preceding events for redundant comments
        for j in range(index - 1, -1, -1):
            if not self.is_within_2s_window(current_event, events[j]):
                break
            if events[j]['type'] == "PullRequestReviewCommentEvent" and \
               events[j]['actor']['id'] == actor_id and events[j]['repo']['id'] == repo_id:
                return False

        # Check following events for redundant comments
        for j in range(index + 1, len(events)):
            if not self.is_within_2s_window(current_event, events[j]):
                break
            if events[j]['type'] == "PullRequestReviewCommentEvent" and \
               events[j]['actor']['id'] == actor_id and events[j]['repo']['id'] == repo_id:
                return False

        return True

    def filter_redundant_review_events(self, events):
        """Filters out redundant PullRequestReviewEvent events."""
        filtered_events = []
        combined_events = self.pending_events + events  # Include end-of-file events from previous file
        self.pending_events = combined_events[-3:]      # Store the last 3 events for next file processing

        for i, event in enumerate(combined_events):
            if event['type'] == "PullRequestReviewEvent" and event['id'] not in self.processed_ids:
                if self.should_keep_event(event, combined_events, i):
                    if not (filtered_events and 
                            filtered_events[-1]['type'] == "PullRequestReviewEvent" and 
                            filtered_events[-1]['actor']['id'] == event['actor']['id'] and 
                            filtered_events[-1]['repo']['id'] == event['repo']['id'] and
                            self.is_within_2s_window(filtered_events[-1], event)):
                        filtered_events.append(event)
                        self.processed_ids.add(event['id'])
            elif event['type'] != "PullRequestReviewEvent" and event['id'] not in self.processed_ids:
                # Keep non-PullRequestReviewEvent events
                filtered_events.append(event)
                self.processed_ids.add(event['id'])

        return filtered_events

    def remove_unwanted_orgs(self, events):
        """Filters out events belonging to unwanted organizations."""
        return [event for event in events if event.get('org', {}).get('login') not in self.orgs_to_remove]

    def process_all_files(self):
        """Processes each file in the input folder and writes processed events to separate output files."""
        os.makedirs(self.output_folder, exist_ok=True)  # Ensure output folder exists

        for filename in sorted(os.listdir(self.input_folder)):
            if filename.startswith('gh_events') and filename.endswith('.json'):
                with open(os.path.join(self.input_folder, filename), 'r') as f:
                    events = json.load(f)

                # Remove events from unwanted organizations
                events = self.remove_unwanted_orgs(events)

                # Filter redundant review events
                events = self.filter_redundant_review_events(events)

                # Save processed events to an individual output file
                output_path = os.path.join(self.output_folder, filename)
                with open(output_path, 'w') as out_file:
                    json.dump(events, out_file, indent=2)
                print(f"Processed events saved to {output_path}")