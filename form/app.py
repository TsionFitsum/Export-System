from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdataaa.db'
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

# Route to display the form
@app.route('/')
def form():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    no = request.form.get('no', '')
    contract_no = request.form.get('contract_no', '')
    cert_no = request.form.get('cert_no', '')
    grade = request.form.get('grade', '')
    buyer = request.form.get('buyer', '')
    bags = request.form.get('bags', '')
    invoice_value = request.form.get('invoice_value', type=float)
    payment_term = request.form.get('payment_term', '')
    pss_sample_date = request.form.get('pss_sample_date', '')
    pss_sample_result_date = request.form.get('pss_sample_result_date', '')
    pss_result = request.form.get('pss_result', '')
    pss_comment = request.form.get('pss_comment', '')
    booking_number = request.form.get('booking_number', '')
    container_number = request.form.get('container_number', '')
    seal_number = request.form.get('seal_number', '')
    documentary_credit = request.form.get('documentary_credit', '')
    mts = request.form.get('mts', '')
    fcl = request.form.get('fcl', '')
    clu_inspected_date = request.form.get('clu_inspected_date', '')
    clu_result = request.form.get('clu_result', '')
    destination = request.form.get('destination', '')
    permit_number = request.form.get('permit_number', '')
    lpco_number = request.form.get('lpco_number', '')
    shipping_line = request.form.get('shipping_line', '')
    
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

    railway_bill_filename = save_file(request.files.get('railway_bill_image'))
    payment_receipt_filename = save_file(request.files.get('payment_receipt_image'))
    trackway_bill_filename = save_file(request.files.get('trackway_bill_image'))
    nb_contract_filename = save_file(request.files.get('nb_contract_image'))
    commercial_invoice_filename = save_file(request.files.get('commercial_invoice_image'))
    pl_filename = save_file(request.files.get('pl_image'))
    vgm_filename = save_file(request.files.get('vgm_image'))
    seal_filename = save_file(request.files.get('seal_image'))
    undertaking_filename = save_file(request.files.get('undertaking_image'))
    payment_recieptt_filename = save_file(request.files.get('payment_recieptt_image'))
    booking_confirmation_filename = save_file(request.files.get('booking_confirmation_image'))
    container_filename = save_file(request.files.get('container_image'))
    
    
    # seal_filename = save_file(request.files.get('seal_image'))
    # print(f"Seal image file path: {seal_filename}")  # Debugging
    
    # Create a new record and add it to the database
    new_entry = FormData(
        no=no,
        contract_no=contract_no,
        cert_no=cert_no,
        grade=grade,
        buyer=buyer,
        bags=bags,
        invoice_value=invoice_value,
        payment_term=payment_term,
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
        date_docs_sent_to_bank=date_docs_sent_to_bank,
        docs_awb_number=docs_awb_number,
        date_credit_advice_received=date_credit_advice_received,
        payment_status=payment_status,
        amount_settled=amount_settled,
        bank=bank,
        ecd_number=ecd_number,
        status=status,
        remark=remark,
        documentary_credit=documentary_credit,
        mts=mts,
        fcl=fcl,
        clu_inspected_date=clu_inspected_date,
        clu_result=clu_result,
        destination=destination,
        permit_number=permit_number,
        lpco_number=lpco_number,
        shipping_line=shipping_line,
        date_received_obl=date_received_obl,
        
        railway_bill_image=railway_bill_filename,
        payment_receipt_image=payment_receipt_filename,
        trackway_bill_image=trackway_bill_filename,
        nb_contract_image=nb_contract_filename,
        commercial_invoice_image=commercial_invoice_filename,
        pl_image=pl_filename,
        vgm_image=vgm_filename,
        seal_image=seal_filename,
        undertaking_image=undertaking_filename,
        payment_recieptt_image=payment_recieptt_filename,
        booking_confirmation_image=booking_confirmation_filename,
        container_image=container_filename
    )

    db.session.add(new_entry)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    with app.app_context():  # Ensure that app context is available
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
