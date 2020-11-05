from zerobrowse import app
from flask import render_template, request, redirect, url_for
from zerobrowse.browser.browser import ZeroconfBrowser
import zeroconf
import json

zero_browser = ZeroconfBrowser ()
@app.context_processor
def inject_stage_and_region():
    return dict(servicestat=zero_browser.get_service_stat ())

@app.route("/")
def page_home():
    return render_template('index.html')


@app.route("/data/scan")
def data_scanner ():
    scanned = zeroconf.ZeroconfServiceTypes.find()
    return json.dumps (scanned), 200

@app.route("/scanajax")
def page_scanajax ():
    return render_template("scanajax.html")

@app.route("/browserajax/<servicename>")
def page_browserajax(servicename=None):

    return render_template('browserajax.html', servicename=servicename)

@app.route("/data/browser/<servicequery>")
def data_browser(servicequery = None):
    services = zero_browser.browser_list.keys()
    host_services = []
    if servicequery:
        brutservices = zero_browser.get_services_from_type(servicequery)

        return json.dumps(brutservices), 200

    return "",406

@app.route("/data/register", methods=['GET','POST'])
def data_register ():
    if request.method == 'POST':
        data = request.form.to_dict()
        print (data)
        for k,v in data.items():
            if v == 'on':
                zero_browser.add_listener(k)
        with open('config.json', 'w', encoding="utf-8") as file:
            file.write (zero_browser.dump_to_json())

        return redirect(url_for ('page_scanajax'))
    return '',404

