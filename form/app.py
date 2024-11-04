import json
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta
from flask_apscheduler import APScheduler
import logging

# Set up logging to display debugging information
logging.basicConfig(level=logging.DEBUG)


# Create the Flask app
app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdatam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Define the expiration check function
def check_for_expiring_forms():
    with app.app_context():
        # Debugging line to confirm function entry
        print("Running expiration check...")
        
        # Set the dates for expired and expiring soon statuses
        expiration_date = datetime.utcnow() - timedelta(days=1)  # 1 day for testing purposes
        expiration_warning_date = datetime.utcnow() - timedelta(days=0.5)  # e.g., 12 hours for testing "expiring soon"

        # Expired forms check
        expired_forms = FormData.query.filter(
            FormData.created_at <= expiration_date,
            FormData.status != 'Expired'
        ).all()

        # Expiring soon forms check
        expiring_forms = FormData.query.filter(
            FormData.created_at <= expiration_warning_date,
            FormData.status != 'Expired'
        ).all()

        # Update expired forms
        for form in expired_forms:
            print(f"Form {form.no} with Contract No {form.contract_no} has expired.")
            form.status = 'Expired'

        # Update expiring soon forms
        for form in expiring_forms:
            print(f"Form {form.no} with Contract No {form.contract_no} is expiring soon.")
            if form.status != 'Expired':  # Ensure it’s not overwritten
                form.status = 'Expiring Soon'

        # Commit changes once after all updates
        db.session.commit()
        print("Expiration check completed.")



# Initialize the scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Add the expiration check job to run daily
scheduler.add_job(id='Expiration Check', func=check_for_expiring_forms, trigger='interval', days=1)



# Rest of your app configuration and routes...

# Configure the SQLite database


# Initialize the database with the Flask app
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
    status = db.Column(db.String(100), nullable=False, default='Draft')  # Status starts as Draft
    remark = db.Column(db.String(100), nullable=False)
    railway_bill_image = db.Column(db.String(200), nullable=True)
    payment_receipt_image = db.Column(db.String(200), nullable=True)
    trackway_bill_image = db.Column(db.String(200), nullable=True)
    nb_contract_image = db.Column(db.String(200), nullable=True)
    commercial_invoice_image = db.Column(db.String(200), nullable=True)
    pl_image = db.Column(db.String(200), nullable=True)
    vgm_image = db.Column(db.String(200), nullable=True)
    payment_recieptt_image = db.Column(db.String(200), nullable=True)

    # New fields for tracking creation and updating expiration status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Track when form is created
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Track when form is updated

    # Method to check if form is expired
    def is_expired(self):
        expiration_date = self.created_at + timedelta(days=90)  # Expire after 3 months
        return datetime.utcnow() > expiration_date

    def __repr__(self):
        return f'<FormData {self.no}, {self.contract_no}>'

# Route to display form data (for example)
# @app.route('/')
# def index():
#     form_data_list = FormData.query.all()
#     return render_template('index.html', form_data_list=form_data_list)

# Initialize the database tables
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()  # Create tables if they don't exist
#     app.run(debug=True)

@app.route('/test-expiration')
def test_expiration():
    check_for_expiring_forms()
    return "Expiration check complete."



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



from datetime import datetime



@app.route('/edit/<string:contract_no>', methods=['GET', 'POST'])
def edit_item(contract_no):
    # Fetch the existing form data by contract_no
    form_data = FormData.query.filter_by(contract_no=contract_no).first()

    if request.method == 'POST':
        if form_data:  # If the item exists, create a history entry
            # Dynamically serialize current state of the item into a JSON object
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
    "payment_recieptt_image": form_data.payment_recieptt_image,
    "created_at": form_data.created_at
            }, default=str)  # `default=str` handles datetime serialization
            # Save the current state to FormDataHistory before updating the item
            
            # Save the current state to FormDataHistory before updating the item
            history_entry = FormDataHistory(
                form_data_id=form_data.id,
                old_data=old_data_json,
                modified_at=datetime.utcnow()
            )
            db.session.add(history_entry)

        else:
            form_data = FormData(contract_no=contract_no)

        # Define datetime fields and validate them
        datetime_fields = ["clu_inspected_date", "pss_sample_date", "pss_sample_result_date", 
                           "date_loaded_from_wh", "vessel_date", "date_received_obl", 
                           "date_docs_sent_to_bank", "date_credit_advice_received", "updated_at"]

        for field in form_data.__table__.columns.keys():
            if field != "id" and field != "created_at":
                form_value = request.form.get(field, '')

                if field in ["invoice_value", "insurance_amount", "amount_settled"]:
                    # Convert to float or set to None if empty
                    setattr(form_data, field, float(form_value) if form_value else None)
                elif field in datetime_fields:
                    # Parse datetime or set to None if empty
                    if form_value:
                        try:
                            parsed_date = datetime.strptime(form_value, '%Y-%m-%d')
                            setattr(form_data, field, parsed_date)
                        except ValueError:
                            logging.error(f"Invalid date format for {field}: {form_value}")
                            setattr(form_data, field, None)
                    else:
                        setattr(form_data, field, None)
                else:
                    setattr(form_data, field, form_value)

        # Ensure 'status' and 'updated_at' get valid defaults
        form_data.status = request.form.get('status', 'Draft')
        form_data.updated_at = datetime.utcnow()  # Automatically set `updated_at` to current timestamp

        # Save the updated item back to the database
        db.session.add(form_data)
        db.session.commit()

        return redirect(url_for('list_items'))

    return render_template('edit_form.html', form_data=form_data)



@app.route('/get_contract_numbers')
def get_contract_numbers():
    contract_numbers = [form.contract_no for form in FormData.query.all()]
    return jsonify(contract_numbers)


@app.route('/check_contract_no', methods=['POST'])
def check_contract_no():
    data = request.get_json()
    contract_no = data.get("contract_no")
    # Query the database to see if the contract number already exists
    existing_form = FormData.query.filter_by(contract_no=contract_no).first()
    return jsonify({"exists": bool(existing_form)}) 



@scheduler.task('interval', hours=24)  # Runs every 24 hours
def check_expiring_forms():
    expiring_forms = FormData.query.filter(
        FormData.created_at <= datetime.utcnow() - timedelta(days=83)  # 7 days left
    ).all()
    for form in expiring_forms:
        notify_user(form)


if __name__ == '__main__':
    with app.app_context():  # Ensure that app context is available
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)