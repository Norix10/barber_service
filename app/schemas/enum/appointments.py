import enum

class AppointmentsEnum(enum.Enum):
    pending = "pending"
    verified = "verified"
    cancelled = "cancelled"
    completed = "completed"

    