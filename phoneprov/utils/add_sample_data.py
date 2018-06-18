from ..models import *
from ..db import sqla_base, sqla_url, get_session
import sqlalchemy as sa

sqla = get_session()

def add_sample_data():
    ptype = PhoneType()
    sqla.add(ptype)
    ptype.model = "CP-7945SCCP-DEV-Alpha"
    ptype.protocol = "sccp"
    ptype.max_lines = 2
    ptype._template = """<device  xsi:type="axl:XIPPhone">
        <sshUserId>user</sshUserId>
        <sshPassword>pass</sshPassword>
        <devicePool>
                <dateTimeSetting>
                        <timeZone>Central Standard/Daylight Time</timeZone>
                </dateTimeSetting>
                <callManagerGroup>
                        <members>
                                <member  priority="0">
                                        <callManager>
                                                <ports>
                                                        <ethernetPhonePort>2000</ethernetPhonePort>
                                                </ports>
                                                <processNodeName>10.160.220.12</processNodeName>
                                        </callManager>
                                </member>
                                <member  priority="1">
                                        <callManager>
                                                <ports>
                                                        <ethernetPhonePort>2000</ethernetPhonePort>
                                                </ports>
                                                <processNodeName>10.160.220.5</processNodeName>
                                        </callManager>
                                </member>
                        </members>
                </callManagerGroup>

                <srstInfo>
                        <srstOption>Enable</srstOption>
                        <ipAddr1></ipAddr1>
                        <port1>2000</port1>
                        <ipAddr2></ipAddr2>
                        <port2>2000</port2>
                        <ipAddr3></ipAddr3>
                        <port3>2000</port3>
                </srstInfo>
        </devicePool>

        <loadInformation>SCCP45.9-4-2-1S</loadInformation>

        <vendorConfig>
                <ehookEnable>1</ehookEnable>
                <disableSpeaker>false</disableSpeaker>
                <disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
                <forwardingDelay>1</forwardingDelay>
                <pcPort>0</pcPort>
                <settingsAccess>1</settingsAccess>
                <garp>0</garp>
                <voiceVlanAccess>0</voiceVlanAccess>
                <videoCapability>0</videoCapability>
                <autoSelectLineEnable>0</autoSelectLineEnable>/
                <autoCallSelect>0</autoCallSelect>
                <sshAccess>0</sshAccess>
                <webAccess>0</webAccess>
                <daysDisplayNotActive>1,7</daysDisplayNotActive>
                <displayOnTime>07:00</displayOnTime>
                <displayOnDuration>9:00</displayOnDuration>
                <displayIdleTimeout>00:05</displayIdleTimeout>
                <displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
                <g722CodecSupport>2</g722CodecSupport>
        </vendorConfig>

        <commonProfile>
                <callLogBlfEnabled>3</callLogBlfEnabled>
                <backgroundImageAccess>true</backgroundImageAccess>
                <backgroundImageURL>http://10.160.220.5/Desktops/320x212x16/firery.png</backgroundImageURL>
        </commonProfile>

        <versionStamp></versionStamp>
        <userLocale>
                <name></name>
                <uid>1</uid>
                <langCode>en</langCode>
                <version></version>
                <winCharSet>iso-8859-1</winCharSet>
        </userLocale>

        <networkLocale></networkLocale>
        <networkLocaleInfo>
                <name></name>
                <version></version>
        </networkLocaleInfo>
        <phonePersonalization>1</phonePersonalization>
        <singleButtonBarge>1</singleButtonBarge>
        <joinAcrossLines>1</joinAcrossLines>
        <autoCallPickupEnable>false</autoCallPickupEnable>
        <blfAudibleAlertSettingOfIdleStation>1</blfAudibleAlertSettingOfIdleStation>
        <blfAudibleAlertSettingOfBusyStation>1</blfAudibleAlertSettingOfBusyStation>
        <deviceSecurityMode>1</deviceSecurityMode>

        <authenticationURL>{{ config.cisco_authentication_url }}</authenticationURL>
        <directoryURL>{{ config.cisco_directory_url }}</directoryURL>
        <servicesURL>{{ config.cisco_services_url }}</servicesURL>
        <idleURL></idleURL>
        <idleTimeout>60</idleTimeout>
        <informationURL></informationURL>
        <messagesURL></messagesURL>
        <proxyServerURL></proxyServerURL>

        <dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
        <dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
        <dscpForCm2Dvce>96</dscpForCm2Dvce>
        <advertiseG722Codec>1</advertiseG722Codec>
</device>"""

    phone_line = PhoneLine()
    sqla.add(phone_line)
    phone_line.mac_address = '002699EF8C1B'
    phone_line.line_index = 1
    phone_line.line_type = 'sccpreg'
    phone_line.line_label = 'Nathan Ranney - 10012'
    phone_line.extension = '10012'
    phone_line.callerid_name = 'Nathan Ranney'
    phone_line.mailbox = '10012'
    phone_line.external_cid = '8167492812'
    phone_line.emergency_cid = '8166292802'

    phone = Phone()
    sqla.add(phone)
    phone.mac_address = "002699EF8C1B"
    phone.model = ptype
    phone.phone_label = "816-749-2812"
    phone.lines.append(phone_line)
    sqla.commit()

if __name__ == '__main__':
    add_sample_data()

