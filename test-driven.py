import re
import unittest
from datetime import datetime


def clean_email_data(raw_data):
    """
    Cleans raw staff data strings and returns a list of structured dictionaries.
    """
    cleaned = []

    for entry in raw_data:
        parts = [p.strip() for p in entry.split(", ")]
        email, birth_date, start_date, title = parts[0], parts[1], parts[2], parts[3]

        # Clean email
        email = email.lower()
        email = email.replace("#", "@")
        email = re.sub(r"@+", "@", email)
        email = re.sub(r"\.+", ".", email)

        # Clean title – strip trailing special characters
        title = re.sub(r"[^a-zA-Z0-9\s]+$", "", title)

        cleaned.append({
            "email": email,
            "birth_date": birth_date,
            "start_date": start_date,
            "title": title,
        })

    return cleaned


def generate_messages(structured_data, today):
    """
    Generates birthday and work anniversary messages for staff whose
    dates match today's month and day.
    """
    messages = []

    for person in structured_data:
        # Derive display name from the email local part
        local_part = person["email"].split("@")[0]
        name = " ".join(
            word.capitalize() for word in local_part.replace("_", ".").split(".")
        )

        birth_date = datetime.strptime(person["birth_date"], "%Y-%m-%d")
        start_date = datetime.strptime(person["start_date"], "%Y-%m-%d")

        # Birthday check
        if birth_date.month == today.month and birth_date.day == today.day:
            messages.append(f"Happy Birthday, {name}! Have a fantastic day!")

        # Work anniversary check
        if start_date.month == today.month and start_date.day == today.day:
            years = today.year - start_date.year
            messages.append(
                f"Happy Work Anniversary, {name}! {years} years at the company!"
            )

    return messages


# ─── Test Suite ───────────────────────────────────────────────────────────────

class TestStaffDataProcessing(unittest.TestCase):

    def test_clean_email_data(self):
        raw_data = [
            "john.doe@company..com, 1985-07-23, 2015-06-15, Software Engineer!!",
            "JANE_DOE@@company.com, 1990-12-05, 2018-09-01, Senior Manager**",
            "BOB.SMITH#company.com, 1975-04-17, 2000-03-12, CTO@@",
        ]
        expected_cleaned_data = [
            {"email": "john.doe@company.com", "birth_date": "1985-07-23",
             "start_date": "2015-06-15", "title": "Software Engineer"},
            {"email": "jane_doe@company.com", "birth_date": "1990-12-05",
             "start_date": "2018-09-01", "title": "Senior Manager"},
            {"email": "bob.smith@company.com", "birth_date": "1975-04-17",
             "start_date": "2000-03-12", "title": "CTO"},
        ]

        cleaned_data = clean_email_data(raw_data)
        self.assertEqual(cleaned_data, expected_cleaned_data)

    def test_generate_messages(self):
        structured_data = [
            {"email": "john.doe@company.com", "birth_date": "1985-07-23",
             "start_date": "2015-07-23", "title": "Software Engineer"},
            {"email": "jane_doe@company.com", "birth_date": "1990-12-05",
             "start_date": "2018-09-01", "title": "Senior Manager"},
            {"email": "bob.smith@company.com", "birth_date": "1975-04-17",
             "start_date": "2000-03-12", "title": "CTO"},
        ]
        today = datetime(2025, 7, 23)
        expected_messages = [
            "Happy Birthday, John Doe! Have a fantastic day!",
            "Happy Work Anniversary, John Doe! 10 years at the company!",
        ]

        messages = generate_messages(structured_data, today)

        for msg in expected_messages:
            self.assertIn(msg, messages)

    def test_no_messages_for_non_matching_dates(self):
        structured_data = [
            {"email": "john.doe@company.com", "birth_date": "1985-07-23",
             "start_date": "2015-06-15", "title": "Software Engineer"},
            {"email": "jane_doe@company.com", "birth_date": "1990-12-05",
             "start_date": "2018-09-01", "title": "Senior Manager"},
            {"email": "bob.smith@company.com", "birth_date": "1975-04-17",
             "start_date": "2000-03-12", "title": "CTO"},
        ]
        today = datetime(2025, 8, 15)
        messages = generate_messages(structured_data, today)
        self.assertEqual(messages, [])


if __name__ == "__main__":
    unittest.main()