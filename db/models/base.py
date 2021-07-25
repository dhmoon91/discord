import datetime
from sqlalchemy import Column, Integer, DateTime
from ..db import Session, Base

session = Session()


class BaseMixin(Base):
    """Base model"""

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    def create(self, orig_session=session, commit=True):
        """Create a row in table
        orig_session will be defaulted to session.
        """
        orig_session.add(self)
        if commit:
            try:
                orig_session.commit()
            except Exception as e_values:
                orig_session.rollback()
                raise e_values
            finally:
                orig_session.close()

    def delete(self, orig_session=session, commit=True):
        """
        Delete a row in table

        We need to use the orig_session, the session passed into this function,
        since the session to query 'to delete' row will still be opened.
        """
        orig_session.delete(self)
        if commit:
            try:
                orig_session.commit()
            except Exception as e_values:
                orig_session.rollback()
                raise e_values
            finally:
                orig_session.close()

    # TODO: Not working figure out why
    def update(self, orig_session=session, commit=True):
        """
        Update a row in table
        NOT USED ATM.
        """
        orig_session.add(self)
        if commit:
            try:
                orig_session.commit()
            except Exception as e_values:
                orig_session.rollback()
                raise e_values
            finally:
                orig_session.close()
