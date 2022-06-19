from typing import Union

from sqlalchemy import Column, String, DateTime, Float, PickleType

from src.data import Base
from src.domain.models import Brand, Influencer
from src.types import ObjectMapperAdapter


class SqlAlchemyBaseEntity:
    id = Column(String(length=36), primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False)


class SqlAlchemyBaseUserEntity(SqlAlchemyBaseEntity):
    auth_user_id = Column(type_=String(length=64), nullable=False, unique=True)


class SqlAlchemyBrandEntity(Base, SqlAlchemyBaseUserEntity):
    __tablename__ = 'brand'

    brand_name = Column(type_=String(length=120), nullable=False)
    brand_description = Column(type_=String(length=500), nullable=False)
    header_image = Column(type_=String(length=360), nullable=True)
    values = Column(type_=PickleType, nullable=False)
    categories = Column(type_=PickleType, nullable=False)
    insta_handle = Column(type_=String(length=30), nullable=True)
    website = Column(type_=String(length=120), nullable=False)
    logo = Column(type_=String(length=360), nullable=True)


class SqlAlchemyInfluencerEntity(Base, SqlAlchemyBaseUserEntity):
    __tablename__ = 'influencer'

    website = Column(type_=String(length=120), nullable=False)
    bio = Column(type_=String(length=500), nullable=False)
    image = Column(type_=String(length=360), nullable=True)
    audience_age_13_to_17_split = Column(type_=Float, nullable=True)
    audience_age_18_to_24_split = Column(type_=Float, nullable=True)
    audience_age_25_to_34_split = Column(type_=Float, nullable=True)
    audience_age_35_to_44_split = Column(type_=Float, nullable=True)
    audience_age_45_to_54_split = Column(type_=Float, nullable=True)
    audience_age_55_to_64_split = Column(type_=Float, nullable=True)
    audience_age_65_plus_split = Column(type_=Float, nullable=True)
    audience_male_split = Column(type_=Float, nullable=True)
    audience_female_split = Column(type_=Float, nullable=True)
    insta_handle = Column(type_=String(length=30), nullable=True)
    values = Column(type_=PickleType, nullable=False)
    categories = Column(type_=PickleType, nullable=False)


def create_mappings(mapper: Union[ObjectMapperAdapter, object]):
    mapper.create_map(Brand, SqlAlchemyBrandEntity)
    mapper.create_map(SqlAlchemyBrandEntity, Brand)
    mapper.create_map(Influencer, SqlAlchemyInfluencerEntity)
    mapper.create_map(SqlAlchemyInfluencerEntity, Influencer)
