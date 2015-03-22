from google.appengine.ext import blobstore

from google.appengine.ext.webapp import blobstore_handlers

import webapp2

import json

from google.appengine.api import urlfetch



class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        """ Return an upload URL. """
        upload_url = blobstore.create_upload_url('/upload', gs_bucket_name='handshake-resume-cnd/resumes/')
        response_object = {}
        response_object['upload_url']= upload_url
        self.response.content_type = 'application/json'
        self.response.out.write(json.dumps(response_object))

    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        # Hook to update Parse database...
        print self.request.POST.get('username')
        payload = {
                'username': self.request.POST.get('username'),
                'resume_url': ''.join(['https://handshake-hack.appspot.com/files/', str(blob_info.key())])
            }
        result = urlfetch.fetch(url='https://api.parse.com/1/classes/JobSeeker',
            payload=json.dumps(payload),
            method=urlfetch.POST,
            headers={'Content-Type': 'application/json',
                'X-Parse-Application-Id': 'Aw2wgeVa9ihzU3OqRggicJ2rcFoQFxQYIWDhnaFR',
                'X-Parse-REST-API-Key': '**REST API KEY HERE**'
            })
        # print json.dumps(result)
        print result.content
        print result.headers
        
        if result.status_code == 200:
            self.redirect('/success.html')
        else:
            self.redirect('/error')


app = webapp2.WSGIApplication([
    webapp2.Route(
        '/upload',
        handler=UploadHandler,
        methods=['GET', 'POST']
    )
])