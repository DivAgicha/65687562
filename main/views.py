from django.http import Http404
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import views
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from oauth2_provider.contrib.rest_framework.permissions import TokenHasScope, TokenHasReadWriteScope
from oauth2_provider.models import AccessToken, RefreshToken

from main import log
from main.response import RESTResponse
from main.models import SourceSet, UserSet, FormStatusSet, PTSet, SHSet, CLSet, CCSet, id_generator

import os, re, string

clear = lambda: os.system('cls')
userid_pattern = re.compile("^[0-9a-z-]+$")
formid_pattern = re.compile("^[0-9a-z]+-\d+-(PT|SH|CL|CC)$")
logger = log.getTimedLogger()

def clear_screen():
    global clear
    clear()
    
def get_type_code(val):
    code = ['pt', 'sh', 'cl', 'cc']
    
    if val in code:
        return val.upper()
    elif val=='private tuition':
        return code[0].upper()
    elif val=='school':
        return code[1].upper()
    elif val=='college':
        return code[2].upper()
    elif val=='coaching centre':
        return code[3].upper()
    
    raise Exception('Enter a valid type')

def get_gender_code(val):
    code = ['m', 'f', 'o']
    
    if val in code:
        return val.upper()
    elif val=='male':
        return code[0].upper()
    elif val=='female':
        return code[1].upper()
    elif val=='other':
        return code[2].upper()
    
    raise Exception('Enter a valid gender')

def get_status_code(val):
    code = ['a', 'r', 'w']
    
    if val in code:
        return val.upper()
    elif val=='approved':
        return code[0].upper()
    elif val=='rejected':
        return code[1].upper()
    elif val=='waiting':
        return code[2].upper()
    
    raise Exception('Enter a valid status')

def get_fee_type_code(val):
    code = ['pm', 'py', 'ps', 'pc']
    
    if val in code:
        return val.upper()
    elif val=='per month':
        return code[0].upper()
    elif val=='per year':
        return code[1].upper()
    elif val=='per sem ':
        return code[2].upper()
    elif val=='per course ':
        return code[3].upper()
    
    raise Exception('Enter a valid status')

def isSourceId(val):
    return val.isdigit()

def isUserId(val):
    return userid_pattern.match(val)

def isFormId(val):
    try:
        #return not val.split('-')[0].isdigit() and formid_pattern.match(val)
        return formid_pattern.match(val)
    except Exception:
        raise Exception('Invalid request')
    
def isValidType(val):
    #val = val.replace(' ', '_')
    valid_types = ['private tuition', 'school', 'college', 'coaching centre', 'pt', 'sh', 'cl', 'cc']
    
    if val in valid_types:
        return True
    
    raise Exception('Invalid request: data tampered')

def get_form(val, source_id=None):
    form_type = val[-2:].lower()
    
    try:
        if isFormId(val):
            if form_type=='pt':
                if source_id:
                    return PTSet.objects.get(uuid=val, source_id__ehub_id=source_id)
                return PTSet.objects.get(uuid=val)
            if form_type=='sh':
                if source_id:
                    return SHSet.objects.get(uuid=val, source_id__ehub_id=source_id)
                return SHSet.objects.get(uuid=val)
            if form_type=='cl':
                if source_id:
                    return CLSet.objects.get(uuid=val, source_id__ehub_id=source_id)
                return CLSet.objects.get(uuid=val)
            if form_type=='cc':
                if source_id:
                    return CCSet.objects.get(uuid=val, source_id__ehub_id=source_id)
                return CCSet.objects.get(uuid=val)
    except Exception:
        raise Exception('Invalid request: no matching form_id exist')        
    
    raise Exception('Invalid request: enter a valid form_id')

def get_all_forms(source_id):
    source_type = SourceSet.objects.get(ehub_id=source_id).type.lower()
    
    if source_type=='pt':
        return PTSet.objects.filter(source_id__ehub_id=source_id)
    if source_type=='sh':
        return SHSet.objects.filter(source_id__ehub_id=source_id)
    if source_type=='cl':
        return CLSet.objects.filter(source_id__ehub_id=source_id)
    if source_type=='cc':
        return CCSet.objects.filter(source_id__ehub_id=source_id)
    
    raise Exception('Invalid request')

def get_source(val):
    return SourceSet.objects.get(ehub_id=val)

def get_user(val):
    return UserSet.objects.get(uuid=val)

def get_all_entries_of_source(source_id, form_id=None):
    source_type =  SourceSet.objects.get(ehub_id=source_id).type
    
    forms = None
    if source_type=='PT':
        if form_id:
            if isFormId(form_id):
                forms = PTSet.objects.filter(source_id__ehub_id=source_id, uuid=form_id)
            else:
                raise Exception('Invalid request')
        else:
            forms = PTSet.objects.filter(source_id__ehub_id=source_id)
    elif source_type=='SH':
        if form_id:
            if isFormId(form_id):
                forms = SHSet.objects.filter(source_id__ehub_id=source_id, uuid=form_id)
            else:
                raise Exception('Invalid request')       
        else:
            forms = SHSet.objects.filter(source_id__ehub_id=source_id)
    elif source_type=='CL':
        if form_id:
            if isFormId(form_id):
                forms = CLSet.objects.filter(source_id__ehub_id=source_id, uuid=form_id)
            else:
                raise Exception('Invalid request')
        else:
            forms = CLSet.objects.filter(source_id__ehub_id=source_id)
    elif source_type=='CC':
        if form_id:
            if isFormId(form_id):
                forms = CCSet.objects.filter(source_id__ehub_id=source_id, uuid=form_id)
            else:
                raise Exception('Invalid request')
        else:
            forms = CCSet.objects.filter(source_id__ehub_id=source_id)
        
    entries = FormStatusSet.objects.none()
    for form in forms:
        entries = entries | form.entries.all()
        
    if entries:
        return entries
    
    raise Exception('No data found')

def serialize_entries(entries, isSource=False):
    data = []
    for entry in entries:
        json = entry.toJSON()
        #json['form_id'] = str(entry.form_type_object)
        json['form'] = get_form(str(entry.form_type_object)).toJSON()
        
        if isSource:
            json['user'] = UserSet.objects.get(uuid=str(entry.user_id)).toJSON(True)
        
        data.append(json)
        
    return data

def serialize_forms(forms, isUser=True):
    data = []
    for form in forms:
        json = form.toJSON()
        
        if isUser:
            json['source'] = form.source_id.toJSON(True)
        
        data.append(json)
        
    return data

def update_form_fields(form, request):
    fields_updated = False
    
    try:
        if request.POST.get('course'):
            form.course = request.POST.get('course').lower()
            fields_updated = True
        if request.POST.get('till_class'):
            form.till_class = request.POST.get('till_class').lower()
            fields_updated = True
        if request.POST.get('fee'):
            form.fee = int(request.POST.get('fee'))
            fields_updated = True
        if request.POST.get('fee_type'):
            form.fee_type = get_fee_type_code(request.POST.get('fee_type').lower())
            fields_updated = True
        if request.POST.get('timing'):
            form.timing = request.POST.get('timing')
            fields_updated = True
        if request.POST.get('no_of_batches'):
            form.number_of_batches = int(request.POST.get('no_of_batches'))
            fields_updated = True
        if request.POST.get('seats_left'):
            form.seats_left = int(request.POST.get('seats_left'))
            fields_updated = True
        if request.POST.get('gform_link'):
            form.gform_link = request.POST.get('gform_link')
            fields_updated = True
        if request.POST.get('is_link_active'):
            form.is_link_active = request.POST.get('is_link_active').lower()=='true'
            fields_updated = True
        if request.POST.get('last_date_to_apply'):
            form.last_date_to_apply = request.POST.get('last_date_to_apply')
            fields_updated = True
    except Exception:
        raise Exception('Invalid request: inappropriate data provided')
    
    if not fields_updated:
        raise Exception('Insufficient data')
    
    form.save()

def authenticate_user(identifier, password, user_type):
    obj = None
    
    try:
        if user_type=='source':
            if not isSourceId(identifier):
                raise Exception('Enter a valid ehub id')
            obj = SourceSet.objects.get(ehub_id=identifier)
        elif user_type=='user':
            validate_email(identifier)
            obj = UserSet.objects.get(email=identifier)
        else:
            raise Exception('Enter a valid type')
                
    except ValidationError:
        raise Exception('Enter a valid email address')
    
    except Exception as e:
        if str(e).startswith('Enter a valid'):
            raise e
        
        raise Exception('Enter a valid credential set')

    if len(password) < 8:
        raise Exception('Enter a valid password(length>=8)')
        
    if not check_password(password, obj.password):
        raise Exception('Enter a valid password')
    
    return obj
    

def default(request):
    clear_screen()
    raise Http404
    
class RequestEhubID(views.APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read', 'write']
    
    def get(self, request):
        clear_screen()
        logger.info("generating Ehub ID...")
        
        json_data = {
            'result': {
                'type': 'creation',
                'status': 'failed',
            }
        }
        
        try:
            ip = request.META.get('REMOTE_ADDR', "-")
            logger.info("found IP: "+ip)
            
            try:
                obj = SourceSet.objects.get(name = ip)
                json_data['result']['type'] = 'retrieval'
            except Exception as e:
                logger.error('Exception: '+str(e))
                ehub_id = id_generator(chars=string.digits, isEhubId=True)
                logger.info("generated Ehub ID: "+ehub_id)
                obj = SourceSet.objects.create(ehub_id = ehub_id, name = ip)
                
            json_data['id'] = int(obj.ehub_id)
            json_data['result']['status'] = 'success'
        except Exception as e:
            json_data['result']['exception'] = 'Error encountered'
            logger.error('Exception: '+str(e))
            
        return RESTResponse(json_data)

class Authenticate(views.APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read', 'write']
    
    def post(self, request):
        clear_screen()
        logger.info("authenticating user...")
        
        json_data = {
            'result': {
                'type': 'authentication',
                'status': 'failed',
            }
        }
        
        try:
            if request.POST.get('authenticate') and request.POST.get('authenticate').lower()=='true':
                if request.POST.get('identifier') and request.POST.get('password') and request.POST.get('type'):
                    obj = authenticate_user(request.POST.get('identifier'), request.POST.get('password'), request.POST.get('type').lower())
                    json_data['id'] = str(obj)
                    json_data['result']['data'] = obj.toJSON()
                    json_data['result']['status'] = 'success'
                else:
                    raise Exception('Insufficient data')
            else:
                json_data['result']['type'] = 'unknown'
                json_data['result']['exception'] = 'Invalid request'
            
        except Exception as e:            
            json_data['result']['exception'] = str(e) if str(e).startswith('Enter a valid') or str(e).startswith('Invalid request') or str(e)=='Insufficient data' else 'Error encountered'
            logger.error('Exception: '+str(e))
            
        return RESTResponse(json_data)

# class Source(views.APIView):
#     authentication_classes = [OAuth2Authentication]
#     permission_classes = [TokenHasScope]
#     required_scopes = ['read', 'write']
#     
#     def post(self, request, ehub_id):
#         clear_screen()
#         logger.info("registering source details...")
#         
#         json_data = {
#             'id': ehub_id,
#             'result': {
#                 'type': 'creation',
#                 'status': 'failed',
#             }
#         }
#         
#         try:
#             if not request.POST.get('update'):
#                 if request.POST.get('type') and request.POST.get('email') and request.POST.get('password') and request.POST.get('name'):
#                     validate_email(request.POST.get('email'))
#                     
#                     if len(request.POST.get('password')) < 8:
#                         raise Exception('Enter a valid password(length>=8)')
#                     
#                     logger.info('putting entry in DB')
#                     
#                     SourceSet.objects.create(
#                             ehub_id = ehub_id,
#                             type = get_type_code(request.POST.get('type').lower()),
#                             email = request.POST.get('email').lower(),
#                             password = make_password(request.POST.get('password')),
#                             name = request.POST.get('name').lower()
#                         )
#                     
#                     json_data['result']['status'] = 'success'
#                     
#                 else:
#                     raise Exception('Please fill all the details to continue')
#                     
#             elif request.POST.get('update').lower()=='true':
#                 json_data['result']['type'] = 'updation'
#                 obj = SourceSet.objects.get(ehub_id__exact=ehub_id)
#                 
#                 if request.POST.get('password'):
#                     if len(request.POST.get('password')) < 8:
#                         raise Exception('Enter a valid password(length>=8)')
#                     obj.password = make_password(request.POST.get('password'))
#                 if request.POST.get('name'):
#                     obj.name = request.POST.get('name').lower()
#                 if request.POST.get('street'):
#                     obj.street = request.POST.get('street').lower()
#                 if request.POST.get('city'):
#                     obj.city = request.POST.get('city').lower()
#                 if request.POST.get('state'):
#                     obj.state = request.POST.get('state').lower()
#                 if request.POST.get('pincode'):
#                     obj.pincode = int(request.POST.get('pincode'))
#                 if request.POST.get('contact'):
#                     obj.contact_num = request.POST.get('contact')
#                 if request.POST.get('starting_year'):
#                     obj.starting_year = int(request.POST.get('starting_year'))
#                 if request.POST.get('board'):
#                     obj.board = request.POST.get('board').lower()
#                 if request.POST.get('affiliation'):
#                     obj.affiliation = request.POST.get('affiliation').lower()
#                 if request.POST.get('college_type'):
#                     obj.college_type = request.POST.get('college_type').lower()
#                 if request.POST.get('asr'):
#                     obj.average_success_ratio = float(request.POST.get('asr'))
#                 if request.POST.get('rating'):
#                     obj.rating = float(request.POST.get('rating'))
#                 if request.POST.get('description'):
#                     obj.additional_info = request.POST.get('description')
#                     
#                 obj.save()
#                 
#                 json_data['result']['status'] = 'success'
#                     
#             else:
#                 json_data['result']['type'] = 'unknown'
#                 json_data['result']['exception'] = 'Invalid request'
#                 
#         except ValidationError:
#             json_data['result']['exception'] = 'Enter a valid email address'
#             logger.error('Exception: Enter a valid email address')
#                     
#         except Exception as e:
#             json_data['result']['exception'] = str(e) if str(e).startswith('Enter a valid') or str(e).startswith('Please fill') else 'Error encountered'
#             logger.error('Exception: '+str(e))
#         
#         return RESTResponse(json_data)
#     
#     def get(self, request, ehub_id):
#         clear_screen()
#         logger.info("fetching source details...")
#         
#         json_data = {
#             'id': ehub_id,
#             'result': {
#                 'type': 'retrieval',
#                 'status': 'failed',
#             }
#         }
#         
#         try:
#             # json_data['result']['data'] = json.loads(serializers.serialize('json', [SourceSet.objects.get(ehub_id__exact=ehub_id), ]))[0]['fields']
#             json_data['result']['data'] = SourceSet.objects.get(ehub_id__exact=ehub_id).toJSON()
#             json_data['result']['status'] = 'success'
#             
#         except Exception as e:
#             json_data['result']['exception'] = 'Error encountered'
#             logger.error('Exception: '+str(e))
#         
#         return RESTResponse(json_data)

class Source(views.APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read', 'write']
    
    def post(self, request, ehub_id):
        clear_screen()
        logger.info("registering source details...")
        
        json_data = {
            'id': ehub_id,
            'result': {
                'type': 'creation',
                'status': 'failed',
            }
        }
        
        try:                
            if not request.POST.get('update'):
                try:
                    obj = SourceSet.objects.get(name = request.META.get('REMOTE_ADDR', "-"))
                
                    if not str(obj.ehub_id)==ehub_id:
                        raise Exception('Invalid Attempt: data has been tampered')
                    
                    logger.info("time difference: "+str(timezone.now() - obj.datetime))
                    
                    if int(str(timezone.now() - obj.datetime).split(":")[1])>=30:
                        obj.ehub_id = id_generator(chars=string.digits, isEhubId=True)
                        obj.datetime = timezone.now()
                        obj.save()
                        
                        raise Exception('Invalid Attempt: registration timeout. Please reload your webpage to continue with the registration')
                except Exception as e:
                    logger.error("Exception: "+str(e))
                    if str(e).startswith("Invalid Attempt"):
                        raise e
                    raise Exception('Invalid Attempt: please use our web interface for registration')
                
                if request.POST.get('type') and request.POST.get('email') and request.POST.get('password') and request.POST.get('name'):
                    validate_email(request.POST.get('email'))
                    
                    if len(request.POST.get('password')) < 8:
                        raise Exception('Enter a valid password(length>=8)')
                    
                    logger.info('putting entry in DB')
                    
                    obj.type = get_type_code(request.POST.get('type').lower())
                    obj.email = request.POST.get('email').lower()
                    obj.password = make_password(request.POST.get('password'))
                    obj.name = request.POST.get('name').lower()
                    
                    obj.save()
                    
                    json_data['result']['status'] = 'success'
                    
                else:
                    raise Exception('Please fill all the details to continue')
                    
            elif request.POST.get('update').lower()=='true':
                json_data['result']['type'] = 'updation'
                obj = SourceSet.objects.get(ehub_id__exact=ehub_id)
                
                if request.POST.get('password'):
                    if len(request.POST.get('password')) < 8:
                        raise Exception('Enter a valid password(length>=8)')
                    obj.password = make_password(request.POST.get('password'))
                if request.POST.get('name'):
                    obj.name = request.POST.get('name').lower()
                if request.POST.get('street'):
                    obj.street = request.POST.get('street').lower()
                if request.POST.get('city'):
                    obj.city = request.POST.get('city').lower()
                if request.POST.get('state'):
                    obj.state = request.POST.get('state').lower()
                if request.POST.get('pincode'):
                    obj.pincode = int(request.POST.get('pincode'))
                if request.POST.get('contact'):
                    obj.contact_num = request.POST.get('contact')
                if request.POST.get('starting_year'):
                    obj.starting_year = int(request.POST.get('starting_year'))
                if request.POST.get('board'):
                    obj.board = request.POST.get('board').lower()
                if request.POST.get('affiliation'):
                    obj.affiliation = request.POST.get('affiliation').lower()
                if request.POST.get('college_type'):
                    obj.college_type = request.POST.get('college_type').lower()
                if request.POST.get('asr'):
                    obj.average_success_ratio = float(request.POST.get('asr'))
                if request.POST.get('rating'):
                    obj.rating = float(request.POST.get('rating'))
                if request.POST.get('description'):
                    obj.additional_info = request.POST.get('description')
                    
                obj.save()
                
                json_data['result']['status'] = 'success'
                    
            else:
                json_data['result']['type'] = 'unknown'
                json_data['result']['exception'] = 'Invalid request'
                
        except ValidationError:
            json_data['result']['exception'] = 'Enter a valid email address'
            logger.error('Exception: Enter a valid email address')
                    
        except Exception as e:
            json_data['result']['exception'] = str(e) if str(e).startswith('Enter a valid') or str(e).startswith('Please fill') or str(e).startswith('Invalid Attempt') else 'Error encountered'
            logger.error('Exception: '+str(e))
        
        return RESTResponse(json_data)
        
class User(views.APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope]
    
    def post(self, request, user_id=None):
        clear_screen()
        logger.info("registering user details...")
        
        json_data = {
            'result': {
                'type': 'creation',
                'status': 'failed',
            }
        }
        
        try:
            if not request.POST.get('update'):                
                if request.POST.get('email') and request.POST.get('password') and request.POST.get('name') and request.POST.get('dob') and request.POST.get('gender'):                    
                    validate_email(request.POST.get('email'))
                    
                    if len(request.POST.get('password')) < 8:
                        raise Exception('Enter a valid password(length>=8)')
                    
                    logger.info('putting entry in DB')
                    
                    user = UserSet.objects.create(
                            email = request.POST.get('email').lower(),
                            password = make_password(request.POST.get('password')),
                            name = request.POST.get('name').lower(),
                            dob = request.POST.get('dob'),
                            gender = get_gender_code(request.POST.get('gender').lower())
                        )
                    
                    json_data['result']['status'] = 'success'
                    json_data['id'] = user.uuid
                    
                else:
                    raise Exception('Please fill all the details to continue')
                    
            elif request.POST.get('update').lower()=='true' and user_id:
                json_data['result']['type'] = 'updation'
                obj = UserSet.objects.get(uuid__exact=user_id)
                
                if request.POST.get('password'):
                    obj.password = make_password(request.POST.get('password'))
                if request.POST.get('name'):
                    obj.name = request.POST.get('name').lower()
                if request.POST.get('dob'):
                    obj.dob = request.POST.get('dob')
                if request.POST.get('gender'):
                    obj.gender = get_gender_code(request.POST.get('gender').lower())
                if request.POST.get('street'):
                    obj.street = request.POST.get('street').lower()
                if request.POST.get('city'):
                    obj.city = request.POST.get('city').lower()
                if request.POST.get('state'):
                    obj.state = request.POST.get('state').lower()
                if request.POST.get('pincode'):
                    obj.pincode = int(request.POST.get('pincode'))
                if request.POST.get('contact'):
                    obj.contact_num = request.POST.get('contact')
                    
                obj.save()
                
                json_data['result']['status'] = 'success'
                json_data['id'] = user_id
                    
            else:
                json_data['result']['type'] = 'unknown'
                json_data['result']['exception'] = 'Invalid request'
                
        except ValidationError:
            json_data['result']['exception'] = 'Enter a valid email address'
            logger.error('Exception: Enter a valid email address')
                    
        except Exception as e:
            json_data['result']['exception'] = str(e) if str(e).startswith('Enter a valid') or str(e).startswith('Please fill') else 'Error encountered'
            logger.error('Exception: '+str(e))
        
        return RESTResponse(json_data)
    
    def get(self, request, user_id=None):
        clear_screen()
        logger.info("fetching user details...")
        
        json_data = {
            'result': {
                'type': 'retrieval',
                'status': 'failed',
            }
        }
        
        try:
            if user_id:
                json_data['id'] = user_id
                # json_data['result']['data'] = json.loads(serializers.serialize('json', [UserSet.objects.get(uuid__exact=ehub_id), ]))[0]['fields']
                json_data['result']['data'] = UserSet.objects.get(uuid__exact=user_id).toJSON()
                json_data['result']['status'] = 'success'
                   
            else:
                json_data['result']['type'] = 'unknown'
                json_data['result']['exception'] = 'Invalid request'
            
        except Exception as e:
            json_data['result']['exception'] = 'Error encountered'
            logger.error('Exception: '+str(e))
        
        return RESTResponse(json_data)
    
class FormStatus(views.APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope]
    
    def post(self, request, id):
        clear_screen()
        logger.info("registering entry details...")
        
        json_data = {
            'result': {
                'type': 'creation',
                'status': 'failed',
            }
        }
        
        try:
            if isSourceId(id) and request.POST.get('update') and request.POST.get('update').lower()=='true':
                json_data['id'] = id
                json_data['result']['type'] = 'updation'
                
                if request.POST.get('status') and request.POST.get('user_id') and request.POST.get('form_id'):
                    #obj = FormStatusSet.objects.get(user_id__uuid=request.POST.get('user_id'), object_id=get_form(request.POST.get('form_id'), id).id)
                    form = get_form(request.POST.get('form_id'), id)
                    obj = form.entries.get(user_id__uuid=request.POST.get('user_id'), datetime=request.POST.get('entry_creation_date'))
                    obj.status = get_status_code(request.POST.get('status').lower())
                    obj.save()
                    
                    if obj.status=='A' and form.seats_left>0:
                        form.seats_left -= 1
                        form.save()
                    
                    json_data['result']['status'] = 'success'
                    
                else:
                    raise Exception('Insufficient data')
                
            elif isUserId(id) and not request.POST.get('update'):
                json_data['id'] = id
                if request.POST.get('form_id'):
                    user = UserSet.objects.get(uuid=id)
                    form = get_form(request.POST.get('form_id'))
                    
                    if form.is_link_active:
                        try:
                            form.entries.get(user_id = user)
                            
                            json_data['result']['status'] = 'application already submitted'
                        except Exception as e:
                            FormStatusSet.objects.create(
                                user_id = user,
                                form_type_object = form
                            )
                            
                            json_data['result']['status'] = 'success'
                    else:
                        json_data['result']['status'] = 'form expired'
                    
                else:
                    raise Exception('Insufficient data')
                                
            else:
                json_data['result']['type'] = 'unknown'
                json_data['result']['exception'] = 'Invalid request'
                    
        except Exception as e:
            json_data['result']['exception'] = str(e) if str(e).startswith('Enter a valid') or str(e).startswith('Invalid request') or str(e)=='Insufficient data' else 'Error encountered'
            logger.error('Exception: '+str(e))
        
        return RESTResponse(json_data)
                
    def get(self, request, id):
        clear_screen()
        logger.info("fetching entry details...")
        
        json_data = {
            'result': {
                'type': 'retrieval',
                'status': 'failed',
                'count': 0,
                'data': [],
            }
        }
                     
        try:                
            if isSourceId(id):
                json_data['id'] = id
                if request.GET.get('form_id') and request.GET.get('all'):
                    raise Exception('Invalid request: conflicting parameters found')
                elif request.GET.get('form_id'):
                    #fetch single form entries
                    if isFormId(request.GET.get('form_id')):
                        entries = get_all_entries_of_source(id, request.GET.get('form_id'))
                        json_data['result']['count'] = entries.count()
                        json_data['result']['data'] = serialize_entries(entries, True)
                        json_data['result']['status'] = 'success'
                    else:
                        raise Exception('Invalid request: enter a valid form_id')
                elif request.GET.get('all') and request.GET.get('all').lower()=='true':
                    #fetch all forms' entries
                    entries = get_all_entries_of_source(id)
                    json_data['result']['count'] = entries.count()
                    json_data['result']['data'] = serialize_entries(entries, True)
                    json_data['result']['status'] = 'success'
                else:
                    raise Exception('Insufficient data')
                
            elif isUserId(id):
                json_data['id'] = id
                if request.GET.get('form_id') and request.GET.get('all'):
                    raise Exception('Invalid request: conflicting parameters found')
                elif request.GET.get('form_id'):
                    #fetch single form entries
                    entries = None
                    form = get_form(request.GET.get('form_id'))
                    if request.GET.get('many') and request.GET.get('many').lower()=='true':
                        entries = form.entries.filter(user_id__uuid=id)
                    else:
                        entries = form.entries.filter(user_id__uuid=id).order_by('-datetime')[:1]
                        
                    if entries.count()==0:
                        raise Exception('Invalid request: no matching record exist')
                        
                    json_data['result']['count'] = entries.count()
                    json_data['result']['data'] = serialize_entries(entries)
                    json_data['result']['status'] = 'success'
                elif request.GET.get('all') and request.GET.get('all').lower()=='true':
                    #fetch all forms' entries
                    entries = FormStatusSet.objects.filter(user_id__uuid=id)
                    json_data['result']['count'] = entries.count()
                    json_data['result']['data'] = serialize_entries(entries)
                    json_data['result']['status'] = 'success'
                else:
                    raise Exception('Insufficient data')
                
            else:
                json_data['result']['type'] = 'unknown'
                json_data['result']['exception'] = 'Invalid request'
                    
        except Exception as e:
            json_data['result']['exception'] = str(e) if str(e).startswith('Enter a valid') or str(e).startswith('Invalid request') or str(e)=='Insufficient data' or str(e)=='No data found' else 'Error encountered'
            logger.error('Exception: '+str(e))
            
        return RESTResponse(json_data)
        
class Form(views.APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope]
    
    def post(self, request, ehub_id):
        clear_screen()
        logger.info("registering form details...")
        
        json_data = {
            'id': ehub_id,
            'result': {
                'type': 'creation',
                'status': 'failed',
            }
        }
        
        try:
            if not request.POST.get('update'):
                if request.POST.get('type') and isValidType(request.POST.get('type').lower()):
                    source = get_source(ehub_id)
                    type_code = get_type_code(request.POST.get('type').lower())
                    
                    logger.info
                    if not source.type==type_code:
                        raise Exception('Invalid request: data tampered')
                    
                    if type_code=='PT':
                        if request.POST.get('course') and request.POST.get('fee') and request.POST.get('fee_type') and request.POST.get('timing') and request.POST.get('no_of_batches') and request.POST.get('seats_left') and request.POST.get('gform_link') and request.POST.get('is_link_active') and request.POST.get('last_date_to_apply'):
                            PTSet.objects.create(
                                source_id = source,
                                course = request.POST.get('course').lower(),
                                fee = int(request.POST.get('fee')),
                                fee_type = get_fee_type_code(request.POST.get('fee_type').lower()),
                                timing = request.POST.get('timing'),
                                number_of_batches = int(request.POST.get('no_of_batches')),
                                seats_left = int(request.POST.get('seats_left')),
                                gform_link = request.POST.get('gform_link'),
                                is_link_active = request.POST.get('is_link_active').lower()=='true',
                                last_date_to_apply = request.POST.get('last_date_to_apply')
                            )
                        else:
                            raise Exception('Insufficient data')
                    
                    elif type_code=='SH':
                        if request.POST.get('till_class') and request.POST.get('fee') and request.POST.get('fee_type') and request.POST.get('timing') and request.POST.get('seats_left') and request.POST.get('gform_link') and request.POST.get('is_link_active') and request.POST.get('last_date_to_apply'):
                            SHSet.objects.create(
                                source_id = source,
                                till_class = request.POST.get('till_class').lower(),
                                fee = int(request.POST.get('fee')),
                                fee_type = get_fee_type_code(request.POST.get('fee_type').lower()),
                                timing = request.POST.get('timing'),
                                seats_left = int(request.POST.get('seats_left')),
                                gform_link = request.POST.get('gform_link'),
                                is_link_active = request.POST.get('is_link_active').lower()=='true',
                                last_date_to_apply = request.POST.get('last_date_to_apply')
                            )
                        else:
                            raise Exception('Insufficient data')
                    
                    elif type_code=='CL':
                        if request.POST.get('course') and request.POST.get('fee') and request.POST.get('fee_type') and request.POST.get('timing') and request.POST.get('seats_left') and request.POST.get('gform_link') and request.POST.get('is_link_active') and request.POST.get('last_date_to_apply'):
                            CLSet.objects.create(
                                source_id = source,
                                course = request.POST.get('course'),
                                fee = int(request.POST.get('fee')),
                                fee_type = get_fee_type_code(request.POST.get('fee_type').lower()),
                                timing = request.POST.get('timing'),
                                seats_left = int(request.POST.get('seats_left')),
                                gform_link = request.POST.get('gform_link'),
                                is_link_active = request.POST.get('is_link_active').lower()=='true',
                                last_date_to_apply = request.POST.get('last_date_to_apply')
                            )
                        else:
                            raise Exception('Insufficient data')
                    
                    elif type_code=='CC':
                        if request.POST.get('course') and request.POST.get('fee') and request.POST.get('fee_type') and request.POST.get('timing') and request.POST.get('no_of_batches') and request.POST.get('seats_left') and request.POST.get('gform_link') and request.POST.get('is_link_active') and request.POST.get('last_date_to_apply'):
                            CCSet.objects.create(
                                source_id = source,
                                course = request.POST.get('course'),
                                fee = int(request.POST.get('fee')),
                                fee_type = get_fee_type_code(request.POST.get('fee_type').lower()),
                                timing = request.POST.get('timing'),
                                number_of_batches = int(request.POST.get('no_of_batches')),
                                seats_left = int(request.POST.get('seats_left')),
                                gform_link = request.POST.get('gform_link'),
                                is_link_active = request.POST.get('is_link_active').lower()=='true',
                                last_date_to_apply = request.POST.get('last_date_to_apply')
                            )
                        else:
                            raise Exception('Insufficient data')
                    
                    json_data['result']['status'] = 'success'
                    
                else:
                    raise Exception('Insufficient data')
                
            elif request.POST.get('update') and request.POST.get('update').lower()=='true':
                json_data['result']['type'] = 'updation'
                
                source = get_source(ehub_id)
                form = None
                
                if request.POST.get('form_id'):
                    if isFormId(request.POST.get('form_id')) and source.type==request.POST.get('form_id')[-2:]:
                        form = get_form(request.POST.get('form_id'), ehub_id)
                    else:
                        raise Exception('Invalid request')
                    
                else:
                    raise Exception('Insufficient data')
                
                #at this point 'form' variable will definitely have a valid form object
                update_form_fields(form, request)
                                                            
                json_data['result']['status'] = 'success'

            else:
                json_data['result']['type'] = 'unknown'
                json_data['result']['exception'] = 'Invalid request'
                    
        except Exception as e:
            json_data['result']['exception'] = str(e) if str(e).startswith('Enter a valid') or str(e).startswith('Invalid request') or str(e)=='Insufficient data' else 'Error encountered'
            logger.error('Exception: '+str(e))
            
        return RESTResponse(json_data)
    
    def get(self, request, ehub_id):
        clear_screen()
        logger.info("fetching form details...")
        
        json_data = {
            'id': ehub_id,
            'result': {
                'type': 'retrieval',
                'status': 'failed',
                'count': 0,
                'data': [],
            }
        }
        
        try:
            if request.GET.get('form_id') and request.GET.get('all'):
                raise Exception('Invalid request: conflicting parameters found')
            elif request.GET.get('form_id'):
                #fetch single form data
                form = get_form(request.GET.get('form_id'), ehub_id)
                json_data['result']['count'] = 1
                json_data['result']['data'] = form.toJSON()
                json_data['result']['status'] = 'success'
            elif request.GET.get('all') and request.GET.get('all').lower()=='true':
                #fetch all forms data
                forms = get_all_forms(ehub_id)
                json_data['result']['count'] = forms.count()
                json_data['result']['data'] = serialize_forms(forms)
                json_data['result']['status'] = 'success'
            else:
                raise Exception('Insufficient data')
                    
        except Exception as e:
            json_data['result']['exception'] = str(e) if str(e).startswith('Enter a valid') or str(e).startswith('Invalid request') or str(e)=='Insufficient data' else 'Error encountered'
            logger.error('Exception: '+str(e))
            
        return RESTResponse(json_data)

class RetrieveTokens(views.APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        clear_screen()
        logger.info("fetching tokens...")
        
        cid = None
        csk = None
        
        try:
            cid = request.POST.get('client_id')
            logger.info("found 'clientID': "+cid)
            csk = request.POST.get('client_secret')
            logger.info("found 'clientSecret': "+csk)
        except Exception as e:
            logger.error("Error: "+str(e))
            raise Http404
        else:
            if cid and csk:
                try:
                    refresh = RefreshToken.objects.get(application__client_id__exact = cid, application__client_secret__exact = csk)
                except Exception as e:
                    logger.error("error: "+str(e))
                    json_data = {
                        'detail': 'Authentication failed'
                    }
                else:
                    now = str(timezone.now())
                    token_expiration_date = str(AccessToken.objects.get(token__exact=str(refresh.access_token)).expires)
                    json_data = {
                        'detail': 'token',
                        'refresh_token': str(refresh.token),
                        'access_token': str(refresh.access_token),
                        'access_token_status': 'active' if token_expiration_date > now else 'expired'
                    }
                    
                return RESTResponse(json_data)
            else:
                logger.info("Error: information not provided")
                raise Http404