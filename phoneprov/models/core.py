from ..db import sqla_base, Session, schema_name
from sqlalchemy import Table, Column, String, Integer, BigInteger, Numeric, ForeignKey, Boolean, Text, Date, UniqueConstraint, event, or_
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.session import object_session
from sqlalchemy_utils import Timestamp, ArrowType, EmailType, PasswordType, PhoneNumberType, force_auto_coercion
from sqlalchemy.sql import case

force_auto_coercion()
line_type_enum = ENUM(*('sipreg', 'blf', 'sccpreg', 'hotdesk', 'sccpservice','sccpfeature','sccpempty'), name='lineType')
protocol_enum = ENUM(*('sip', 'sccp'), name='protocol')

class PhoneType( sqla_base, Timestamp ):

    __hash_fields__ = []

    __tablename__ = 'phoneprov_types'
    __table_args__ = (
        { 'schema': schema_name }
    )

    model = Column( 'model', String(45), primary_key=True )
    protocol = Column( protocol_enum, index=True )
    max_lines = Column( 'maxLines', Integer )
    _template = Column( 'template', Text )

    phones = relationship( 'Phone', back_populates='model' )

    @hybrid_property
    def template(self):
        return self._template

class Phone( sqla_base, Timestamp ):

    __hash_fields__ = []

    __tablename__ = 'phoneprov_phone'
    __table_args__ = (
        { 'schema': schema_name }
    )

    mac_address = Column( 'macaddress', String(12), primary_key=True )
    model_id = Column( 'type', String(45), ForeignKey('public.phoneprov_types.model') )
    _template = Column( 'template', Text )
    phone_label = Column( 'phoneLabel', String(45) )
    softkey_set = Column( 'softKeyset', String(30) )
    comments = Column( 'comments', Text )
    paging_zone = Column( 'pagingZone', Text )
    background_image = Column( 'backgroundimage', String(250) )
    model = relationship( 'PhoneType', back_populates='phones' )

    lines = relationship( 'PhoneLine', back_populates='phone' )

    @hybrid_property
    def template(self):
        if self._template is None and self.model:
            return self.model.template

        return self._template

class PhoneLine( sqla_base, Timestamp ):

    __hash_fields__ = []

    __tablename__ = 'phoneprov_line'
    __table_args__ = (
        UniqueConstraint('macaddress', 'lineIndex', name='uix_1'),
        { 'schema': schema_name },
    )

    mac_address = Column( 'macaddress', String(12), ForeignKey('public.phoneprov_phone.macaddress'), primary_key=True )
    line_index = Column( 'lineIndex', Integer )
    line_type = Column( line_type_enum, index=True )
    sip_identity = Column( 'sipIdentity', String(45), index=True )
    line_label = Column( 'lineLabel', String(45), index=True )
    extension = Column( 'extension', String(45), index=True )
    callerid_name = Column( 'callerIDName', String(45), index=True )
    mailbox = Column( 'mailbox', String(45), index=True )
    external_cid = Column( 'externalCID', String(10), index=True )
    blf_target = Column( 'blfTarget', String(255), index=True )
    intercom = Column( 'intercom', String(3), index=True )
    callgroup = Column( 'callgroup', String(45), index=True )
    pickupgroup = Column( 'pickupgroup', String(45), index=True )
    emergency_cid = Column( '911CID', String(10), index=True )

    phone = relationship( "Phone", back_populates='lines' )
