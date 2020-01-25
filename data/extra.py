SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'SIGNING_KEY': "FC465F92ED31AB01ECD61C2FDC0CFCCD7AB11AE3CE88C9F5999565B80E82"
    }
REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ]
}
REST_USE_JWT = True

#url
import rest_framework_simplejwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
# SAMPLE URL https://api.credicxotech.com/UserInfo/3/selfie.jpg
def protected_serve(request, path, document_root=None, show_indexes=False):
    try:
        user = JWTAuthentication.authenticate(JWTAuthentication(), request)[0]
    except TypeError:
        return JsonResponse({'error': 'Token Not Supplied!!'}, status=401)
    except rest_framework_simplejwt.exceptions.InvalidToken:
        return JsonResponse({'error': 'Invalid Token!!'}, status=401)
    try:
        if 'SELFIE.jpg' == path[-10:] or int(path.split('/')[0]) == user.id or \
                bool(user.groups.filter(name__in=group_names)) or user.is_superuser \
                or ('xml' == path[-3:] and user.groups.filter(name__in='Credit')):
            return serve(request, path, document_root, show_indexes)
        else:
            return JsonResponse({'error': 'ACCESS DENIED!!'}, status=401)
    except ValueError:
        return JsonResponse({'error': 'ACCESS DENIED!!'}, status=401)

#genrater
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from AdminPanel.agreement_script import agreement_generator
from AdminPanel.settings import DOCUMENTS_LOC, BASE_DIR
from api.controlbruteforce import control_brute_force
from api.decorator import group_required, step_authorization
from api.models import Loans, LoanTypes, Profile, BankAccountDetails
def get_info(request, loanId, loantype_obj, bank_obj):
    prof_obj = Profile.objects.filter(user=request.user).values('name', 'mother_name', 'dob', 'father_name',
                                                                'gender__gender', 'marital_status__marital_status',
                                                                'profession__profession', 'resident_address',
                                                                'resident_type__resident_type', 'phone_number',
                                                                'preference__relation', 'preference_number',
                                                                'aadhaar__address', 'pan__number',
                                                                'pin_code__india_district__district',
                                                                'device__imei_1', 'email')[0]

    data = {
        "Name:": prof_obj['name'],
        "Spouse:": prof_obj['father_name'],
        "Date of Birth:": prof_obj['dob'],
        "Gender:": prof_obj['gender__gender'],
        "Marital Status:": prof_obj['marital_status__marital_status'],
        "Occupation:": prof_obj['profession__profession'],
        "Nationality:": "Indian",
        "Residential Status:": "Indian",
        "Proof of Identity": "PAN",
        "PAN:": prof_obj['pan__number'],
        "Proof of Address:": "Aadhaar",
        "Address Type:": prof_obj['resident_type__resident_type'],
        "Address:": prof_obj['aadhaar__address'],
        "Current Address:": prof_obj['resident_address'],
        "Phone Number:": prof_obj['phone_number'],
        "Email:": prof_obj['email'],
        "Name of Bank:": bank_obj['ifsc_code__bank__bank'],
        "Bank A/C No:": bank_obj['account_number'],
        "IFSC:": bank_obj['ifsc_code__ifsc_code'],
        "Name of Related Person:": prof_obj['preference__relation'],
        "Phone Number of": "",
        "Related Person:": prof_obj['preference_number'],

        'picture': open(DOCUMENTS_LOC + str(request.user.id) + '/SELFIE.jpg', 'rb'),
        'logo': open(BASE_DIR + '/logo.png', 'rb'),
        'pan_image': open(DOCUMENTS_LOC + str(request.user.id) + '/PAN_CARD.jpg', 'rb'),

        "LOAN ID / SERIAL NO.": loanId,
        "CITY :": prof_obj['pin_code__india_district__district'],

        "Lender:": 'USHA Financial Services Pvt. Ltd.',
        "Fees and Charges:": '',
        "Platform:": 'www.credicxo.com',
        "Platform Fees:": loantype_obj.processing_fees,
        "Loan Amount:": loantype_obj.amount,
        "GST Charges:": 0,
        "Rate of Interest:": '36% per annum',
        "Cheque bounce:": 0,
        "Purpose of Loan:": 'Personal',
        "Cheque swap:": 0,
        "Service Charges:": 0,
        "Document retrieval:": "",
        "Late Payment Fee:(subsequent per day):": "1% of EMI amount per day",
        "NACH Dishonor:": 'N/A',
        "Late Payment Fee:(one time overduecharges):": '5% of loan amount',
        "Full and Part Prepayment Charges:": 0,

        "PAN Card or Form 60*": 'PAN',
        "Last 3 months bank statements or other income proof": '',
        "Address Proof:": 'Masked Aadhaar',
        "Any other document requested by Lender": '',

        "Signed By: ": prof_obj['name'],
        'Reason: ': 'Availing Loan',
        'Signed using ': 'Self Signed',
        "Device ID: ": '',
        'IMEI: ': prof_obj['device__imei_1'],
        'IP Address: ': request.META['HTTP_X_FORWARDED_FOR'].split(',')[0],
        'Timestamp: ': timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"),
    }

    try:
        data['aadhar_front'] = open(DOCUMENTS_LOC + str(request.user.id) + '/AADHAAR_FRONT.jpg', 'rb')
        data['aadhar_back'] = open(DOCUMENTS_LOC + str(request.user.id) + '/AADHAAR_BACK.jpg', 'rb')
    except FileNotFoundError:
        pass
    return data


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@group_required('Borrower')
@step_authorization(16)
def generate_agreement(request):
    if control_brute_force(request, "Agreement"):
        return Response({
            'show': True,
            'error': "Hold on a bit, try again after an hour!!",
            'current_step': 16
         }, 403)

    if Loans.objects.filter(user=request.user, repayment_status__lte=1, disbursement_status__gte=1).count() != 0:
        return Response({
            'error': 'Older Loans not repaid or last loan disbursal under process!!',
            'current_step': 16
        }, 400)
    orderId = "CDXO" + timezone.localtime(timezone.now()).strftime("%d%m%Y") + str(request.user.id) \
              + str(Loans.objects.filter(user=request.user).count())
    try:
        loan_type = int(request.data.get('loan_type'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid Loan Type!!'}, 400)

    if loan_type not in Profile.objects.get(user=request.user).allowed_loan_types:
        return Response({'error': 'Loan Type not allowed for current user!!'}, 401)

    loantype_obj = LoanTypes.objects.get(id=loan_type)
    total_repayment_amount = loantype_obj.total_repayment_amount
    loan_obj, _ = Loans.objects.get_or_create(loan_type_id=loan_type, balance=total_repayment_amount, user=request.user,
                                              loanId=orderId)
    bank_obj = BankAccountDetails.objects.filter(user=request.user).values('ifsc_code__ifsc_code',
                                                                           'ifsc_code__bank__bank', 'account_number')[0]

    if not bank_obj['account_number']:
        return Response({'error': 'No bank accounts found for current user!!'}, 400)

    agreement_generator(get_info(request, orderId, loantype_obj, bank_obj),
                        DOCUMENTS_LOC + str(request.user.id) + '/' + orderId)
    return Response({'loanId': orderId,
                     'pdf': 'https://api.credicxotech.com/UserInfo/' + str(request.user.id) + '/' + orderId + '.pdf'},
                    200)
