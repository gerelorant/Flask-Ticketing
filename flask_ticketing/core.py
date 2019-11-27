from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_ticketing.model import TicketTypeMixin, TicketMixin


class Ticketing(object):
    """Flask-Ticketing extension class.

    :param app: Flask application instance
    :param db: Flask-SQLAlchemy instance

    """
    def __init__(
            self,
            app: Flask,
            db: SQLAlchemy,
            ticket_type_class: type(TicketTypeMixin) = None,
            ticket_class: type(TicketMixin) = None
    ):
        self.app = app
        self.db = db

        self.ticket_type_class = ticket_type_class
        self.ticket_class = ticket_class

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        self.app.extensions["ticketing"] = self

        if self.ticket_type_class is None:
            class TicketType(self.db.Model, TicketTypeMixin):
                __tablename__ = "ticket_type"

            self.ticket_type_class = TicketType

        if self.ticket_class is None:
            class Ticket(self.db.Model, TicketMixin):
                __tablename__ = "ticket"

            self.ticket_class = Ticket
