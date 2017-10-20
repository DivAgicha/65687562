from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import uuid, string, random, time
from datetime import datetime, timedelta

from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

def get_deadline():
    return datetime.today() + timedelta(days=1)

def get_form_id(form_type):
    valid_form_types = ['PT', 'SH', 'CL', 'CC']
    if form_type in valid_form_types:
        return id_generator(form_type=form_type)
    else:
        raise Exception('Invalid Data: form creation error')

def id_generator(size=8, chars=string.ascii_lowercase + string.digits, form_type='NULL', isEhubId=False):
    if not isEhubId:
        return ''.join(random.choice(chars) for _ in range(size)) + '-' + str(round(time.time() * 1000)) + '-' + form_type
    else:
        return ''.join(random.choice(chars) for _ in range(size))

PER_MONTH = 'PM'
PER_YEAR = 'PY'
PER_SEM = 'PS'
PER_COURSE = 'PC'
FEE_TYPE_CHOICES = (
    (PER_MONTH, 'Per Month'),
    (PER_YEAR, 'Per Year'),
    (PER_SEM, 'Per Sem'),
    (PER_COURSE, 'Per Course'),
)

class SourceSet(models.Model):
    PRIVATE_TUITION = 'PT'
    SCHOOL = 'SH'
    COLLEGE = 'CL'
    COACHING_CENTRE = 'CC'
    TYPE_CHOICES = (
        (PRIVATE_TUITION, 'Private Tuition'),
        (SCHOOL, 'School'),
        (COLLEGE, 'College'),
        (COACHING_CENTRE, 'Coaching Centre'),
    )
    
    def _get_commission(self):
        if self.type=='PT' or self.type=='SH':
            return 10
        else:
            return 15
        
    def _get_address(self):
        address = ''
        something_present = False
        
        if self.street:
            address += self.street + ', '
            something_present = True
            
        if self.city:
            address += self.city + ', '
            something_present = True
            
        if self.state:
            address += self.state + ', '
            something_present = True
            
        if self.pincode and something_present:
            address = address.rstrip(', ')
            address += ' - ' + str(self.pincode)
        else:
            address = '-'
            
        return address
        
    def toJSON(self, data_for_form=False):
        exclusion = ['id', 'ehub_id', 'password', 'street', 'city', 'state', 'pincode']
        fields_for_form_exclusion = ['id', 'type', 'email', 'password', 'street', 'city', 'state', 'pincode', 'contact_num', 'datetime']
        json_dict = {}
        for field in self._meta.fields:
            if data_for_form:
                if field.name not in fields_for_form_exclusion and field.name=='ehub_id':
                    json_dict['id'] = getattr(self, field.name)
                elif field.name not in fields_for_form_exclusion:
                    json_dict[field.name] = getattr(self, field.name)
            elif field.name not in exclusion:
                json_dict[field.name] = getattr(self, field.name)
    
        if not data_for_form:
            json_dict['address'] = getattr(self, 'address')
        return json_dict
    
    ehub_id = models.PositiveIntegerField(unique=True, editable=False)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, null=False)
    email = models.EmailField(max_length=254, validators=[EmailValidator], null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    commission = property(_get_commission)
    
    name = models.CharField(max_length=200, null=True)
    street = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.PositiveIntegerField(null=True)
    address = property(_get_address)
    contact_num = models.CharField(max_length=13, null=True)
    starting_year = models.PositiveSmallIntegerField(null=True)
    board = models.CharField(max_length=50, null=True)
    affiliation = models.CharField(max_length=100, null=True)   #in case of 'College'
    college_type = models.CharField(max_length=50, null=True)   #in case of 'College' - Deemed, Autonomous, etc.
    average_success_ratio = models.DecimalField(validators=[MinValueValidator(1), MaxValueValidator(10)], max_digits=3, decimal_places=1, null=True)    #in case of 'College' or 'Coaching Centre'
    rating = models.DecimalField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)], max_digits=3, decimal_places=1)
    additional_info = models.TextField()
    datetime = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return str(self.ehub_id)
        
    class Meta:
        unique_together = (('email', 'name'),)
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'

class UserSet(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )
        
    def _get_address(self):
        address = ''
        something_present = False
        
        if self.street:
            address += self.street + ', '
            something_present = True
            
        if self.city:
            address += self.city + ', '
            something_present = True
            
        if self.state:
            address += self.state + ', '
            something_present = True
            
        if self.pincode and something_present:
            address = address.rstrip(', ')
            address += ' - ' + str(self.pincode)
        else:
            address = '-'
            
        return address
        
    def toJSON(self, data_for_form=False):
        exclusion = ['id', 'uuid', 'password', 'street', 'city', 'state', 'pincode']
        fields_for_form = ['uuid', 'email', 'name', 'contact_num']
        json_dict = {}
        for field in self._meta.fields:
            if data_for_form:
                if field.name in fields_for_form and field.name=='uuid':
                    json_dict['id'] = getattr(self, field.name)
                elif field.name in fields_for_form:
                    json_dict[field.name] = getattr(self, field.name)
            elif field.name not in exclusion:
                json_dict[field.name] = getattr(self, field.name)
    
        if not data_for_form:
            json_dict['address'] = getattr(self, 'address')
        return json_dict
    
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=254, validators=[EmailValidator], null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    street = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.PositiveIntegerField(null=True)
    address = property(_get_address)
    contact_num = models.CharField(max_length=13, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    datetime = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return str(self.uuid)
        
    class Meta:
        unique_together = (('email', 'name'),)
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s' % (self.name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
        
class FormStatusSet(models.Model):
    APPROVED = 'A'
    REJECTED = 'R'
    WAITING = 'W'
    CANCELLED = 'C'
    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (WAITING, 'Waiting'),
        (CANCELLED, 'Cancelled'),
    )
        
    def toJSON(self):
        exclusion = ['id', 'user_id', 'content_type', 'object_id']
        #fields_to_be_passed_as_string = ['user_id']
        json_dict = {}
        for field in self._meta.fields:
            #if field.name in fields_to_be_passed_as_string:
            #    json_dict[field.name] = str(getattr(self, field.name))
            if field.name not in exclusion:
                json_dict[field.name] = getattr(self, field.name)
    
        return json_dict
    
    user_id = models.ForeignKey(UserSet, on_delete=models.PROTECT)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    form_type_object = GenericForeignKey('content_type', 'object_id')
    
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='W')
    last_modified = models.DateField(auto_now=True)
    datetime = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return str(self.id)
        
    class Meta:
        verbose_name = 'ApplicationFormStatus'
        verbose_name_plural = 'ApplicationFormStatus'
        
class PTSet(models.Model):
    def toJSON(self):
        exclusion = ['id', 'source_id', 'entries']
        json_dict = {}
        for field in self._meta.fields:
            if field.name not in exclusion:
                json_dict[field.name] = getattr(self, field.name)
    
        return json_dict
    
    source_id = models.ForeignKey(SourceSet, on_delete=models.PROTECT)
    uuid = models.CharField(max_length=40, unique=True, editable=False)
    course = models.CharField(max_length=100, null=False)
    fee = models.PositiveIntegerField(null=False)
    fee_type = models.CharField(max_length=2, choices=FEE_TYPE_CHOICES)
    timing = models.CharField(max_length=150, null=False)
    number_of_batches = models.PositiveSmallIntegerField(null=False)
    seats_left = models.PositiveIntegerField(default=0)
    gform_link = models.URLField(max_length=200, null=False)
    is_link_active = models.BooleanField(default=True)
    last_date_to_apply = models.DateField(default=get_deadline)
    entries = GenericRelation(FormStatusSet)
    datetime = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return str(self.uuid)        
        
    class Meta:
        unique_together = (('source_id', 'course'),)
        verbose_name = 'PrivateTuition Form'
        verbose_name_plural = 'PrivateTuition Forms'
        
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.uuid = get_form_id('PT')
            super(PTSet, self).save(*args, **kwargs)

class SHSet(models.Model):
    def toJSON(self):
        exclusion = ['id', 'source_id', 'entries']
        json_dict = {}
        for field in self._meta.fields:
            if field.name not in exclusion:
                json_dict[field.name] = getattr(self, field.name)
    
        return json_dict
    
    source_id = models.ForeignKey(SourceSet, on_delete=models.PROTECT)
    uuid = models.CharField(max_length=40, unique=True, editable=False)
    till_class = models.CharField(max_length=10, null=False)
    fee = models.PositiveIntegerField(null=False)
    fee_type = models.CharField(max_length=2, choices=FEE_TYPE_CHOICES)
    timing = models.CharField(max_length=150, null=False)
    seats_left = models.CharField(max_length=100, null=True)   #in each class
    gform_link = models.URLField(max_length=200, null=False)
    is_link_active = models.BooleanField(default=True)
    last_date_to_apply = models.DateField(default=get_deadline)
    entries = GenericRelation(FormStatusSet)
    datetime = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return str(self.uuid)        
        
    class Meta:
        unique_together = (('source_id', 'till_class'),)
        verbose_name = 'School Form'
        verbose_name_plural = 'School Forms'
        
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.uuid = get_form_id('SH')
            super(SHSet, self).save(*args, **kwargs)
    
class CLSet(models.Model):
    def toJSON(self):
        exclusion = ['id', 'source_id', 'entries']
        json_dict = {}
        for field in self._meta.fields:
            if field.name not in exclusion:
                json_dict[field.name] = getattr(self, field.name)
    
        return json_dict
    
    source_id = models.ForeignKey(SourceSet, on_delete=models.PROTECT)
    uuid = models.CharField(max_length=40, unique=True, editable=False)
    course = models.CharField(max_length=100, null=False)
    fee = models.PositiveIntegerField(null=False)
    fee_type = models.CharField(max_length=2, choices=FEE_TYPE_CHOICES)
    timing = models.CharField(max_length=150, null=False)
    seats_left = models.PositiveIntegerField(default=0)
    gform_link = models.URLField(max_length=200, null=False)
    is_link_active = models.BooleanField(default=True)
    last_date_to_apply = models.DateField(default=get_deadline)
    entries = GenericRelation(FormStatusSet)
    datetime = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return str(self.uuid)
        
    class Meta:
        unique_together = (('source_id', 'course'),)
        verbose_name = 'College Form'
        verbose_name_plural = 'College Forms'
        
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.uuid = get_form_id('CL')
            super(CLSet, self).save(*args, **kwargs)

class CCSet(models.Model):
    def toJSON(self):
        exclusion = ['id', 'source_id', 'entries']
        json_dict = {}
        for field in self._meta.fields:
            if field.name not in exclusion:
                json_dict[field.name] = getattr(self, field.name)
    
        return json_dict
    
    source_id = models.ForeignKey(SourceSet, on_delete=models.PROTECT)
    uuid = models.CharField(max_length=40, unique=True, editable=False)
    course = models.CharField(max_length=100, null=False)
    fee = models.PositiveIntegerField(null=False)
    fee_type = models.CharField(max_length=2, choices=FEE_TYPE_CHOICES)
    timing = models.CharField(max_length=150, null=False)
    number_of_batches = models.PositiveSmallIntegerField(null=True)
    seats_left = models.PositiveIntegerField(default=0)
    gform_link = models.URLField(max_length=200, null=False)
    is_link_active = models.BooleanField(default=True)
    last_date_to_apply = models.DateField(default=get_deadline)
    entries = GenericRelation(FormStatusSet)
    datetime = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return str(self.uuid)
        
    class Meta:
        unique_together = (('source_id', 'course'),)
        verbose_name = 'CoachingCentre Form'
        verbose_name_plural = 'CoachingCentre Forms'
        
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.uuid = get_form_id('CC')
            super(CCSet, self).save(*args, **kwargs)
        