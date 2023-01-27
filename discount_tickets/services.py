from .models import DiscountTicket


def save_ticket(*, ticket: DiscountTicket, user_id: int):
    ticket.saved_users.add(user_id)
