from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from lxml import html
import argparse

argv = argparse.ArgumentParser( description = 'Веб-краулер' )
argv.add_argument( '--galaxy' , type = int , help = 'Галактика' )
argv.add_argument( '--system' , type = int , help = 'Система' )
argv.add_argument( '--login' , required = True , help = 'Логин' )
argv.add_argument( '--password' , required = True , help = 'Пароль' )
args = argv.parse_args( )

if args.galaxy is None : galaxyes = range( 1 , 4 )
else : galaxyes = [ args.galaxy ]

if args.system is None : systems = range( 1 , 301 )
else : systems = [ args.system ]

planets = range( 1 , 31 )

options = Options( )
options.add_experimental_option( 'prefs' , {
	'profile.managed_default_content_settings.images' : 2 ,
	'plugins.plugins_disabled' : [ 'Shockwave Flash' ]
} )
for option in [
	'disable-infobars' , 'start-maximized' ,
	'--no-sandbox' , '--disable-dev-shm-usage' , '--headless' , '--disable-gpu' , '--disable-extensions' ,
	'User-Agent=Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
] : options.add_argument( option )

try :
	wdh = webdriver.Chrome( executable_path = '/usr/lib/chromium-browser/chromedriver' , chrome_options = options )
	wdh.get( 'http://oxsar.ru/index.php/site/index' )

	form = wdh.find_element_by_name( 'oxsar_form' )
	field = form.find_element_by_name( 'username' )
	field.send_keys( args.login )

	field = form.find_element_by_name( 'password' )
	field.send_keys( args.password )
	field.send_keys( Keys.RETURN )

	wdh.get( 'http://dm.oxsar.ru/game.php/Galaxy' )

	for galaxy in galaxyes :
		for system in systems :
			form = wdh.find_element_by_name( 'galaxy_form' )
			field = form.find_element_by_name( 'galaxy' )
			field.clear( )
			field.send_keys( galaxy )

			field = form.find_element_by_name( 'system' )
			field.clear( )
			field.send_keys( system )
			field.send_keys( Keys.RETURN )

			print( "%s\t%s" % ( galaxy , system ) )

			for planet in planets :
				try :
					value = wdh.execute_script( 'return debris_%s' % planet )
					items = html.fromstring( value ).xpath( '//tr[position( )>1]//text( )' )

					if items : print( "%s\t%s\t%s\t%s" % ( galaxy , system , planet , items ) )
				except : pass
except Exception as exception : print( exception )
finally : wdh.quit( )