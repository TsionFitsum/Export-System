from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import json  
from flask import url_for
from datetime import datetime 
   


app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdataaam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

# Define the model for the form data
class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.String(100), nullable=False)
    contract_no = db.Column(db.String(100), nullable=False)
    cert_no = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(100), nullable=False)
    buyer = db.Column(db.String(100), nullable=False)
    invoice_value = db.Column(db.Float, nullable=False)
    payment_term = db.Column(db.String(50), nullable=False)
    seal_image = db.Column(db.String(200), nullable=True)
    undertaking_image = db.Column(db.String(200), nullable=True)
    documentary_credit = db.Column(db.String(200), nullable=True)
    bags = db.Column(db.String(200), nullable=True)
    mts = db.Column(db.String(200), nullable=True)
    fcl = db.Column(db.String(200), nullable=True)
    clu_inspected_date = db.Column(db.String(200), nullable=True)
    clu_result = db.Column(db.String(200), nullable=True)
    destination = db.Column(db.String(200), nullable=True)
    permit_number = db.Column(db.String(200), nullable=True)
    lpco_number = db.Column(db.String(200), nullable=True)
    shipping_line = db.Column(db.String(200), nullable=True)
    pss_sample_date = db.Column(db.String(100), nullable=False)
    pss_sample_result_date = db.Column(db.String(100), nullable=False)
    pss_result = db.Column(db.String(50), nullable=False)
    pss_comment = db.Column(db.Text, nullable=True)
    booking_number = db.Column(db.String(100), nullable=False)
    booking_confirmation_image = db.Column(db.String(200), nullable=True)
    container_number = db.Column(db.String(100), nullable=False)
    container_image = db.Column(db.String(200), nullable=True)
    seal_number = db.Column(db.String(100), nullable=False)
    date_loaded_from_wh = db.Column(db.String(100), nullable=False)
    transitor_name = db.Column(db.String(100), nullable=False)
    transitor_operation_number = db.Column(db.String(100), nullable=False)
    insurance_company = db.Column(db.String(100), nullable=False)
    insurance_amount = db.Column(db.Float, nullable=False)
    truck_or_train_plate_number = db.Column(db.String(100), nullable=False)
    driver_phone_number = db.Column(db.String(100), nullable=False)
    djibouti_forwarder = db.Column(db.String(100), nullable=False)
    djibouti_forwarder_contact = db.Column(db.String(100), nullable=False)
    vessel_date = db.Column(db.String(100), nullable=False)
    vessel_name = db.Column(db.String(100), nullable=False)
    bill_no = db.Column(db.String(100), nullable=False)
    date_received_obl = db.Column(db.String(100), nullable=False)
    date_docs_sent_to_bank = db.Column(db.String(100), nullable=False)
    docs_awb_number = db.Column(db.String(100), nullable=False)
    date_credit_advice_received = db.Column(db.String(100), nullable=False)
    payment_status = db.Column(db.String(100), nullable=False)
    amount_settled = db.Column(db.Float, nullable=False)
    bank = db.Column(db.String(100), nullable=False)
    ecd_number = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    remark = db.Column(db.String(100), nullable=False)
    railway_bill_image = db.Column(db.String(200), nullable=True)
    payment_receipt_image = db.Column(db.String(200), nullable=True)
    trackway_bill_image = db.Column(db.String(200), nullable=True)
    nb_contract_image = db.Column(db.String(200), nullable=True)
    commercial_invoice_image = db.Column(db.String(200), nullable=True)
    pl_image = db.Column(db.String(200), nullable=True)
    vgm_image = db.Column(db.String(200), nullable=True)
    payment_recieptt_image = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<FormData {self.no}, {self.contract_no}>'



class FormDataHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_data_id = db.Column(db.Integer, db.ForeignKey('form_data.id'), nullable=False)
    old_data = db.Column(db.Text, nullable=False)  # Store the full form data as JSON
    modified_at = db.Column(db.DateTime, nullable=False, default=db.func.now())  # Timestamp of change

    def __repr__(self):
        return f'<FormDataHistory {self.id} for FormData {self.form_data_id}>'

        

@app.route('/list_items', methods=['GET'])
def list_items():
    items = FormData.query.all()  # Assuming FormData contains all your item details
    return render_template('list.html', items=items)





# Route to display the form
@app.route('/')
def form():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data from the request
    no = request.form.get('no', '')
    contract_no = request.form.get('contract_no', '')
    cert_no = request.form.get('cert_no', '')
    grade = request.form.get('grade', '')
    buyer = request.form.get('buyer', '')
    invoice_value = request.form.get('invoice_value', type=float)
    payment_term = request.form.get('payment_term', '')
    bags = request.form.get('bags', '')
    mts = request.form.get('mts', '')
    fcl = request.form.get('fcl', '')
    clu_inspected_date = request.form.get('clu_inspected_date', '')
    clu_result = request.form.get('clu_result', '')
    destination = request.form.get('destination', '')
    permit_number = request.form.get('permit_number', '')
    lpco_number = request.form.get('lpco_number', '')
    shipping_line = request.form.get('shipping_line', '')
    pss_sample_date = request.form.get('pss_sample_date', '')
    pss_sample_result_date = request.form.get('pss_sample_result_date', '')
    pss_result = request.form.get('pss_result', '')
    pss_comment = request.form.get('pss_comment', '')
    booking_number = request.form.get('booking_number', '')
    container_number = request.form.get('container_number', '')
    seal_number = request.form.get('seal_number', '')
    date_loaded_from_wh = request.form.get('date_loaded_from_wh', '')
    transitor_name = request.form.get('transitor_name', '')
    transitor_operation_number = request.form.get('transitor_operation_number', '')
    insurance_company = request.form.get('insurance_company', '')
    insurance_amount = request.form.get('insurance_amount', type=float)
    truck_or_train_plate_number = request.form.get('truck_or_train_plate_number', '')
    driver_phone_number = request.form.get('driver_phone_number', '')
    djibouti_forwarder = request.form.get('djibouti_forwarder', '')
    djibouti_forwarder_contact = request.form.get('djibouti_forwarder_contact', '')
    vessel_date = request.form.get('vessel_date', '')
    vessel_name = request.form.get('vessel_name', '')
    bill_no = request.form.get('bill_no', '')
    date_received_obl = request.form.get('date_received_obl', '')
    date_docs_sent_to_bank = request.form.get('date_docs_sent_to_bank', '')
    docs_awb_number = request.form.get('docs_awb_number', '')
    date_credit_advice_received = request.form.get('date_credit_advice_received', '')
    payment_status = request.form.get('payment_status', '')
    amount_settled = request.form.get('amount_settled', type=float)
    bank = request.form.get('bank', '')
    ecd_number = request.form.get('ecd_number', '')
    status = request.form.get('status', '')
    remark = request.form.get('remark', '')

    # Handle file uploads
    def save_file(file):
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return filename
        return None

    seal_image = save_file(request.files.get('seal_image'))
    undertaking_image = save_file(request.files.get('undertaking_image'))
    documentary_credit = request.form.get('documentary_credit', '')
    booking_confirmation_image = save_file(request.files.get('booking_confirmation_image'))
    container_image = save_file(request.files.get('container_image'))
    railway_bill_image = save_file(request.files.get('railway_bill_image'))
    payment_receipt_image = save_file(request.files.get('payment_receipt_image'))
    trackway_bill_image = save_file(request.files.get('trackway_bill_image'))
    nb_contract_image = save_file(request.files.get('nb_contract_image'))
    commercial_invoice_image = save_file(request.files.get('commercial_invoice_image'))
    pl_image = save_file(request.files.get('pl_image'))
    vgm_image = save_file(request.files.get('vgm_image'))
    payment_recieptt_image = save_file(request.files.get('payment_recieptt_image'))

    # Check if the form data already exists
    form_data = FormData.query.filter_by(no=no).first()

    if form_data:
        # Create a snapshot of the existing data for history
        old_data = {
            'no': form_data.no,
            'contract_no': form_data.contract_no,
            'cert_no': form_data.cert_no,
            'grade': form_data.grade,
            'buyer': form_data.buyer,
            'invoice_value': form_data.invoice_value,
            'payment_term': form_data.payment_term,
            'bags': form_data.bags,
            'mts': form_data.mts,
            'fcl': form_data.fcl,
            'clu_inspected_date': form_data.clu_inspected_date,
            'clu_result': form_data.clu_result,
            'destination': form_data.destination,
            'permit_number': form_data.permit_number,
            'lpco_number': form_data.lpco_number,
            'shipping_line': form_data.shipping_line,
            'pss_sample_date': form_data.pss_sample_date,
            'pss_sample_result_date': form_data.pss_sample_result_date,
            'pss_result': form_data.pss_result,
            'pss_comment': form_data.pss_comment,
            'booking_number': form_data.booking_number,
            'container_number': form_data.container_number,
            'seal_number': form_data.seal_number,
            'date_loaded_from_wh': form_data.date_loaded_from_wh,
            'transitor_name': form_data.transitor_name,
            'transitor_operation_number': form_data.transitor_operation_number,
            'insurance_company': form_data.insurance_company,
            'insurance_amount': form_data.insurance_amount,
            'truck_or_train_plate_number': form_data.truck_or_train_plate_number,
            'driver_phone_number': form_data.driver_phone_number,
            'djibouti_forwarder': form_data.djibouti_forwarder,
            'djibouti_forwarder_contact': form_data.djibouti_forwarder_contact,
            'vessel_date': form_data.vessel_date,
            'vessel_name': form_data.vessel_name,
            'bill_no': form_data.bill_no,
            'date_received_obl': form_data.date_received_obl,
            'date_docs_sent_to_bank': form_data.date_docs_sent_to_bank,
            'docs_awb_number': form_data.docs_awb_number,
            'date_credit_advice_received': form_data.date_credit_advice_received,
            'payment_status': form_data.payment_status,
            'amount_settled': form_data.amount_settled,
            'bank': form_data.bank,
            'ecd_number': form_data.ecd_number,
            'status': form_data.status,
            'remark': form_data.remark,
        }

        # Log the old data to history
        form_history = FormDataHistory(
            form_data_id=form_data.id, 
            old_data=json.dumps(old_data)
        )
        db.session.add(form_history)

        # Update existing record with new values
        form_data.contract_no = contract_no
        form_data.cert_no = cert_no
        form_data.grade = grade
        form_data.buyer = buyer
        form_data.invoice_value = invoice_value
        form_data.payment_term = payment_term
        form_data.bags = bags
        form_data.mts = mts
        form_data.fcl = fcl
        form_data.clu_inspected_date = clu_inspected_date
        form_data.clu_result = clu_result
        form_data.destination = destination
        form_data.permit_number = permit_number
        form_data.lpco_number = lpco_number
        form_data.shipping_line = shipping_line
        form_data.pss_sample_date = pss_sample_date
        form_data.pss_sample_result_date = pss_sample_result_date
        form_data.pss_result = pss_result
        form_data.pss_comment = pss_comment
        form_data.booking_number = booking_number
        form_data.container_number = container_number
        form_data.seal_number = seal_number
        form_data.date_loaded_from_wh = date_loaded_from_wh
        form_data.transitor_name = transitor_name
        form_data.transitor_operation_number = transitor_operation_number
        form_data.insurance_company = insurance_company
        form_data.insurance_amount = insurance_amount
        form_data.truck_or_train_plate_number = truck_or_train_plate_number
        form_data.driver_phone_number = driver_phone_number
        form_data.djibouti_forwarder = djibouti_forwarder
        form_data.djibouti_forwarder_contact = djibouti_forwarder_contact
        form_data.vessel_date = vessel_date
        form_data.vessel_name = vessel_name
        form_data.bill_no = bill_no
        form_data.date_received_obl = date_received_obl
        form_data.date_docs_sent_to_bank = date_docs_sent_to_bank
        form_data.docs_awb_number = docs_awb_number
        form_data.date_credit_advice_received = date_credit_advice_received
        form_data.payment_status = payment_status
        form_data.amount_settled = amount_settled
        form_data.bank = bank
        form_data.ecd_number = ecd_number
        form_data.status = status
        form_data.remark = remark
        form_data.seal_image = seal_image
        form_data.undertaking_image = undertaking_image
        form_data.documentary_credit = documentary_credit
        form_data.booking_confirmation_image = booking_confirmation_image
        form_data.container_image = container_image
        form_data.railway_bill_image = railway_bill_image
        form_data.payment_receipt_image = payment_receipt_image
        form_data.trackway_bill_image = trackway_bill_image
        form_data.nb_contract_image = nb_contract_image
        form_data.commercial_invoice_image = commercial_invoice_image
        form_data.pl_image = pl_image
        form_data.vgm_image = vgm_image
        form_data.payment_recieptt_image = payment_recieptt_image

    else:
        # Create a new form data entry
        form_data = FormData(
            no=no,
            contract_no=contract_no,
            cert_no=cert_no,
            grade=grade,
            buyer=buyer,
            invoice_value=invoice_value,
            payment_term=payment_term,
            bags=bags,
            mts=mts,
            fcl=fcl,
            clu_inspected_date=clu_inspected_date,
            clu_result=clu_result,
            destination=destination,
            permit_number=permit_number,
            lpco_number=lpco_number,
            shipping_line=shipping_line,
            pss_sample_date=pss_sample_date,
            pss_sample_result_date=pss_sample_result_date,
            pss_result=pss_result,
            pss_comment=pss_comment,
            booking_number=booking_number,
            container_number=container_number,
            seal_number=seal_number,
            date_loaded_from_wh=date_loaded_from_wh,
            transitor_name=transitor_name,
            transitor_operation_number=transitor_operation_number,
            insurance_company=insurance_company,
            insurance_amount=insurance_amount,
            truck_or_train_plate_number=truck_or_train_plate_number,
            driver_phone_number=driver_phone_number,
            djibouti_forwarder=djibouti_forwarder,
            djibouti_forwarder_contact=djibouti_forwarder_contact,
            vessel_date=vessel_date,
            vessel_name=vessel_name,
            bill_no=bill_no,
            date_received_obl=date_received_obl,
            date_docs_sent_to_bank=date_docs_sent_to_bank,
            docs_awb_number=docs_awb_number,
            date_credit_advice_received=date_credit_advice_received,
            payment_status=payment_status,
            amount_settled=amount_settled,
            bank=bank,
            ecd_number=ecd_number,
            status=status,
            remark=remark,
            seal_image=seal_image,
            undertaking_image=undertaking_image,
            documentary_credit=documentary_credit,
            booking_confirmation_image=booking_confirmation_image,
            container_image=container_image,
            railway_bill_image=railway_bill_image,
            payment_receipt_image=payment_receipt_image,
            trackway_bill_image=trackway_bill_image,
            nb_contract_image=nb_contract_image,
            commercial_invoice_image=commercial_invoice_image,
            pl_image=pl_image,
            vgm_image=vgm_image,
            payment_recieptt_image=payment_recieptt_image
        )
        db.session.add(form_data)

    db.session.commit()
    return redirect(url_for('list_items'))  # Change 'success' to your success endpoint


@app.route('/history/<int:form_data_id>/json', methods=['GET'])
def view_history(form_data_id):
    history = FormDataHistory.query.filter_by(form_data_id=form_data_id).order_by(FormDataHistory.modified_at.desc()).all()

    if not history:
        return jsonify({"error": "No history found"})

    # Prepare history data for JSON response
    history_data = []
    for entry in history:
        history_data.append({
            "modified_at": entry.modified_at.strftime('%Y-%m-%d %H:%M:%S'),
            "old_data": json.loads(entry.old_data)
        })

    return jsonify(history_data)














@app.route('/history/<string:contract_no>/json', methods=['GET'])
def view_history_json(contract_no):
    # Find the form_data record that corresponds to the provided contract_no
    form_data = FormData.query.filter_by(contract_no=contract_no).first()
    
    if not form_data:
        # Return an error if no form_data found with that contract_no
        return jsonify({"error": "No form data found for the given contract number"}), 404
    
    # Now fetch the history using form_data_id
    history_entries = FormDataHistory.query.filter_by(form_data_id=form_data.id).order_by(FormDataHistory.modified_at.desc()).all()
    
    if not history_entries:
        return jsonify({"error": "No history found for this contract"}), 404
    
    # Format the history data for the response
    history_data = []
    for entry in history_entries:
        history_data.append({
            "modified_at": entry.modified_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format timestamp
            "old_data": json.dumps(json.loads(entry.old_data), indent=4)  # Pretty-print old data
        })
    
    # Return the formatted history data as a JSON response
    return jsonify(history_data)




@app.route('/edit/<string:contract_no>', methods=['GET', 'POST'])
def edit_item(contract_no):
    # Fetch the existing form data (item) by contract_no
    form_data = FormData.query.filter_by(contract_no=contract_no).first()

    if request.method == 'POST':
        if form_data:  # If the item exists, create a history entry
            # Serialize the current state of the item into a JSON object
            old_data_json = json.dumps({
                "contract_no": form_data.contract_no,
                "cert_no": form_data.cert_no,
                "grade": form_data.grade,
                "buyer": form_data.buyer,
                "invoice_value": form_data.invoice_value,
                "payment_term": form_data.payment_term,
                "seal_image": form_data.seal_image,
                "undertaking_image": form_data.undertaking_image,
                "documentary_credit": form_data.documentary_credit,
                "bags": form_data.bags,
                "mts": form_data.mts,
                "fcl": form_data.fcl,
                "clu_inspected_date": form_data.clu_inspected_date,
                "clu_result": form_data.clu_result,
                "destination": form_data.destination,
                "permit_number": form_data.permit_number,
                "lpco_number": form_data.lpco_number,
                "shipping_line": form_data.shipping_line,
                "pss_sample_date": form_data.pss_sample_date,
                "pss_sample_result_date": form_data.pss_sample_result_date,
                "pss_result": form_data.pss_result,
                "pss_comment": form_data.pss_comment,
                "booking_number": form_data.booking_number,
                "booking_confirmation_image": form_data.booking_confirmation_image,
                "container_number": form_data.container_number,
                "container_image": form_data.container_image,
                "seal_number": form_data.seal_number,
                "date_loaded_from_wh": form_data.date_loaded_from_wh,
                "transitor_name": form_data.transitor_name,
                "transitor_operation_number": form_data.transitor_operation_number,
                "insurance_company": form_data.insurance_company,
                "insurance_amount": form_data.insurance_amount,
                "truck_or_train_plate_number": form_data.truck_or_train_plate_number,
                "driver_phone_number": form_data.driver_phone_number,
                "djibouti_forwarder": form_data.djibouti_forwarder,
                "djibouti_forwarder_contact": form_data.djibouti_forwarder_contact,
                "vessel_date": form_data.vessel_date,
                "vessel_name": form_data.vessel_name,
                "bill_no": form_data.bill_no,
                "date_received_obl": form_data.date_received_obl,
                "date_docs_sent_to_bank": form_data.date_docs_sent_to_bank,
                "docs_awb_number": form_data.docs_awb_number,
                "date_credit_advice_received": form_data.date_credit_advice_received,
                "payment_status": form_data.payment_status,
                "amount_settled": form_data.amount_settled,
                "bank": form_data.bank,
                "ecd_number": form_data.ecd_number,
                "status": form_data.status,
                "remark": form_data.remark,
                "railway_bill_image": form_data.railway_bill_image,
                "payment_receipt_image": form_data.payment_receipt_image,
                "trackway_bill_image": form_data.trackway_bill_image,
                "nb_contract_image": form_data.nb_contract_image,
                "commercial_invoice_image": form_data.commercial_invoice_image,
                "pl_image": form_data.pl_image,
                "vgm_image": form_data.vgm_image,
                "payment_recieptt_image": form_data.payment_recieptt_image
            })

            # Save the current state to FormDataHistory before updating the item
            history_entry = FormDataHistory(
                form_data_id=form_data.id,  # Reference the form_data primary key
                old_data=old_data_json,  # Store the serialized old data
                modified_at=datetime.utcnow()  # Capture the time of the change
            )
            db.session.add(history_entry)

        # If form_data does not exist, create a new FormData object
        if not form_data:
            form_data = FormData(contract_no=contract_no)

        # Update the fields based on form input
        form_data.cert_no = request.form.get('cert_no', '')
        form_data.grade = request.form.get('grade', '')
        form_data.buyer = request.form.get('buyer', '')
        form_data.invoice_value = request.form.get('invoice_value', type=float)
        form_data.payment_term = request.form.get('payment_term', '')
        form_data.seal_image = request.form.get('seal_image', '')
        form_data.undertaking_image = request.form.get('undertaking_image', '')
        form_data.documentary_credit = request.form.get('documentary_credit', '')
        form_data.bags = request.form.get('bags', '')
        form_data.mts = request.form.get('mts', '')
        form_data.fcl = request.form.get('fcl', '')
        form_data.clu_inspected_date = request.form.get('clu_inspected_date', '')
        form_data.clu_result = request.form.get('clu_result', '')
        form_data.destination = request.form.get('destination', '')
        form_data.permit_number = request.form.get('permit_number', '')
        form_data.lpco_number = request.form.get('lpco_number', '')
        form_data.shipping_line = request.form.get('shipping_line', '')
        form_data.pss_sample_date = request.form.get('pss_sample_date', '')
        form_data.pss_sample_result_date = request.form.get('pss_sample_result_date', '')
        form_data.pss_result = request.form.get('pss_result', '')
        form_data.pss_comment = request.form.get('pss_comment', '')
        form_data.booking_number = request.form.get('booking_number', '')
        form_data.booking_confirmation_image = request.form.get('booking_confirmation_image', '')
        form_data.container_number = request.form.get('container_number', '')
        form_data.container_image = request.form.get('container_image', '')
        form_data.seal_number = request.form.get('seal_number', '')
        form_data.date_loaded_from_wh = request.form.get('date_loaded_from_wh', '')
        form_data.transitor_name = request.form.get('transitor_name', '')
        form_data.transitor_operation_number = request.form.get('transitor_operation_number', '')
        form_data.insurance_company = request.form.get('insurance_company', '')
        form_data.insurance_amount = request.form.get('insurance_amount', type=float)
        form_data.truck_or_train_plate_number = request.form.get('truck_or_train_plate_number', '')
        form_data.driver_phone_number = request.form.get('driver_phone_number', '')
        form_data.djibouti_forwarder = request.form.get('djibouti_forwarder', '')
        form_data.djibouti_forwarder_contact = request.form.get('djibouti_forwarder_contact', '')
        form_data.vessel_date = request.form.get('vessel_date', '')
        form_data.vessel_name = request.form.get('vessel_name', '')
        form_data.bill_no = request.form.get('bill_no', '')
        form_data.date_received_obl = request.form.get('date_received_obl', '')
        form_data.date_docs_sent_to_bank = request.form.get('date_docs_sent_to_bank', '')
        form_data.docs_awb_number = request.form.get('docs_awb_number', '')
        form_data.date_credit_advice_received = request.form.get('date_credit_advice_received', '')
        form_data.payment_status = request.form.get('payment_status', '')
        form_data.amount_settled = request.form.get('amount_settled', type=float)
        form_data.bank = request.form.get('bank', '')
        form_data.ecd_number = request.form.get('ecd_number', '')
        form_data.status = request.form.get('status', 'Draft')  # Example: Draft or Done
        form_data.remark = request.form.get('remark', '')
        form_data.railway_bill_image = request.form.get('railway_bill_image', '')
        form_data.payment_receipt_image = request.form.get('payment_receipt_image', '')
        form_data.trackway_bill_image = request.form.get('trackway_bill_image', '')
        form_data.nb_contract_image = request.form.get('nb_contract_image', '')
        form_data.commercial_invoice_image = request.form.get('commercial_invoice_image', '')
        form_data.pl_image = request.form.get('pl_image', '')
        form_data.vgm_image = request.form.get('vgm_image', '')
        form_data.payment_recieptt_image = request.form.get('payment_recieptt_image', '')

        # Save the updated item back to the database
        db.session.add(form_data)
        db.session.commit()

        return redirect(url_for('list_items'))  # Redirect after saving

    return render_template('edit_form.html', form_data=form_data)





if __name__ == '__main__':
    with app.app_context():  # Ensure that app context is available
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)