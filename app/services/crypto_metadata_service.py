from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID

from app.models.metadata_models import CryptoMetadata
from app.core.logging_config import logger


class CryptoMetadataService:
    """
    Service layer responsible for all business logic related to CryptoMetadata.
    It abstracts direct DB access from the API layer, enabling clean separation of concerns.
    """

    @staticmethod
    def create_crypto_metadata(db: Session, metadata_data: dict) -> CryptoMetadata:
        """
        Create a new CryptoMetadata record. If one already exists with the same symbol,
        it will be backed up (e.g., printed/stored/logged) and replaced.
        """
        try:
            existing = db.query(CryptoMetadata).filter(
                CryptoMetadata.crypto_symbol == metadata_data["crypto_symbol"]
            ).first()

            if existing:
                logger.info(f"[REPLACE] Existing entry for {existing.crypto_symbol} found. Backing up and deleting.")
                # Here you could store to file, archive table, or just log
                logger.info(f"Backup: {existing.__dict__}")
                db.delete(existing)
                db.commit()  # Commit the deletion before insert

            new_metadata = CryptoMetadata(**metadata_data)
            db.add(new_metadata)
            db.commit()
            db.refresh(new_metadata)

            logger.info(f"[CREATE] New metadata for {new_metadata.crypto_symbol} created.")
            return new_metadata

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"[ERROR][CREATE] Failed to create or replace metadata: {e}")
            raise

    @staticmethod
    def get_all_crypto_metadata(db: Session) -> list[CryptoMetadata]:
        """
        Retrieve all CryptoMetadata records.

        Args:
            db (Session): SQLAlchemy session.

        Returns:
            List of CryptoMetadata instances.
        """
        return db.query(CryptoMetadata).all()

    @staticmethod
    def get_crypto_metadata_by_id(db: Session, metadata_id: UUID) -> CryptoMetadata | None:
        """
        Retrieve a single CryptoMetadata record by its UUID.

        Args:
            db (Session): SQLAlchemy session.
            metadata_id (UUID): The unique identifier of the record.

        Returns:
            CryptoMetadata if found, else None.
        """
        return db.query(CryptoMetadata).filter(
            CryptoMetadata.crypto_metadata_id == metadata_id
        ).first()

    @staticmethod
    def update_crypto_metadata(db: Session, metadata_id: UUID, update_data: dict) -> CryptoMetadata | None:
        """
        Update an existing CryptoMetadata record by ID.

        Args:
            db (Session): SQLAlchemy session.
            metadata_id (UUID): Unique identifier of the record to update.
            update_data (dict): Fields to update.

        Returns:
            Updated CryptoMetadata if successful, else None.
        """
        metadata = db.query(CryptoMetadata).filter(
            CryptoMetadata.crypto_metadata_id == metadata_id
        ).first()

        if not metadata:
            logger.warning(f"[UPDATE] No record found with ID: {metadata_id}")
            return None

        for key, value in update_data.items():
            setattr(metadata, key, value)

        try:
            db.commit()
            db.refresh(metadata)
            logger.info(f"[UPDATE] CryptoMetadata '{metadata.crypto_symbol}' updated successfully.")
            return metadata

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"[ERROR][UPDATE] Failed to update CryptoMetadata: {e}")
            raise

    @staticmethod
    def delete_crypto_metadata(db: Session, metadata_id: UUID) -> bool:
        """
        Delete a CryptoMetadata record by ID.

        Args:
            db (Session): SQLAlchemy session.
            metadata_id (UUID): Unique identifier of the record to delete.

        Returns:
            True if deletion was successful, False if record not found.
        """
        metadata = db.query(CryptoMetadata).filter(
            CryptoMetadata.crypto_metadata_id == metadata_id
        ).first()

        if not metadata:
            logger.warning(f"[DELETE] No record found with ID: {metadata_id}")
            return False

        try:
            db.delete(metadata)
            db.commit()
            logger.info(f"[DELETE] CryptoMetadata '{metadata.crypto_symbol}' deleted successfully.")
            return True

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"[ERROR][DELETE] Failed to delete CryptoMetadata: {e}")
            raise
