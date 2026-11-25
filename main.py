
from datetime import datetime, timedelta
import math

# Smart Parking Fee Management System

# Hourly parking rates
VEHICLE_RATES = {
    "car": 30,
    "bike": 15,
    "bus": 60,
    "truck": 50
}

# Maximum parking fee per calendar day
DAILY_LIMITS = {
    "car": 200,
    "bike": 100,
    "bus": 400,
    "truck": 350
}

OVERNIGHT_CHARGE = 50
LOST_TICKET_PENALTY = 200
LONG_STAY_PENALTY = 300


def get_datetime(message):
    """Accept and validate date and time."""
    while True:
        try:
            value = input(message)
            return datetime.strptime(
                value, "%Y-%m-%d %H:%M"
            )
        except ValueError:
            print("Invalid format! Use YYYY-MM-DD HH:MM.")


def calculate_parking_hours(start, end):
    """Calculate billable hours for each calendar day."""
    daily_hours = {}
    current = start

    while current < end:
        next_day = datetime.combine(
            current.date() + timedelta(days=1),
            datetime.min.time()
        )

        segment_end = min(next_day, end)

        hours = (
            segment_end - current
        ).total_seconds() / 3600

        day = current.date()

        daily_hours[day] = math.ceil(
            daily_hours.get(day, 0) + hours
        )

        current = segment_end

    return daily_hours


def calculate_fee(vehicle, entry, exit_time, lost_ticket):
    """Calculate total parking fee and penalties."""

    rate = VEHICLE_RATES[vehicle]
    daily_limit = DAILY_LIMITS[vehicle]

    daily_hours = calculate_parking_hours(
        entry, exit_time
    )

    total_fee = 0

    print("\n----- PARKING DETAILS -----")

    for day, hours in daily_hours.items():

        daily_fee = hours * rate

        # Apply daily maximum limit
        daily_fee = min(daily_fee, daily_limit)

        total_fee += daily_fee

        print(
            f"{day} | {hours} hours | "
            f"Rs. {daily_fee}"
        )

    # Overnight charge for each crossed midnight
    overnight_days = (
        exit_time.date() - entry.date()
    ).days

    overnight_fee = overnight_days * OVERNIGHT_CHARGE
    total_fee += overnight_fee

    # Calculate total duration
    duration = exit_time - entry
    total_hours = duration.total_seconds() / 3600

    # Apply penalties
    penalty = 0

    if lost_ticket:
        penalty += LOST_TICKET_PENALTY
        print("Lost ticket penalty: Rs. 200")

    if total_hours > 24:
        penalty += LONG_STAY_PENALTY
        print("Long stay penalty: Rs. 300")

    total_fee += penalty

    print("\n----- BILL SUMMARY -----")
    print("Vehicle Type:", vehicle.upper())
    print("Entry Time:", entry)
    print("Exit Time:", exit_time)
    print(f"Total Hours: {total_hours:.2f}")
    print("Overnight Charge: Rs.", overnight_fee)
    print("Penalty: Rs.", penalty)
    print("Total Parking Fee: Rs.", total_fee)


def main():

    print("=" * 45)
    print("     SMART PARKING FEE MANAGEMENT")
    print("=" * 45)

    print("\nVehicle Categories:")
    for vehicle, rate in VEHICLE_RATES.items():
        print(f"{vehicle.title()} - Rs. {rate}/hour")

    # Vehicle validation
    while True:
        vehicle = input(
            "\nEnter vehicle type: "
        ).strip().lower()

        if vehicle in VEHICLE_RATES:
            break

        print("Invalid vehicle category! Try again.")

    # Entry and exit time
    entry = get_datetime(
        "Enter entry date and time (YYYY-MM-DD HH:MM): "
    )

    while True:
        exit_time = get_datetime(
            "Enter exit date and time (YYYY-MM-DD HH:MM): "
        )

        if exit_time > entry:
            break

        print("Exit time must be later than entry time!")

    # Lost ticket validation
    while True:
        ticket = input(
            "Is the parking ticket lost? (yes/no): "
        ).strip().lower()

        if ticket in ["yes", "no"]:
            break

        print("Please enter yes or no.")

    lost_ticket = ticket == "yes"

    # Calculate and display fee
    calculate_fee(
        vehicle,
        entry,
        exit_time,
        lost_ticket
    )


if __name__ == "__main__":
    main()
