import threading

from flask import Flask, jsonify, request, abort

from src.pygennf_v9_multi_threads import get_flow_data_list, DEFAULT_FLOW_DATA, start_send

app = Flask(__name__)

@app.route('/')
def help():
    return jsonify(
        # 'API (application/json)': 'PATH, notes ?org-id=<orgId> currently required',
        {'Cache clean': '/marketing/cache/clean?org-ids=<org-ids>',
         'Cache clean and rebuild': '/marketing/cache/clean-rebuild?org-ids=<org-ids>&rebuild-table=true',
         'Cache status': '/marketing/cache/status',
         'On board': '/marketing/onboard?org-ids=<org-ids>',
         'On board status': '/marketing/onboard/status',
         'Delayed scheduled rebuild task': 'add:/marketing/cache/rebuild/operation?opt=add&org-ids=<org-ids> '
                                           'delete:/marketing/cache/rebuild/operation?opt=delete&org-ids=<org-ids>',
         'Delayed task status': '/marketing/cache/rebuild/status?org-id=<org-ids>'
         })


@app.route('/pygennf/send', methods=['POST'])
def send():
    print "send() invoked..."
    if not request.json:
        abort(404)
    print request.json
    ip_src = request.json['ip_src']
    print 'ip_src: %s' % ip_src
    ip_dst = request.json['ip_dst']
    print 'ip_dst: %s' % ip_dst
    port_src = int(request.json['port_src'])
    print 'port_src: ', port_src
    port_dst = int(request.json['port_dst'])
    print 'port_dst: ', port_dst
    flow_data_list = get_flow_data_list(request.json['flows-data'], DEFAULT_FLOW_DATA)
    print 'flow_data_list: %s' % flow_data_list
    pkt_count = int(request.json['pkt_count'])
    print 'pkt_count:', pkt_count
    time_interval = request.json['time_interval']
    print 'time_interval: %s' % time_interval
    print 'Thread %s is running...' % threading.current_thread().name
    t = threading.Thread(target=start_send, name='SendingThread', args=(ip_src, ip_dst, port_src, port_dst,
                                                                        flow_data_list, pkt_count, time_interval))
    # t.do_run = True
    # t.setDaemon(True)
    t.start()
    while True:
        t.join(5)
        if not t.isAlive():
            break

    print 'Thread %s ended.' % threading.current_thread().name


@app.route('/pygennf/status')
def status():
    pass


def start():
    app.run(host='0.0.0.0', port=9080)
