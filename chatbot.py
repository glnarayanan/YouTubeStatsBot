#-------------------------------------------------------------------------------
# Name:        bot-info
# Purpose:      Google Chat Bot
#
# Author:      Lakshmi Narayanan G
#
# Created:     15/1/2013
# Copyright:   (c) TrailBlazer 2012
# Licence:     GNU General Public License
#-------------------------------------------------------------------------------

import cgi
from google.appengine.api import xmpp
import webapp2

import urlparse
#Initialize YouTube Data Service Object
import gdata.youtube
import gdata.youtube.service
yt_service = gdata.youtube.service.YouTubeService()
#Turn on SSL Access
yt_service.ssl = True
#Set YouTube Developer Key and Client ID
yt_service.developer_key = 'AI39si7Bh99MmvU7rYsDBeixgVWv_IXdSUKIPlDKBjM7WKgcCO_E2a3tYKUQyhVTCCqfVOp-PxPoHxuLbtK8HP_OX-vBKnFoRQ'

class XMPPHandler(webapp2.RequestHandler):

    def post(self):
        #Gets the message sent by the user
        message = xmpp.Message(self.request.POST)
        #Parse the message body
        url_data = urlparse.urlparse(""+message.body+"")
        #Parse the Query Component
        q = urlparse.parse_qs(url_data.query)
        #Retrieve the video ID from the given URL
        videoid = q["v"][0]
        #Retrive the information about the particular video
        entry = yt_service.GetYouTubeVideoEntry(video_id=''+videoid+'')
        comments = yt_service.GetYouTubeVideoCommentFeed(video_id=''+videoid+'')
        #Display the View Count,Average Video Rating,Number of Raters,Duration in seconds,Total Number of Comments
        message.reply('Views: %s \n Video rating: %s \n Number of Raters: %s \n Video duration(Seconds): %s \n Total Comments: %s' %(entry.statistics.view_count,entry.rating.average,entry.rating.num_raters,entry.media.duration.seconds,entry.comments.feed_link[0].count_hint))


application = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],debug=True)

def main():
    application.run()
if __name__ == "__main__":
    main()
