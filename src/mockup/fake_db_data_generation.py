#!/usr/bin/env python3
######################################################################
# Authors:  David Anthony Parham

# Module Description: This script contains the logic for certain
# database related operations, such as the creation, population
# of retrieval of table data.
######################################################################

from database.schema import Base, Order, OrderSet, Piece, Set, SetPiece
from faker import Faker
from sqlalchemy import func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

fake = Faker()


def create_tables(engine: Engine) -> None:
    """Create all tables defined in the SQLAlchemy Base.

    :param engine: SQLAlchemy engine object
    """
    Base.metadata.create_all(engine)


def populate_tables(engine: Engine, num_records: int = 10) -> None:
    """Populate tables with dummy data.

    :param engine: SQLAlchemy engine object
    :param num_records: Number of records to generate for each table
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Generate dummy data for orders
        orders = [
            Order(date=fake.date_this_year(), total_sets=fake.random_int(min=1, max=5)) for _ in range(num_records)
        ]
        session.add_all(orders)
        session.commit()

        # Generate dummy data for sets
        sets = [
            Set(
                name=fake.company(),
                theme=fake.word(),
                year_released=fake.random_int(min=2000, max=2023),
                piece_count=fake.random_int(min=50, max=100),
            )
            for _ in range(num_records)
        ]
        session.add_all(sets)
        session.commit()

        # Generate dummy data for pieces
        pieces = [
            Piece(name=fake.word(), color=fake.color_name(), dimension=fake.word(), pattern=fake.word())
            for _ in range(num_records)
        ]
        session.add_all(pieces)
        session.commit()

        # Generate dummy data for order sets
        order_sets = [
            OrderSet(order_id=order.id, set_id=set_.id, quantity=fake.random_int(min=1, max=3))
            for order in orders
            for set_ in sets
        ]
        session.add_all(order_sets)
        session.commit()

        # Generate dummy data for set pieces
        set_pieces = [
            SetPiece(set_id=set_.id, piece_id=piece.id, quantity=fake.random_int(min=5, max=20))
            for set_ in sets
            for piece in pieces
        ]
        session.add_all(set_pieces)
        session.commit()

        print("Tables populated successfully!")

    except Exception as e:
        print(f"Error populating tables: {e!s}")
        session.rollback()

    finally:
        session.close()


def fetch_order_info(engine: Engine) -> None:
    """Retrieve total count of each piece across all orders.

    :param engine: SQLAlchemy engine object
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        total_counts = (
            session.query(Piece.id, Piece.name, func.sum(SetPiece.quantity * OrderSet.quantity).label("total_quantity"))
            .join(SetPiece, Piece.id == SetPiece.piece_id)
            .join(Set, SetPiece.set_id == Set.id)
            .join(OrderSet, Set.id == OrderSet.set_id)
            .group_by(Piece.id, Piece.name)
            .all()
        )

        for count in total_counts:
            print(f"Piece ID: {count.id}, Piece Name: {count.name}, Total Quantity: {count.total_quantity}")

    except Exception as e:
        print(f"Error retrieving order info: {e!s}")

    finally:
        session.close()
