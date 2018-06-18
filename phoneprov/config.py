from os import environ
from os.path import expanduser
import simplejson as json

class Config( object ):
    config_defs = [
        {
            "name": "sqla_url",
            "description": "url for sql database",
            "type": str,
            "values": "",
            "default": "",
            "hidden": True,
            "prefix": None
        },
        {
            "name": "directory_url",
            "description": "url for directory app",
            "type": str,
            "values": "",
            "default": "",
            "hidden": True,
            "prefix": None
        },

        {
            "name": "authentication_url",
            "description": "url for authentication app",
            "type": str,
            "values": "",
            "default": "",
            "hidden": True,
            "prefix": None
        },


    ]
    def __init__( self, *args, **kwargs):

        with_defaults = kwargs.get( "with_defaults", True )
        json = kwargs.get( "json", None )
        filename = kwargs.get("config_filename", self.get_config_filename())
        for cd in self.config_defs:
            if with_defaults:
                value = kwargs.get( cd['name'], cd['default'])
            else:
                value = kwargs.get( cd['name'], None )

            object.__setattr__(self, cd['name'], value)

        if json:
            self.load( json )
        elif filename:
            try:
                with open( expanduser(filename), "rb" ) as f:
                    config_json = f.read()
                self.load( config_json )
            except IOError as e:
                pass

    def get( self, name ):
        return self.__getattribute__(name)

    def __getattribute__( self, name ):
        try:
            r = object.__getattribute__(self, name)
            return r
        except AttributeError as e:
            return None

    def set( self, name, value, force=False ):
        return self.__setattr__( name, value, force=force )

    def __setattr__( self, name, value, force=False ):
        for cd in self.config_defs:
            if cd['name'] == name:
                object.__setattr__(self, name, value)
                return True

        raise AttributeError( "Attribute '{}' is not a valid configuration term".format( name ))

    def __str__(self):
        return self.json()

    def load_defaults(self, strict=True):
        for cd in self.config_defs:
            if strict:
                object.__setattr__(self, cd['name'], cd['default'])
            else:
                if cd['default'] and not object.__getattribute__(self, cd['name']):
                    object.__setattr__(self, cd['name'], cd['default'])

    def json( self ):

        d = {}
        for c in self.config_defs:
            d[c['name']] = object.__getattribute__(self, c['name'])

        return json.dumps(d, indent=2)

    def load( self, json_obj ):
        try:
            d = json.loads(json_obj)
            for c in d:
                object.__setattr__(self, c, d[c])
        except Exception as e:
            self.load_defaults()

    def get_config_filename(self):
        if environ.get('PHONEPROV_CONFIG_FILENAME', None) is not None:
            return environ.get('PHONEPROV_CONFIG_FILENAME')

        return environ.get('PHONEPROV_PATH', "~/.phoneprov") + "/config.json"

    def write(self, filename=None):
        if filename is None:
            filename = self.get_config_filename()

        json_config = self.json()
        with open( expanduser(filename), "wb" ) as f:
            f.write( bytes( json_config.encode('latin-1')) )

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Phoneprov config reader/writer")
    parser.add_argument( '--init', action='store_true', help="initialize new config file and set to defaults" )
    parser.add_argument( '--config', default="~/.phoneprov/config.json", help="config file to read/write to [~/.phoneprov/config.json]" )
    parser.add_argument( 'option', nargs='?', help="configuration option to read or write to" )
    parser.add_argument( 'value', nargs='*', help="value to set (multiple values will result in an array")

    args = parser.parse_args()
    config = Config(config_filename=args.config)

    if args.option is None:
        if args.init:
            config.write(filename=args.config)

        print(config)
        exit()

    if not args.value:
        print("{}: {}".format( args.option, config.get( args.option )))
        exit()

    if len( args.value ) == 1:
        config.set( args.option, args.value[0] )
    else:
        config.set( args.option, args.value )

    config.write(filename=args.config)
    print(config)
