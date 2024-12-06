import json
import os
from datetime import datetime, timedelta
from typing import List, Dict
from tqdm import tqdm

class EventProcessor:
    """
    A class to process GitHub events, removing unwanted events and filtering redundant review events.

    Attributes:
        orgs_to_remove (List[str]): List of organizations to exclude from the raw events.
        input_folder (str): Path to the folder containing raw events.
        output_folder (str): Path to the folder where processed events will be saved.
        processed_ids (set): Set of event IDs that have been processed.
        pending_events (List[Dict]): Stores events pending processing across files.
    """

    def __init__(self, orgs_to_remove: List[str], input_folder: str, output_folder: str):
        self.orgs_to_remove = orgs_to_remove
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.processed_ids = set()  # Track event IDs across all files
        self.pending_events = []    # Store end-of-file events for cross-file checks

    @staticmethod
    def _parse_time(timestamp: str | int) -> datetime:
        """
        Converts a Unix timestamp (in milliseconds) or an ISO 8601 string to a datetime object.
        """
        if isinstance(timestamp, str):
            return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        
        elif isinstance(timestamp, int):
            return datetime.utcfromtimestamp(timestamp / 1000)

    @staticmethod
    def _calculate_time_diff(start: datetime, end: datetime) -> float:
        """
        Calculates the difference in seconds between two datetime objects.
        """
        return (end - start).total_seconds()

    @staticmethod
    def _is_within_time_window(event1: Dict, event2: Dict, window: int = 2) -> bool:
        """
        Checks if event2 is within a specified time window (in seconds) of event1.
        """
        time_diff = abs(EventProcessor._calculate_time_diff(
            EventProcessor._parse_time(event1['created_at']),
            EventProcessor._parse_time(event2['created_at'])
        ))
        return time_diff <= window

    def _should_keep_event(self, current_event: Dict, events: List[Dict], index: int) -> bool:
        """
        Determines whether the current event should be kept based on redundant review checks.
        """
        actor_id = current_event['actor']['id']
        repo_id = current_event['repo']['id']

        # Check preceding events for redundant comments
        for j in range(index - 1, -1, -1):
            if not self._is_within_time_window(current_event, events[j]):
                break
            if events[j]['type'] == "PullRequestReviewCommentEvent" and \
               events[j]['actor']['id'] == actor_id and events[j]['repo']['id'] == repo_id:
                return False

        # Check following events for redundant comments
        for j in range(index + 1, len(events)):
            if not self._is_within_time_window(current_event, events[j]):
                break
            if events[j]['type'] == "PullRequestReviewCommentEvent" and \
               events[j]['actor']['id'] == actor_id and events[j]['repo']['id'] == repo_id:
                return False

        return True

    def _filter_redundant_review_events(self, events: List[Dict]) -> List[Dict]:
        """
        Filters out redundant PullRequestReviewEvent events.
        """
        filtered_events = []
        combined_events = self.pending_events + events  # Include end-of-file events from previous file
        self.pending_events = combined_events[-3:]      # Store the last 3 events for next file processing

        for i, event in enumerate(combined_events):
            if event['type'] == "PullRequestReviewEvent" and event['id'] not in self.processed_ids:
                if self._should_keep_event(event, combined_events, i):
                    if not (filtered_events and 
                            filtered_events[-1]['type'] == "PullRequestReviewEvent" and 
                            filtered_events[-1]['actor']['id'] == event['actor']['id'] and 
                            filtered_events[-1]['repo']['id'] == event['repo']['id'] and
                            self._is_within_time_window(filtered_events[-1], event)):
                        filtered_events.append(event)
                        self.processed_ids.add(event['id'])
            elif event['type'] != "PullRequestReviewEvent" and event['id'] not in self.processed_ids:
                # Keep non-PullRequestReviewEvent events
                filtered_events.append(event)
                self.processed_ids.add(event['id'])

        return filtered_events

    def _remove_unwanted_orgs(self, events: List[Dict]) -> List[Dict]:
        """
        Filters out events belonging to unwanted organizations.
        """
        return [event for event in events if event.get('org', {}).get('login') not in self.orgs_to_remove]

    def process(self) -> List[Dict]:
        """
        Processes the input folder or a single file, filters events, and returns the processed events.
        """
        all_processed_events = []  # List to store all processed events

        # Check if the input is a directory or a single file
        if os.path.isdir(self.input_folder):
            # Loop over files in the input folder with tqdm
            for filename in tqdm(sorted(os.listdir(self.input_folder)), desc="Processing event files"):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.input_folder, filename)
                    with open(file_path, 'r') as f:
                        events = json.load(f)

                    # Remove events from unwanted organizations
                    events = self._remove_unwanted_orgs(events)

                    # Filter redundant review events
                    events = self._filter_redundant_review_events(events)

                    # Add processed events to the list
                    all_processed_events.extend(events)

        elif os.path.isfile(self.input_folder):
            # Process a single file with tqdm for consistency
            with tqdm(total=1, desc="Processing event file") as pbar:
                with open(self.input_folder, 'r') as f:
                    events = json.load(f)

                # Remove events from unwanted organizations
                events = self._remove_unwanted_orgs(events)

                # Filter redundant review events
                events = self._filter_redundant_review_events(events)

                # Add processed events to the list
                all_processed_events.extend(events)
                pbar.update(1)

        return all_processed_events