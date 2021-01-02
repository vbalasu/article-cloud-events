from chalice import Chalice, Response
from boto3.session import Session

app = Chalice(app_name='chalice-cloud-events')
app.experimental_feature_flags.update(['WEBSOCKETS'])
app.websocket_api.session = Session()

@app.route('/')
def index():
    with open('chalicelib/index.html') as f:
        return Response(body=f.read(), status_code=200, headers={'Content-Type': 'text/html'})


@app.on_s3_event(bucket='cloudmatica',
                 events=['s3:ObjectCreated:*'])
def handle_object_created(event):
    import boto3
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url('get_object', Params={'Bucket':event.bucket, 'Key':event.key})
    print(url)
    
@app.on_ws_message()
def message(event):
    app.websocket_api.send(event.connection_id, 'I got your message!')
    

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
