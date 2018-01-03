# -*- coding: utf-8 -*-
from decimal import Decimal
from flask import Blueprint, request, jsonify, url_for, abort

bpauction = Blueprint('auction', __name__, template_folder='templates')
import application.model as model
from application.application import async


@async
def on_auction_creation(auction):
    accounts = model.account_list()
    if not accounts:
        return

    mail = model.mail_create(
        message='New auction created. Join at %s' % auction['uri'],
        subject='New auction created',
        sender=model.cfg.get('MAIL_USERNAME'),
        recipients=[x['email'] for x in accounts]
    )
    print mail
    model.mail_send([mail])


@async
def on_bid_creation(bidder_id, auction, bid):
    bidders = model.auction_bidders_list(auction['id'])
    mails = [
        model.mail_create(
            message='New bid created for auction: %s, bid: %s' % (auction['uri'], bid['bid_value']),
            subject='New bid created',
            sender=model.cfg.get('MAIL_USERNAME'),
            recipients=[x['email']]
        ) for x in bidders if x['id'] != bidder_id
    ]
    if mails:
        model.mail_send(mails)


@bpauction.route('/auction', methods=['GET'])
def auction_list():
    status = request.json.get('status') if request.json else None
    auctions = model.auction_list(status=status)
    for a in auctions:
        a['uri'] = url_for('.auction_get', auction_id=a['id'], _external=True)
    return jsonify({'data': auctions})


@bpauction.route('/auction', methods=['POST'])
def auction_create():
    if not request.json:
        abort(400)
    for fld in ('description', 'bid_start', 'bid_step', 'finish_date'):
        if not request.json.get(fld):
            return jsonify({'error': 'Missing required fields: description, bid_start, bid_step, finish_date'}), 400

    try:
        if float(request.json['bid_start'] < 0) or float(request.json['bid_step'] <= 0):
            return jsonify({
                'error': 'Bid start value must be non-negative, bid step must be positive. Got %0.2f and %0.2f' % (request.json['bid_start'], request.json['bid_step'])
            }), 400
    except Exception:
        return jsonify({
            'error': 'Bid start value must be non-negative, bid step must be positive. Got %s and %s' % (request.json['bid_start'], request.json['bid_step'])
        }), 400

    user = model.get_user_by_token(request.headers.get('Authorization'))
    if not user:
        abort(403)

    auction = model.auction_create(
        description=request.json['description'],
        bid_start=request.json['bid_start'],
        bid_step=request.json['bid_step'],
        finish_date=request.json['finish_date'],
        account_id=user['id']
    )
    auction['uri'] = url_for('.auction_get', auction_id=auction['id'], _external=True)
    on_auction_creation(auction)

    return jsonify({
        'id': auction['id'],
        'uri': auction['uri'],
        'bids': url_for('.auction_place_bid', auction_id=auction['id'], _external=True),
    })


@bpauction.route('/auction/<auction_id>/bid', methods=['POST'])
def auction_place_bid(auction_id):
    bid_value = request.json.get('bid')
    try:
        bid_value = Decimal(bid_value)
        if bid_value <= 0:
            return jsonify({'error': 'Bid must positive float. Got %0.2f' % bid_value}), 400
    except Exception:
        return jsonify({'error': 'Bid must positive float. Got %s' % bid_value}), 400

    user = model.get_user_by_token(request.headers.get('Authorization'))
    if not user:
        abort(403)

    auction = model.auction_get(auction_id=auction_id)
    if not auction:
        abort(404)

    if user['id'] == auction['account_id']:
        return jsonify({'error': 'Can not make a bin on belonging auction'}), 403
    if auction['status'] != 'active':
        return jsonify({'error': 'Can not make a bin on finished auction'}), 400

    bids = model.auction_get_bids(auction_id=auction_id)
    bid_values = sorted((x['bid_value'] for x in bids), reverse=True)
    max_bid = bid_values[0] if bid_values else auction['bid_start']
    if max_bid >= bid_value:
        return jsonify({'error': 'Bid must be greater than %0.2f' % max_bid}), 400
    if (bid_value - max_bid) % auction['bid_step']:
        return jsonify({'error': 'Bid must be multiple of %0.2f starting from %0.2f' % (auction['bid_step'], auction['bid_start'])}), 400

    bid = model.auction_place_bid(auction_id=auction_id, bid=bid_value, account_id=user['id'])
    auction['uri'] = url_for('.auction_get', auction_id=auction['id'], _external=True)
    on_bid_creation(bidder_id=user['id'], auction=auction, bid=bid)

    return jsonify({'prev_bid_value': max_bid, 'bid_step': auction['bid_step'], 'bid': bid})


@bpauction.route('/auction/<auction_id>', methods=['GET'])
def auction_get(auction_id):
    auction = model.auction_get(auction_id=auction_id)
    if not auction:
        abort(404)
    del auction['account_id']
    auction['uri'] = url_for('.auction_get', auction_id=auction['id'], _external=True)
    auction['bids'] = {
        'uri': url_for('.auction_place_bid', auction_id=auction['id'], _external=True),
        'data': model.auction_get_bids(auction_id=auction['id'])
    }
    return jsonify(auction)
