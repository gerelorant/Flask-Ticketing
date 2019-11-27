import datetime as dt

from flask import render_template
import flask_sqlalchemy as fsa
import pdfkit as pdf
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref


class TicketTypeMixin(fsa.Model):
    name = sa.Column(sa.String(40), nullable=False, index=True)
    description = sa.Column(sa.Text)
    available_from = sa.Column(sa.DateTime, index=True)
    available_until = sa.Column(sa.DateTime, index=True)
    price = sa.Column(sa.Float, nullable=False)
    limit = sa.Column(sa.Integer)
    template = sa.Column(sa.String(40), nullable=False)


class TicketMixin(fsa.Model):
    code = sa.Column(sa.String(40))
    issued = sa.Column(sa.DateTime, default=dt.datetime.utcnow)
    used = sa.Column(sa.DateTime)

    # noinspection PyMethodParameters
    @declared_attr
    def ticket_type_id(cls):
        return sa.Column(
            sa.Integer,
            sa.ForeignKey('ticket_type.id'),
            nullable=False,
            index=True
        )

    # noinspection PyMethodParameters
    @declared_attr
    def ticket_type(cls):
        return relationship(
            'TicketType',
            backref=backref('tickets', lazy='dynamic')
        )

    @property
    def pdf(self):
        ticket_type = getattr(self, 'ticket_type')
        return pdf.from_string(
            render_template(ticket_type.template, ticket=self),
            output_path=False
        )
