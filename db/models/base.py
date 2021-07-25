from sqlalchemy import Column, Integer, DateTime
import datetime
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

    def create(self, sessionOrig=session, commit=True):
        """Create a row in table
        sessionOrig will be defaulted to session.
        """
        sessionOrig.add(self)
        if commit:
            try:
                sessionOrig.commit()
            except Exception as e_values:
                sessionOrig.rollback()
                raise e_values
            finally:
                sessionOrig.close()

    def delete(self, sessionOrig=session, commit=True):
        """
        Delete a row in table

        We need to use the session passed in
        since the session to query 'to delete' row will still be opened.
        """
        sessionOrig.delete(self)
        if commit:
            try:
                sessionOrig.commit()
            except Exception as e_values:
                sessionOrig.rollback()
                raise e_values
            finally:
                sessionOrig.close()

    # TODO: Not working figure out why
    def update(self, sessionOrig=session, commit=True):
        if commit:
            try:
                sessionOrig.commit()
            except Exception as e_values:
                sessionOrig.rollback()
                raise e_values
            finally:
                sessionOrig.close()
