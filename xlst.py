#!/usr/pkg/bin/python3.13

#
# Time-stamp: <2025/03/23 16:55:48 (UT+08:00) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy.time
import astropy.units

# importing datetime module
import datetime

# importing sys module
import sys

# importing tkinter module
import tkinter
import tkinter.ttk

# initialising a parser
parser = argparse.ArgumentParser (description='LST Clock')

# adding arguments
parser.add_argument ('-s', '--site', default='Lulin', \
                     help='Observatory site name (default: Lulin)')
parser.add_argument ('-l', '--longitude', default='120:52:21.5', \
                     help='Longitude in ddd:mm:ss.s format')
parser.add_argument ('-b', '--latitude', default='+23:28:10.0', \
                     help='Latitude in [+/-]dd:mm:ss.s format')
parser.add_argument ('-a', '--altitude', type=float, default=2862.0, \
                     help='Altitude above sea level in metre')
parser.add_argument ('-z', '--timezone', type=float, default=8.0, \
                     help='offset from UT in hour')

# parsing arguments
args = parser.parse_args ()

# command-line arguments
site_name   = args.site
longitude   = args.longitude
latitude    = args.latitude
altitude_m  = args.altitude
timezone_hr = args.timezone

# class AstroTime
class AstroTime:
    def __init__ (self, site, lon, lat, altitude, tz):
        if ( (site == '') or (lon == '') or (lat == '') or (altitude == '') \
             or (tz == '') ):
            print (f'ERROR: missing information')
            sys.exit (0)
        self.site     = site
        self.lon      = lon
        self.lat      = lat
        self.altitude = altitude
        self.tz       = tz

    # method to find date/time in UTC
    def find_utcnow (self):
        # date/time
        utc_now  = datetime.datetime.now (datetime.UTC)
        utc_YYYY = utc_now.year
        utc_MM   = utc_now.month
        utc_DD   = utc_now.day
        utc_hh   = utc_now.hour
        utc_mm   = utc_now.minute
        utc_ss   = utc_now.second
        # utc in YYYY-MM-DD
        utc_YYYYMMDD = f'{utc_YYYY:04d}-{utc_MM:02d}-{utc_DD:02d}'
        # utc in hh:mm:ss format
        utc_hhmmss = f'{utc_hh:02d}:{utc_mm:02d}:{utc_ss:02d}'
        # return utc in hh:mm:ss format
        return (utc_YYYYMMDD, utc_hhmmss)

    # method to find local time
    def find_localtime (self):
        # finding local time
        offset  = datetime.timedelta (hours=self.tz)
        tz      = datetime.timezone (offset)
        lt_now  = datetime.datetime.now (tz)
        lt_YYYY = lt_now.year
        lt_MM   = lt_now.month
        lt_DD   = lt_now.day
        lt_hh   = lt_now.hour
        lt_mm   = lt_now.minute
        lt_ss   = lt_now.second
        # localtime in YYYY-MM-DD
        lt_YYYYMMDD = f'{lt_YYYY:04d}-{lt_MM:02d}-{lt_DD:02d}'
        # localtime in hh:mm:ss format
        lt_hhmmss = f'{lt_hh:02d}:{lt_mm:02d}:{lt_ss:02d}'
        # return localtime in hh:mm:ss format
        return (lt_YYYYMMDD, lt_hhmmss)

    # method to find local sidereal time
    def find_lst (self):
        (utc_YYYYMMDD, utc_hhmmss) = astrotime.find_utcnow ()
        utc_str = f'{utc_YYYYMMDD} {utc_hhmmss}'
        t_astropy = astropy.time.Time (utc_str, format='iso', scale='utc', \
                                       location=(self.lon, self.lat) )
        lst = t_astropy.sidereal_time ('apparent')
        lst_hhmmss = f'{int (lst.hms.h):02d}:{int (lst.hms.m):02d}:{int (lst.hms.s):02d}'
        return (lst_hhmmss)

# function to update label
def update_time ():
    (utc_YYYYMMDD, utc_hhmmss) = astrotime.find_utcnow ()
    (lt_YYYYMMDD, lt_hhmmss)   = astrotime.find_localtime ()
    (lst_hhmmss)               = astrotime.find_lst ()
    label_utc_YYYYMMDD.configure (text=f'Date (UTC): {utc_YYYYMMDD}')
    label_utc_hhmmss.configure (text=f'Time (UTC): {utc_hhmmss}')
    label_lt_YYYYMMDD.configure (text=f'Date (Local): {lt_YYYYMMDD}')
    label_lt_hhmmss.configure (text=f'Time (Local): {lt_hhmmss}')
    label_lst_hhmmss.configure (text=f'LST: {lst_hhmmss}')
    gui.after (300, update_time)

# main routine
if (__name__ == '__main__'):
    # making AstroTime object
    astrotime = AstroTime (site_name, longitude, latitude, altitude_m, \
                           timezone_hr)
    # root window of GUI
    gui = tkinter.Tk ()
    # style
    style = tkinter.ttk.Style ()
    style.configure ('TButton', font=('Helvetica', 32))
    # frame
    frame = tkinter.ttk.Frame (gui, padding=10)
    frame.grid ()
    # date/time
    (utc_YYYYMMDD, utc_hhmmss) = astrotime.find_utcnow ()
    (lt_YYYYMMDD, lt_hhmmss)   = astrotime.find_localtime ()
    (lst_hhmmss)               = astrotime.find_lst ()
    # adding components
    label_title = tkinter.ttk.Label (frame, \
                                     padding=8, \
                                     text=f'LST Clock', \
                                     font=('Helvetica', 64))
    label_title.grid (column=0, row=0, columnspan=2)

    label_siteinfo = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'Site Information: {astrotime.site}', \
        font=('Helvetica', 48)
    )
    label_siteinfo.grid (column=0, row=1, columnspan=2)
    label_lon = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'Longitude: {astrotime.lon}', \
        font=('Helvetica', 32)
    )
    label_lon.grid (column=0, row=2)
    label_lat = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'Latitude: {astrotime.lat}', \
        font=('Helvetica', 32)
    )
    label_lat.grid (column=1, row=2)
    label_altitude = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'Altitude: {astrotime.altitude}-m', \
        font=('Helvetica', 32)
    )
    label_altitude.grid (column=0, row=3)
    label_timezone = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'Timezone: {astrotime.tz:+4.1f}-hr', \
        font=('Helvetica', 32)
    )
    label_timezone.grid (column=1, row=3)

    label_time = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'Time', \
        font=('Helvetica', 48)
    )
    label_time.grid (column=0, row=4, columnspan=2)
    label_utc_YYYYMMDD = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'Date (UTC): {utc_YYYYMMDD}', \
        font=('Helvetica', 32)
    )
    label_utc_YYYYMMDD.grid (column=0, row=5)
    label_utc_hhmmss = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'Time (UTC): {utc_hhmmss}', \
        font=('Helvetica', 32)
    )
    label_utc_hhmmss.grid (column=1, row=5)
    label_lt_YYYYMMDD = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'Date (Local): {lt_YYYYMMDD}', \
        font=('Helvetica', 32)
    )
    label_lt_YYYYMMDD.grid (column=0, row=6)
    label_lt_hhmmss = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'Time (Local): {lt_hhmmss}', \
        font=('Helvetica', 32)
    )
    label_lt_hhmmss.grid (column=1, row=6)
    label_lst_hhmmss = tkinter.ttk.Label (
        frame, \
        padding=8, \
        text=f'LST: {lst_hhmmss}', \
        font=('Helvetica', 32)
    )
    label_lst_hhmmss.grid (column=1, row=7)

    button_quit = tkinter.ttk.Button (
        frame, \
        command=gui.destroy, \
        text=f'Quit', \
        style='TButton'
    )
    button_quit.grid (column=0, row=8, columnspan=2)

    update_time ()
    gui.mainloop ()
