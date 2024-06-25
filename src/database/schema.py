#!/usr/bin/env python3
######################################################################
# Author: David Anthony Parham

# Module Description: This script contains the schema for the database
# designed to store the order history of all Lego sets and brick pieces
# used at a Lego Play Day Event.
######################################################################

from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeMeta

Base: "DeclarativeMeta" = declarative_base()


class Order(Base):
    """Represents a order history in the database."""

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, name="order_id")
    date = Column(Date, nullable=False, name="order_date")
    total_sets = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    order_sets = relationship("OrderSet", back_populates="order")


class Set(Base):
    """Represents a LEGO set."""

    __tablename__ = "sets"
    id = Column(Integer, primary_key=True, name="set_id")
    name = Column(String, nullable=False, name="set_name")
    theme = Column(String)
    year_released = Column(Integer)
    piece_count = Column(Integer)
    order_sets = relationship("OrderSet", back_populates="set")
    set_pieces = relationship("SetPiece", back_populates="set")


class Piece(Base):
    """Represents a single LEGO brick."""

    __tablename__ = "pieces"
    id = Column(Integer, primary_key=True, name="piece_id")
    name = Column(String, nullable=False, name="piece_name")
    color = Column(String, nullable=False)
    dimension = Column(String)
    pattern = Column(String)
    set_pieces = relationship("SetPiece", back_populates="piece")


class OrderSet(Base):
    """Represents a relationship between an order and a set in the database."""

    __tablename__ = "order_sets"
    id = Column(Integer, primary_key=True, name="order_set_id")
    order_id = Column(Integer, ForeignKey("orders.order_id"), index=True)
    set_id = Column(Integer, ForeignKey("sets.set_id"), index=True)
    quantity = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="order_sets")
    set = relationship("Set", back_populates="order_sets")


class SetPiece(Base):
    """Represents a relationship between a set and a piece (brick) in the database."""

    __tablename__ = "set_pieces"
    id = Column(Integer, primary_key=True, name="set_piece_id")
    set_id = Column(Integer, ForeignKey("sets.set_id"), index=True)
    piece_id = Column(Integer, ForeignKey("pieces.piece_id"), index=True)
    quantity = Column(Integer, nullable=False)
    set = relationship("Set", back_populates="set_pieces")
    piece = relationship("Piece", back_populates="set_pieces")
