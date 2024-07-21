from flask_restx import Namespace, Resource

guest_ns = Namespace("guest", description="Demonstration of a unprotected resource")

@guest_ns.route("/message")
class Message(Resource):
    def get(self):
        return {"message": "Mám tu odezvu z /message, která je dostupná vždy."}