import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools


templateDocumentId = '1_fdQ-iutI51TmvzY8IHspbQyejzHpVDcjCEF7ff4ayI' # Please set the Document ID.

creds = 'credentials.json'

# authorization constants
CLIENT_ID_FILE = 'credentials.json'
TOKEN_STORE_FILE = 'token.json'
SCOPES = (  # iterable or space-delimited string
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
)


def get_http_client():
    """Uses project credentials in CLIENT_ID_FILE along with requested OAuth2
        scopes for authorization, and caches API tokens in TOKEN_STORE_FILE.
    """
    store = file.Storage(TOKEN_STORE_FILE)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_ID_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
    return creds.authorize(Http())


# service endpoints to Google APIs
HTTP = get_http_client()
DRIVE = discovery.build('drive', 'v3', http=HTTP)
DOCS = discovery.build('docs', 'v1', http=HTTP)
SHEETS = discovery.build('sheets', 'v4', http=HTTP)

def create_audit(company, seo_data):
    outputPDFFilename = f'{company}.pdf'  # Please set the output PDF filename.

    # 1. Copy template Document.
    copiedDoc = DRIVE.files().copy(fileId=templateDocumentId, body={'name': 'copiedTemplateDocument'}).execute()
    copiedDocId = copiedDoc.get('id')
    print('Done: 1. Copy template Document.')

    # 2. Update copied Document.
    requests1 = [
        {
          "replaceAllText": {
              "replaceText": seo_data['title'],
              "containsText": {
                  "text": '{{Title}}',
                  "matchCase": True
              },
          }
        },
    {
          "replaceAllText": {
                  "replaceText": seo_data['description'],
              "containsText": {
                  "text": '{{Description}}',
              },
          }
        },
    {
          "replaceAllText": {
              "replaceText": seo_data['headings'],
              "containsText": {
                  "text": '{{h_tags}}',
              }
        }
    },
    {
          "replaceAllText": {
              "replaceText": seo_data['keywords'],
              "containsText": {
                  "text": '{{Keyword_results}}',
              }
          }
        },
    {
          "replaceAllText": {
              "replaceText": seo_data['warnings'],
              "containsText": {
                  "text": '{{warning_results}}',
                  "matchCase": True
              }
        },
    },
    {
          "replaceAllText": {
              "replaceText": seo_data['wordcount'],
              "containsText": {
                  "text": '{{Wordcount}}',
                  "matchCase": True
              },
          }
        },
    ]
    result = DOCS.documents().batchUpdate(documentId=copiedDocId, body={'requests': requests1}).execute()
    print('Done: 2. Update copied Document.')

    # 3. Download the updated Document as PDF file.
    request = DRIVE.files().export_media(fileId=copiedDocId, mimeType='application/pdf')
    fh = io.FileIO(outputPDFFilename, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print('Download %d%%.' % int(status.progress() * 100))
    print('Done: 3. Download the updated Document as PDF file.')

    # 4. Send email of copied document

    # 5. Delete the copied Document.
    DRIVE.files().delete(fileId=copiedDocId).execute()
    print('Done: 4. Delete the copied Document.')

