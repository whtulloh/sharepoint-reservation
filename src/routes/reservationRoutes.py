from flask import Blueprint
from src.controllers.reservationController import getData, updateData, getAllData, getHook

reservationBlueprint = Blueprint('blueprintt', __name__)

reservationBlueprint.route('/hook', methods=['GET'])(getHook)
reservationBlueprint.route('/all', methods=['GET'])(getAllData)
reservationBlueprint.route('/<accnumber>', methods=['GET'])(getData)
reservationBlueprint.route('/<accnumber>', methods=['PUT'])(updateData)
