from google.appengine.ext import blobstore

from google.appengine.ext.webapp import blobstore_handlers

from google.appengine.api.images import get_serving_url

import webapp2

import json

from google.appengine.api import urlfetch

import urllib


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
        payload = {
                'username': self.request.POST.get('username'),
                'resume_url': ''.join(['https://handshake-hack.appspot.com/files/', str(blob_info.key())])
            }
        result = urlfetch.fetch(url='https://api.parse.com/1/classes/JobSeeker',
            payload=json.dumps(payload),
            method=urlfetch.POST,
            headers={'Content-Type': 'application/json',
                'X-Parse-Application-Id': 'Aw2wgeVa9ihzU3OqRggicJ2rcFoQFxQYIWDhnaFR',
                'X-Parse-REST-API-Key': 'TWEMo9AIIRXCUCfesvRI49Q4mqPM7Zw5muXW239G'
            })
        if result.status_code >= 200 and result.status_code <= 299:
            self.redirect('/success.html')
        else:
            self.redirect('/error')


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, fileId=None):
        """ Return a link to download a file. """

        if not fileId:
            abort(400)

        blob_info = blobstore.BlobInfo.get(fileId)
        self.response.headers.add('Content-Disposition', str(''.join(['attachment; filename="', blob_info.filename, '"'])))
        self.send_blob(blob_info)  # For some reason this wasn't working
        # self.redirect(get_serving_url(blob_info.key()))  # Isntead we'll redirect to a serving link


app = webapp2.WSGIApplication([
    webapp2.Route(
        '/upload',
        handler=UploadHandler,
        methods=['GET', 'POST']
    ), webapp2.Route(
        '/files/<fileId>',
        handler=DownloadHandler,
        methods=['GET']
    )
])
