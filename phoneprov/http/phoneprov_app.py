from flask import Flask, request, render_template, make_response, redirect, url_for
from flask_cors import CORS
from ..db import get_session
from ..config import Config

APP_NAME = 'phoneprov'
APP_URL_PREFIX = '/phoneprov'
API_URL_PREFIX = APP_URL_PREFIX + '/api'


sqla = get_session(echo=False)
app = Flask(__name__, static_url_path=APP_URL_PREFIX + '/static')
app.secret_key = 'asdfaerwasdf'
app.config['SECRET_KEY'] = 'afe8e8fea04aa810f0df68655bf5b51574d8359e6c343431'
app.config['APP_NAME'] = APP_NAME
app.config['PHONEPROV_CONFIG'] = Config()

# Flask-CORS
cors = CORS(app, resources={
    API_URL_PREFIX + "/*": {"origins": "*"}
})

#####
#
# View Endpoints Here
#
#####

@app.route(APP_URL_PREFIX + "/cisco/authenticate")
def cisco_authenticate():
    return "AUTHORIZED"

@app.route(APP_URL_PREFIX + "/cisco/directories")
def cisco_directories():

    resp = make_response()
    resp.mimetype = 'text/xml'
    resp.headers['Expires'] = "-1"

    device = request.args.get('device', '');

    resp_xml = """<?xml version="1.0"?>
<CiscoIPPhoneMenu>
  <Title>Call History/Directories</Title>
  <Prompt></Prompt>
  <MenuItem>
   <Name>Local Directory</Name>
   <URL>{local_directory_url}</URL>
  </MenuItem>
 <MenuItem>
   <Name>Corporate Directory</Name>
   <URL>{corporate_directory_url}</URL>
  </MenuItem>
  <MenuItem>
   <Name>Personal Directory</Name>
   <URL>{personal_directory_url}</URL>
  </MenuItem>
</CiscoIPPhoneMenu>""".format(
        local_directory_url=url_for("cisco_directories_location", location="10.160.220.5", _external=True),
        corporate_directory_url=url_for("cisco_directories_location", location="corporate", _external=True),
        personal_directory_url=url_for("cisco_directories_personal", device=device, _external=True)
    )

    resp.set_data(resp_xml)
    return resp

@app.route(APP_URL_PREFIX + "/cisco/directories/<location>")
def cisco_directories_location(location):
    from sqlalchemy import create_engine, event
    from sqlalchemy.pool import QueuePool

    resp = make_response()
    resp.mimetype = 'text/xml'
    resp.headers['Expires'] = "-1"

    lastname = request.args.get('lastname', None)
    resp_xml = ''

    if not lastname:
        resp_xml = """<CiscoIPPhoneInput>
  <Title>Directory Search</Title>
  <Prompt>Use the letters on your keypad</Prompt>
  <URL>{local_directory_url}</URL>
  <InputItem>
   <DisplayName>First 3 letters of Last Name</DisplayName>
   <QueryStringParam>lastname</QueryStringParam>
   <DefaultValue></DefaultValue>
   <InputFlags>N</InputFlags>
  </InputItem>
</CiscoIPPhoneInput>""".format(
          local_directory_url=url_for("cisco_directories_location", location=location, _external=True)
        )

    else:
        sqla_url = "mysql://engineering:timeout@npg-asterisk-app.npgco.com/realtime_asterisk"

        e = create_engine(sqla_url, echo=False, pool_recycle=1800, poolclass=QueuePool, pool_size=10, max_overflow=25)
        with e.connect() as conn:
            if location == 'corporate':
                rs = conn.execute("SELECT mailbox, lastname, firstname, location FROM view_directory WHERE lastname_key='{lastname}' ORDER BY lastname, firstname".format(lastname=lastname))
            else:
                rs = conn.execute("SELECT mailbox, lastname, firstname, location FROM view_directory WHERE lastname_key='{lastname}' AND location='{location}' ORDER BY lastname, firstname".format(lastname=lastname, location=location))

            if rs.rowcount:
                resp_xml += """<CiscoIPPhoneDirectory><Title>Corporate Directory</Title><Prompt></Prompt>"""
                for row in rs:
                    resp_xml += """<DirectoryEntry><Name>{last_name}, {first_name}</Name><Telephone>{mailbox}</Telephone></DirectoryEntry>""".format(
                            last_name = row[1], first_name=row[2], mailbox=row[0] )
                resp_xml += """</CiscoIPPhoneDirectory>"""

    resp.set_data(resp_xml)
    return resp

@app.route(APP_URL_PREFIX + "/cisco/directories/personal/<device>")
def cisco_directories_personal(device):
    return ""
