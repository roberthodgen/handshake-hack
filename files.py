from google.appengine.ext import blobstore

from google.appengine.ext.webapp import blobstore_handlers

import webapp2

import json




class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        """ Return an upload URL. """
        upload_url = blobstore.create_upload_url('/', gs_bucket_name='handshake-resume-cnd/resumes/')
        response_object = {}
        response_object['upload_url']= upload_url
        self.response.content_type = 'application/json'
        self.response.out.write(json.dumps(response_object))

    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        self.redirect('/serve/%s' % blob_info.key())


app = webapp2.WSGIApplication([
    webapp2.Route(
        '/upload',
        handler=UploadHandler,
        methods=['GET', 'POST']
    )
])