from flask_restx import Namespace, Resource
from website.api_models import message

guest_ns = Namespace("guest", description="Demonstration of a unprotected resource")

@guest_ns.route("/message")
class Message(Resource):
    @guest_ns.marshal_with(message)
    def get(self):
        return {"message": "Mám tu odezvu z /message, která je dostupná vždy."}