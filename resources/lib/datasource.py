# -*- coding: utf-8 -*-
# 
# Massengeschmack XBMC add-on
# Copyright (C) 2013 by Janek Bevendorff
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import xbmcgui
import urllib
from globalvars import *
import resources.lib
from resources.lib.listing import *

class DataSource(object):
    id = -1
    """Numeric ID of the show."""
    
    moduleName = ''
    """Internal module name."""
    
    showMetaData = {
        'Title'     : None,
        'Director'  : None,
        'Genre'     : None,
        'Premiered' : None,
        'Country'   : None,
        'Plot'      : None
    }
    """Global meta data for the show."""
    
    def getListItems(self):
        """
        Generate a list of ListItem objects for the current data source.
        """
        return [
            # Fernsehkritik-TV
            ListItem(
                FKTVDataSource.id,
                ADDON.getLocalizedString(30200),
                resources.lib.assembleListURL(FKTVDataSource.module),
                ADDON_BASE_PATH + '/resources/media/banner-' + FKTVDataSource.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + FKTVDataSource.module + '.jpg',
                FKTVDataSource.showMetaData
            ),
            # Pantoffel-TV
            ListItem(
                PTVDataSource.id,
                ADDON.getLocalizedString(30210),
                resources.lib.assembleListURL(PTVDataSource.module),
                ADDON_BASE_PATH + '/resources/media/banner-' + PTVDataSource.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + PTVDataSource.module + '.jpg',
                PTVDataSource.showMetaData
            ),
            # Pressesch(l)au
            ListItem(
                PSDataSource.id,
                ADDON.getLocalizedString(30220),
                resources.lib.assembleListURL(PSDataSource.module),
                ADDON_BASE_PATH + '/resources/media/banner-' + PSDataSource.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + PSDataSource.module + '.jpg',
                PSDataSource.showMetaData
            ),
            # Massengeschmack-TV
            ListItem(
                MGTVDataSource.id,
                ADDON.getLocalizedString(30230),
                resources.lib.assembleListURL(MGTVDataSource.module),
                ADDON_BASE_PATH + '/resources/media/banner-' + MGTVDataSource.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + MGTVDataSource.module + '.jpg',
                MGTVDataSource.showMetaData
            ),
        ]
    
    def getContentMode(self):
        """
        Get the view mode for the listing content.
        
        Content mode is usually either 'tvshows' or 'episodes', but can
        also be any other valid value for xbmcplugin.setContent().
        
        @return content mode
        """
        return 'tvshows'
    
    def _buildFeedURL(self, ids, quality):
        """
        Build a feed URL which points to an RSS feed filtered by the given IDs.
        
        This method relies on self.id being set properly in derived classes.
        
        @protected
        
        @type ids: list
        @param ids: a list of numeric IDs of all sub shows to filter by
        @type quality: str
        @param quality: the movie quality (either 'hd', 'mobile' or 'audio')
        """
        url = HTTP_BASE_FEED_URI
        
        first = True
        for i in ids:
            if not first:
                url += 'x'
            first = False
            url += str(self.id) + '-' + str(i)
            
        url += '/' + quality + '.xml'
        
        return url


class FKTVDataSource(DataSource):
    id           = 1
    module       = 'fktv'
    showMetaData = {
        'Title'    : ADDON.getLocalizedString(30200),
        'Director' :'Holger Kreymeier, Nils Beckmann, Daniel Gusy',
        'Genre'    : ADDON.getLocalizedString(30201),
        'Premiered':'07.04.2007',
        'Country'  : ADDON.getLocalizedString(30202),
        'Plot'     : ADDON.getLocalizedString(30203)
    }
    
    def __init__(self):
        self.__urls = {
            'hd' : {
                'all'          : DataSource._buildFeedURL(self, [1, 2, 3, 4, 5], 'hd'),
                'episodes'     : DataSource._buildFeedURL(self, [1], 'hd'),
                'postecke'     : DataSource._buildFeedURL(self, [2], 'hd'),
                'interviews'   : DataSource._buildFeedURL(self, [3], 'hd'),
                'extras'       : DataSource._buildFeedURL(self, [4], 'hd'),
                'sendeschluss' : DataSource._buildFeedURL(self, [5], 'hd')
            },
            'mobile' : {
                'all'          : DataSource._buildFeedURL(self, [1, 2, 3, 4, 5], 'mobile'),
                'episodes'     : DataSource._buildFeedURL(self, [1], 'mobile'),
                'postecke'     : DataSource._buildFeedURL(self, [2], 'mobile'),
                'interviews'   : DataSource._buildFeedURL(self, [3], 'mobile'),
                'extras'       : DataSource._buildFeedURL(self, [4], 'mobile'),
                'sendeschluss' : DataSource._buildFeedURL(self, [5], 'mobile')
            },
            'audio' : {
                'all'          : DataSource._buildFeedURL(self, [1, 2, 3, 4, 5], 'audio'),
                'episodes'     : DataSource._buildFeedURL(self, [1], 'audio'),
                'postecke'     : DataSource._buildFeedURL(self, [2], 'audio'),
                'interviews'   : DataSource._buildFeedURL(self, [3], 'audio'),
                'extras'       : DataSource._buildFeedURL(self, [4], 'audio'),
                'sendeschluss' : DataSource._buildFeedURL(self, [5], 'audio')
            }
        }
    
    def getListItems(self):
        audioOnly = ADDON.getSetting('content.audioOnly')
        
        quality = None
        if 'true' == audioOnly:
            quality = 'audio'
        else:
            if 0 == int(ADDON.getSetting('content.quality')):
                quality = 'hd'
            else:
                quality = 'mobile'
        
        submodule = None
        if 'submodule' in ADDON_ARGS and ADDON_ARGS['submodule'] in self.__urls[quality]:
            submodule = ADDON_ARGS['submodule']
        
        if None == submodule:
            return self.__getBaseList()
        
        data      = resources.lib.parseRSSFeed(self.__urls[quality][submodule], True)
        listItems = []
        
        for i in data:
            iconimage = self.__getThumbnailURL(i['guid'])
            date      = resources.lib.parseUTCDateString(i['pubdate']).strftime('%d.%m.%Y')
            metaData  = {
                'Title'     : i['title'],
                'Genre'     : ADDON.getLocalizedString(30201),
                'Date'      : date,
                'Premiered' : date,
                'Country'   : ADDON.getLocalizedString(30232),
                'Plot'      : i['description'],
                'Duration'  : int(i['duration']) / 60
            }
            streamInfo = {
                'duration' : i['duration']
            }
            
            listItems.append(
                ListItem(
                    self.id,
                    i['title'],
                    resources.lib.assemblePlayURL(i['url'], i['title'], iconimage, metaData, streamInfo),
                    iconimage,
                    ADDON_BASE_PATH + '/resources/media/fanart-fktv.jpg',
                    metaData,
                    streamInfo,
                    False
                )
            )
        
        return listItems
    
    def getContentMode(self):
        if 'submodule' in ADDON_ARGS:
            return 'episodes'
        
        return 'tvshows'
    
    def __getThumbnailURL(self, guid):
        basePath1 = 'http://fernsehkritik.tv/images/magazin/'
        basePath2 = 'http://massengeschmack.tv/img/mag/'
        
        if 'fktv' == guid[0:4]:
            return basePath1 + 'folge' + guid[4:] + '@2x.jpg'
        if 'postecke' == guid[0:8]:
            return basePath2 + 'postecke.jpg'
        if 'interview-' == guid[0:10]:
            if 'remote' == guid[10:]:
                # ugly fix for single episode
                return basePath2 + 'remotecontrol.jpg'
            
            return basePath2 + guid[10:] + '.jpg'
        
        return basePath2 + guid + '.jpg'
    
    def __getBaseList(self):
        return [
            # All
            ListItem(
                self.id,
                ADDON.getLocalizedString(30300),
                resources.lib.assembleListURL(self.module, 'all'),
                ADDON_BASE_PATH + '/resources/media/banner-' + self.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + self.module + '.jpg',
                {
                    'Title': ADDON.getLocalizedString(30300),
                    'Plot': ADDON.getLocalizedString(30350)
                }
            ),
            # Episodes
            ListItem(
                self.id,
                ADDON.getLocalizedString(30301),
                resources.lib.assembleListURL(self.module, 'episodes'),
                ADDON_BASE_PATH + '/resources/media/banner-' + self.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + self.module + '.jpg',
                {
                    'Title': ADDON.getLocalizedString(30301),
                    'Plot': ADDON.getLocalizedString(30351)
                }
            ),
            # Sendeschluss
            ListItem(
                self.id,
                ADDON.getLocalizedString(30356),
                resources.lib.assembleListURL(self.module, 'sendeschluss'),
                ADDON_BASE_PATH + '/resources/media/banner-' + self.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + self.module + '.jpg',
                {
                    'Title': ADDON.getLocalizedString(30356),
                    'Plot': ADDON.getLocalizedString(30357)
                }
            ),
            # Postecke
            ListItem(
                self.id,
                ADDON.getLocalizedString(30352),
                resources.lib.assembleListURL(self.module, 'postecke'),
                ADDON_BASE_PATH + '/resources/media/banner-' + self.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + self.module + '.jpg',
                {
                    'Title': ADDON.getLocalizedString(30352),
                    'Plot': ADDON.getLocalizedString(30353)
                }
            ),
            # Interviews
            ListItem(
                self.id,
                ADDON.getLocalizedString(30302),
                resources.lib.assembleListURL(self.module, 'interviews'),
                ADDON_BASE_PATH + '/resources/media/banner-' + self.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + self.module + '.jpg',
                {
                    'Title': ADDON.getLocalizedString(30302),
                    'Plot': ADDON.getLocalizedString(30354)
                }
            ),
            # Extras
            ListItem(
                self.id,
                ADDON.getLocalizedString(30303),
                resources.lib.assembleListURL(self.module, 'extras') ,
                ADDON_BASE_PATH + '/resources/media/banner-' + self.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + self.module + '.jpg',
                {
                    'Title': ADDON.getLocalizedString(30303),
                    'Plot': ADDON.getLocalizedString(30355)
                }
            )
        ]


class PTVDataSource(DataSource):
    id           = 2
    module       = 'ptv'
    showMetaData = {
        'Title'    : ADDON.getLocalizedString(30210),
        'Director' :'Holger Kreymeier, Jenny von Gagern, Steven Gräwe, Michael Stock',
        'Genre'    : ADDON.getLocalizedString(30211),
        'Premiered':'17.06.2013',
        'Country'  : ADDON.getLocalizedString(30212),
        'Plot'     : ADDON.getLocalizedString(30213)
    }
    
    def __init__(self):
        self.__urls = {
            'hd' : {
                'all' : DataSource._buildFeedURL(self, [1], 'hd'),
            },
            'mobile' : {
                'all' : DataSource._buildFeedURL(self, [1], 'mobile'),
            },
            'audio' : {
                'all' : DataSource._buildFeedURL(self, [1], 'audio'),
            }
        }
    
    def getListItems(self):
        audioOnly = ADDON.getSetting('content.audioOnly')
        
        quality = None
        if 'true' == audioOnly:
            quality = 'audio'
        else:
            if 0 == int(ADDON.getSetting('content.quality')):
                quality = 'hd'
            else:
                quality = 'mobile'
        
        data      = resources.lib.parseRSSFeed(self.__urls[quality]['all'], True)
        listItems = []
        
        for i in data:
            iconimage = self.__getThumbnailURL(i['guid'])
            date      = resources.lib.parseUTCDateString(i['pubdate']).strftime('%d.%m.%Y')
            metaData  = {
                'Title'     : i['title'],
                'Genre'     : ADDON.getLocalizedString(30211),
                'Date'      : date,
                'Premiered' : date,
                'Country'   : ADDON.getLocalizedString(30232),
                'Plot'      : i['description'],
                'Duration'  : int(i['duration']) / 60
            }
            streamInfo = {
                'duration' : i['duration']
            }
            
            listItems.append(
                ListItem(
                    self.id,
                    i['title'],
                    resources.lib.assemblePlayURL(i['url'], i['title'], iconimage, metaData, streamInfo),
                    iconimage,
                    ADDON_BASE_PATH + '/resources/media/fanart-ptv.jpg',
                    metaData,
                    streamInfo,
                    False
                )
            )
        
        return listItems
    
    def getContentMode(self):
        return 'episodes'
    
    def __getThumbnailURL(self, guid):
        episodeNumber = '1'
        if 'ptv-pilot' == guid[:9]:
            if 'ptv-pilot' != guid:
                # if not very first episode
                episodeNumber= guid[9:]
        else:
            episodeNumber = guid[4:]
            
        return 'http://pantoffel.tv/img/thumbs/ptv' + episodeNumber + '_shot1@2x.jpg'


class PSDataSource(DataSource):
    id           = 3
    module       = 'ps'
    showMetaData = {
        'Title'     : ADDON.getLocalizedString(30220),
        'Director'  :'Holger Kreymeier, Steven Gräwe, Daniel Gusy',
        'Genre'     : ADDON.getLocalizedString(30221),
        'Premiered' :'01.08.2013',
        'Country'   : ADDON.getLocalizedString(30222),
        'Plot'      : ADDON.getLocalizedString(30223)
    }
    
    def __init__(self):
        self.__urls = {
            'hd' : {
                'all' : DataSource._buildFeedURL(self, [1], 'hd'),
            },
            'mobile' : {
                'all' : DataSource._buildFeedURL(self, [1], 'mobile'),
            },
            'audio' : {
                'all' : DataSource._buildFeedURL(self, [1], 'audio'),
            }
        }
    
    def getListItems(self):
        audioOnly = ADDON.getSetting('content.audioOnly')
        
        quality = None
        if 'true' == audioOnly:
            quality = 'audio'
        else:
            if 0 == int(ADDON.getSetting('content.quality')):
                quality = 'hd'
            else:
                quality = 'mobile'
        
        data      = resources.lib.parseRSSFeed(self.__urls[quality]['all'], True)
        listItems = []
        
        for i in data:
            iconimage = self.__getThumbnailURL(i['guid'])
            date      = resources.lib.parseUTCDateString(i['pubdate']).strftime('%d.%m.%Y')
            metaData  = {
                'Title'     : i['title'],
                'Genre'     : ADDON.getLocalizedString(30221),
                'Date'      : date,
                'Premiered' : date,
                'Country'   : ADDON.getLocalizedString(30232),
                'Plot'      : i['description'],
                'Duration'  : int(i['duration']) / 60
            }
            streamInfo = {
                'duration' : i['duration']
            }
            
            listItems.append(
                ListItem(
                    self.id,
                    i['title'],
                    resources.lib.assemblePlayURL(i['url'], i['title'], iconimage, metaData, streamInfo),
                    iconimage,
                    ADDON_BASE_PATH + '/resources/media/fanart-ps.jpg',
                    metaData,
                    streamInfo,
                    False
                )
            )
        
        return listItems
    
    def getContentMode(self):
        return 'episodes'
    
    def __getThumbnailURL(self, guid):
        if 'ps-pilot' == guid:
            guid = 'ps1'
        return 'http://massengeschmack.tv/img/ps/' + guid + '.jpg'


class MGTVDataSource(DataSource):
    id           = 0
    module       = 'mgtv'
    showMetaData = {
        'Title'     : ADDON.getLocalizedString(30230),
        'Director'  :'Holger Kreymeier',
        'Genre'     : ADDON.getLocalizedString(30231),
        'Premiered' :'05.08.2013',
        'Country'   : ADDON.getLocalizedString(30232),
        'Plot'      : ADDON.getLocalizedString(30233)
    }
    
    def __init__(self):
        self.__urls = {
            'hd' : {
                'all'      : DataSource._buildFeedURL(self, [1, 2], 'hd'),
                'internal' : DataSource._buildFeedURL(self, [1], 'hd'),
                'studio'   : DataSource._buildFeedURL(self, [2], 'hd')
            },
            'mobile' : {
                'all'      : DataSource._buildFeedURL(self, [1, 2], 'mobile'),
                'internal' : DataSource._buildFeedURL(self, [1], 'mobile'),
                'studio'   : DataSource._buildFeedURL(self, [2], 'mobile')
            },
            'audio' : {
                'all'      : DataSource._buildFeedURL(self, [1, 2], 'audio'),
                'internal' : DataSource._buildFeedURL(self, [1], 'audio'),
                'studio'   : DataSource._buildFeedURL(self, [2], 'audio')
            }
        }
    
    def getListItems(self):
        audioOnly = ADDON.getSetting('content.audioOnly')
        
        quality = None
        if 'true' == audioOnly:
            quality = 'audio'
        else:
            if 0 == int(ADDON.getSetting('content.quality')):
                quality = 'hd'
            else:
                quality = 'mobile'
        
        submodule = None
        if 'submodule' in ADDON_ARGS and ADDON_ARGS['submodule'] in self.__urls[quality]:
            submodule = ADDON_ARGS['submodule']
        
        if None == submodule:
            return self.__getBaseList()
        
        data      = resources.lib.parseRSSFeed(self.__urls[quality][submodule], True)
        listItems = []
        
        for i in data:
            iconimage = self.__getThumbnailURL(i['guid'])
            date      = resources.lib.parseUTCDateString(i['pubdate']).strftime('%d.%m.%Y')
            metaData  = {
                'Title'     : i['title'],
                'Genre'     : ADDON.getLocalizedString(30231),
                'Date'      : date,
                'Premiered' : date,
                'Country'   : ADDON.getLocalizedString(30232),
                'Plot'      : i['description'],
                'Duration'  : int(i['duration']) / 60
            }
            streamInfo = {
                'duration' : i['duration']
            }
            
            listItems.append(
                ListItem(
                    self.id,
                    i['title'],
                    resources.lib.assemblePlayURL(i['url'], i['title'], iconimage, metaData, streamInfo),
                    iconimage,
                    ADDON_BASE_PATH + '/resources/media/fanart-mgtv.jpg',
                    metaData,
                    streamInfo,
                    False
                )
            )
        
        return listItems
    
    def getContentMode(self):
        if 'submodule' in ADDON_ARGS:
            return 'episodes'
        
        return 'tvshows'
    
    def __getThumbnailURL(self, guid):
        if 'studio-' == guid[:7]:
            return 'http://massengeschmack.tv/img/mag/studio' + guid[7:] + '.jpg'
        
        return 'http://massengeschmack.tv/img/mgfeedlogo.jpg'
    
    def __getBaseList(self):
        return [
            # All
            ListItem(
                self.id,
                ADDON.getLocalizedString(30300),
                resources.lib.assembleListURL(self.module, 'all'),
                ADDON_BASE_PATH + '/resources/media/banner-' + self.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + self.module + '.jpg',
                {
                    'Title': ADDON.getLocalizedString(30300),
                    'Plot': ADDON.getLocalizedString(30361)
                }
            ),
            # Das Studio
            ListItem(
                self.id,
                ADDON.getLocalizedString(30360),
                resources.lib.assembleListURL(self.module, 'studio'),
                ADDON_BASE_PATH + '/resources/media/banner-' + self.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + self.module + '.jpg',
                {
                    'Title': ADDON.getLocalizedString(30360),
                    'Plot': ADDON.getLocalizedString(30362)
                }
            ),
            # Massengeschmack Internal
            ListItem(
                self.id,
                ADDON.getLocalizedString(30363),
                resources.lib.assembleListURL(self.module, 'internal'),
                ADDON_BASE_PATH + '/resources/media/banner-' + self.module + '.png',
                ADDON_BASE_PATH + '/resources/media/fanart-' + self.module + '.jpg',
                {
                    'Title': ADDON.getLocalizedString(30363),
                    'Plot': ADDON.getLocalizedString(30364)
                }
            )
        ]


def createDataSource(module=''):
    """
    Create a data source object based on the magazine name.
    If left empty, an overview data source will be generated.
    
    @type module: str
    @keyword module: the magazine name (fktv, ptv, ps, mgtv, ...)
    @return: DataSource instance
    """
    if 'fktv' == module:
        return FKTVDataSource()
    elif 'ptv' == module:
        return PTVDataSource()
    elif 'ps' == module:
        return PSDataSource()
    elif 'mgtv' == module:
        return MGTVDataSource()
    else:
        return DataSource()