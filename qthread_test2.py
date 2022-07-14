import sys
import pickle
import platform
from PyQt5.QtCore import SIGNAL, Qt, QPoint
from PyQt5.QtGui import QMainWindow, QApplication, QSystemTrayIcon, QIcon
from PyQt5.QtGui import QPixmap, QMenu, QMessageBox, QPainter, QFont, QColor
from GetWeatherQThread import GetWeatherQThread
from WeatherDialog import WeatherDialog
from ConfigureDialog import ConfigureDialog
from configparser import ConfigParser
import io
import os.path

class PigeonFeather(QMainWindow):
    """Main class for the application, inherits class genrated from pyuic"""

    def __init__(self, parent=None):
        super(PigeonFeather, self).__init__(parent)

        # Check that environment supports systemtray
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print('FATAL: There is no system tray')
            sys.exit(1)

        # Make sure that we can load an icon list
        try:
            with open('code2iconlist.pkl', 'rb') as iconList:
                self.codeToIconList = pickle.load(iconList)
        except (IOError, pickle.PickleError):
            print('FATAL: Could not not load code2iconlist')
            sys.exit(1)

        # See if balloon messages are supported
        #print('Desktop support balloon messages = ' + \
        #    str(QSystemTrayIcon.supportsMessages()))

        # Set the user config fle
        self.USER_CONFIG = os.path.expanduser('~/.pigeonfeather')

        # Load preferences
        self.loadConfig()

        # Class properties
        self.trayIcon = QSystemTrayIcon(self)

        # Weather Dialog and Configure Dialog
        self.weatherDialog = WeatherDialog(self)
        self.configureDialog = ConfigureDialog(self)

        # Set up the application
        self.setup()

    def setup(self):
        """Setup and start the application"""
        # Connect some slots

        # Icon is clicked
        self.connect(self.trayIcon, \
            SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), \
            self.trayIconClicked)

        # Connnect slot emitted from CnfigureDialog to update preferences
        self.connect(self.configureDialog, SIGNAL('ConfigureDialogOk'), \
            self.saveConfig)

        # Set an initial icon for tray and weather dialog
        self.setTrayIcon(QIcon('images/22/dunno.png'))
        self.weatherDialog.labelIcon.setPixmap(QPixmap('images/64/dunno.png'))

        # Set the menu
        self.trayIcon.setContextMenu(self.createMenu())

        # Setup the config dialog with values loaded from config
        woeid = self.config.get('main', 'woeid')

        # If woeid is not valid set a default and use that
        try:
            self.configureDialog.setWoeid(woeid)
        except ValueError as ve:
            self.config.set('main', 'woeid', '2408842')
            self.configureDialog.setWoeid('2408842')

        # Set temperature units
        if self.config.get('units', 'temperature') == 'fahrenheit':
            self.configureDialog.setTemperature('fahrenheit')
        else:
            self.configureDialog.setTemperature('celcius')

        # Set distance units
        if self.config.get('units', 'distance') == 'km':
            self.configureDialog.setDistance('km')
        else:
            self.configureDialog.setDistance('mi')

        # Set wind units
        if self.config.get('units', 'wind') == 'kph':
            self.configureDialog.setWind('kph')
        else:
            self.configureDialog.setWind('mph')

        # Set pressure units
        if self.config.get('units', 'pressure') == 'mb':
            self.configureDialog.setPressure('mb')
        else:
            self.configureDialog.setPressure('in')

        # Start getWeather thread with Id from config
        # Connect two slots for the two signals emitted from thread
        self.getWeatherThread = GetWeatherQThread(self.config.get( \
            'main', 'woeid'))
        self.getWeatherThread.start()

        self.connect(self.getWeatherThread, SIGNAL('WeatherUpdate'), \
            self.processWeather)
        self.connect(self.getWeatherThread, SIGNAL('WeatherReadError'), \
            self.showErrorMessage)

    def loadConfig(self):
        """Load preferences from defaults then self.USER_CONFIG if exists"""
        # Load a default set first
        defaultConfig = io.StringIO("""\
[main]
Woeid=2408842
[units]
temperature=celcius
wind=mph
pressure=mb
distance=mi
""")

        self.config = ConfigParser()

        # Load defaults
        self.config.readfp(defaultConfig)

        # Load config if it exists
        self.config.read(self.USER_CONFIG)

    def createMenu(self):
        """Create and return the applications menu"""
        menu = QMenu(self)
        menu.addAction(QIcon('images/22/sunny.png'), '&Show Weather Report', \
            self.showWeatherDialog)
        menu.addAction(QIcon('images/22/configure.png'), '&Configure', \
            self.showConfigureDialog)
        menu.addAction(QIcon('images/22/help.png'), '&About', \
            self.showAboutDialog)
        menu.addAction(QIcon('images/22/exit.png'), '&Exit', self.quitApp)
        return menu

    def saveConfig(self, config):
        """Save the recieved config back to the config file and update the
        local copy in the object

        Keyword arguments:
        config -- A dict. of config recieved from the configuration dialog
        """
        # Set the local config object and try and save it
        self.config.set('main', 'woeid', config['woeid'])
        self.config.set('units', 'temperature', config['temperature'])
        self.config.set('units', 'wind', config['wind'])
        self.config.set('units', 'pressure', config['pressure'])
        self.config.set('units', 'distance', config['distance'])

        # Update the Weoid in the get weather thread
        self.getWeatherThread.setWoeid(config['woeid'])

        # Try and save the config
        try:
            with open(self.USER_CONFIG, 'wb') as configfile:
                self.config.write(configfile)
        except IOError as ioe:
            self.showErrorMessage('Could not save configuration settings' + \
                'to disk')

    def showErrorMessage(self, message):
        """Show a error as a tray balloon message

        Keyword arguments:
        message -- Error message to display
        """
        self.trayIcon.showMessage('Application Error', message, \
            QSystemTrayIcon.Critical)

    def trayIconClicked(self, reason):
        """If the tray icon is left clicked, show/hide the weather dialog
        If this is called on a Darwin(mac) machine do not pop up.  This follows
        better mac convention

        Keyword arguments:
        reason -- A QSystemTrayIcon.ActivationReason enum
        """
        # If mac then ignore click
        if platform.system() == 'Darwin':
            return

        # Test for left click
        if reason == 3:
            if self.weatherDialog.isVisible():
                self.weatherDialog.hide()
            else:
                self.weatherDialog.show()

    def showWeatherDialog(self):
        """Show the weather report dialog"""
        self.weatherDialog.show()

    def showConfigureDialog(self):
        """Show the configure dialog"""
        self.configureDialog.show()

    def showAboutDialog(self):
        """Show the about pyqtweather dialog"""
        QMessageBox.about(None, 'About Pigeon Feather', 'Pigeon Feather\n \
            (c) 2010 Ben Sampson\nPigeon Feather uses the Yahoo! Weather API\n\
            License: GNU General Public License Version 3')

    def processWeather(self, weather):
        """Slot that is called by the weather thread, responsible for updating
        the GUI with the new weather data, this includes the trayicon and
        tooltip and the weather report dialog

        Keyword arguments:
        weather -- map of weather data
        """
        # TODO These should really call setter methods on weather dialog

        # Copy weather to local vars basd on preferences
        fetched = weather['fetched']

        code = weather['code']
        if self.config.get('units', 'temperature') == 'celcius':
            temp = weather['tempC']
            chill = weather['chillC']
            tempUnit = 'C'
        else:
            temp = weather['tempF']
            chill = weather['chillF']
            tempUnit = 'F'

        text = weather['text']
        city = weather['city']
        region = weather['region']
        country = weather['country']

        sunrise = weather['sunrise']
        sunset = weather['sunset']

        if self.config.get('units', 'wind') == 'mph':
            windSpeed = weather['windSpeedMph']
            speedUnit = 'mph'
        else:
            windSpeed = weather['windSpeedKph']
            speedUnit = 'kph'

        if self.config.get('units', 'pressure') == 'mb':
            pressure = weather['pressureMb']
            pressureUnit = 'mb'
        else:
            pressure = weather['pressureIn']
            pressureUnit = 'in'

        directionTextual = weather['directionTextual']
        pressureTendancy = weather['pressureTendancy']
        humidity = weather['humidity']

        if self.config.get('units', 'distance') == 'mi':
            visibility = weather['visibilityMi']
            distanceUnit = 'mi'
        else:
            visibility = weather['visibilityKm']
            distanceUnit = 'km'

        # Get the filename for the icon to disply from the icon list map
        # Generate the system tray icon and set it
        iconFileName = self.codeToIconList[int(code)][1]
        icon = self.createWeatherIcon('images/22/' + iconFileName, str(temp))
        self.setTrayIcon(icon)

        # Set the tool tip
        tempString = str(temp) + '°' + tempUnit + ' ' + text
        self.trayIcon.setToolTip(tempString)

        # Update the weather report dialog
        self.weatherDialog.labelLastUpdate.setText( \
            fetched.strftime('%H:%M:%S'))
        self.weatherDialog.setWindowTitle('Weather report for ' + city + \
            ', ' + region + ' ' + country)
        self.weatherDialog.labelTemp.setText(tempString)
        self.weatherDialog.labelSunrise.setText(sunrise)
        self.weatherDialog.labelSunset.setText(sunset)
        self.weatherDialog.labelWindChill.setText(str(chill) + \
            '°' + tempUnit)
        self.weatherDialog.labelWindSpeed.setText(str(windSpeed) + ' ' + \
            speedUnit)
        self.weatherDialog.labelWindDirection.setText(directionTextual)
        self.weatherDialog.labelHumidity.setText(str(humidity) + '%')
        self.weatherDialog.labelVisibility.setText(str(visibility) + ' ' + \
            distanceUnit)
        self.weatherDialog.labelPressure.setText(str(pressure) + ' ' + \
            pressureUnit)
        self.weatherDialog.labelRising.setText(pressureTendancy)

        # Set the image
        self.weatherDialog.labelIcon.setPixmap(QPixmap('images/64/' + \
          iconFileName))

    # TODO - this should really be in another class
    def createWeatherIcon(self, iconFileName, temp):
        """Create the icon to display in the tray"""
        # Create a map of what image to use based on code
        # Start by creating a transparent image to paint on
        print(('Using' + iconFileName))
        icon = QPixmap(22, 22)
        icon.fill(Qt.transparent)

        # Create a painter to paint on to the icon and draw on the text
        painter = QPainter(icon)
        painter.setOpacity(0.5)

        # Draw text of temperature
        font = QFont('Times', 10, QFont.Black)
        painter.setFont(font)
        painter.setPen(QColor('red'))
        painter.drawPixmap(QPoint(0, 0), QPixmap(iconFileName))
        painter.setOpacity(1)
        painter.drawText(5, 15, temp)
        painter.end()

        # Return the icon
        return QIcon(icon)

    def setTrayIcon(self, icon):
        """Set the tray icon"""
        self.trayIcon.setIcon(icon)
        self.trayIcon.show()

    def quitApp(self):
        """Exit the application"""
        sys.exit(0)
