from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from lxml import html
import argparse

argv = argparse.ArgumentParser( description = 'Веб-краулер' )
argv.add_argument( '--galaxy' , help = 'Галактика' )
argv.add_argument( '--system' , help = 'Система' )
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
	'profile.managed_default_content_settings.images' : 2
} )
options.add_argument( '--no-sandbox' )
options.add_argument( '--disable-dev-shm-usage' )
options.add_argument( '--headless' )
options.add_argument( '--disable-gpu' )
options.add_argument( 'User-Agent=Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36' )

webdriver = webdriver.Chrome( executable_path = '/usr/lib/chromium-browser/chromedriver' , chrome_options = options )
webdriver.get( 'http://oxsar.ru/index.php/site/index' )

form = webdriver.find_element_by_css_selector( '.left_reset_form' )
login_login = form.find_element_by_css_selector( '.left_text_login' )
login_passwd = form.find_element_by_css_selector( '.left_text_passwd' )
login_submit = form.find_element_by_css_selector( '.left_submit_btn' )

login_login.clear( )
login_passwd.clear( )

login_login.send_keys( args.login )
login_passwd.send_keys( args.password )
login_submit.send_keys( Keys.RETURN )

webdriver.get( 'http://dm.oxsar.ru/game.php/Galaxy' )

for galaxy in galaxyes :
	print( 'galaxy %s' % galaxy )

	for system in systems :
		print( 'galaxy %s, system %s' % ( galaxy , system ) )

		try :
			form = webdriver.find_element_by_name( 'galaxy_form' )
			input_galaxy = form.find_element_by_name( 'galaxy' )
			input_system = form.find_element_by_name( 'system' )

			input_galaxy.clear( )
			input_galaxy.send_keys( galaxy )

			input_system.clear( )
			input_system.send_keys( system )
			input_system.send_keys( Keys.RETURN )
		except : continue

		for planet in planets :
			try :
				value = webdriver.execute_script( 'return debris_%s' % planet )
				items = html.fromstring( value ).xpath( '//tr[position( )>1]//text( )' )

				if not len( items ) : continue

				print( "%s-%s-%s" % ( galaxy , system , planet ) )

				while len( items ) :
					name = items.pop( 0 )[:-1]
					value = items.pop( 0 )

					print( "%s\t%s" % ( name , value ) )
			except : pass
webdriver.quit( )