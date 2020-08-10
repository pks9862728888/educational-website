export const webAppName = 'ScholarDiet';
export const authTokenName = 'auth-token-edu-website';
export const UNLIMITED = 99999;

// For user
export const userId = 'user_id';

// For institutes
export const currentInstituteRole = 'currentInstituteRole';
export const currentInstituteSlug = 'currentInstituteSlug';
export const currentInstituteType = 'currentInstituteType';

// For institute Class
export const currentClassSlug = 'currentClassSlug';
export const hasClassPerm = 'hasClassPerm';

// For institute subject
export const currentSubjectSlug = 'currentSubjectSlug';
export const hasSubjectPerm = 'hasSubjectPerm';

// For institue section
export const currentSectionSlug = 'currentSectionSlug';
export const hasSectionPerm = 'hasSectionPerm';

// For license
export const selectedLicenseId = 'selectedLicenseId';
export const purchasedLicenseExists = 'purchasedLicenseExists';
export const paymentComplete = 'paymentComplete';

export const COUNTRY = {
    IN: 'India',
    US: 'USA'
};

export const COUNTRY_REVERSE = {
  India: 'IN',
  USA: 'US'
};

export const COUNTRY_FORM_FIELD_OPTIONS = [
  {value: '', viewValue: ''},
  {value: 'IN', viewValue: 'India'},
  {value: 'US', viewValue: 'USA'},
];

export const GENDER = {
    O: 'Others',
    M: 'Male',
    F: 'Female'
};

export const GENDER_REVERSE = {
  Others: 'O',
  Male: 'M',
  Female: 'F'
};

export const GENDER_FORM_FIELD_OPTIONS = [
  {value: '', viewValue: ''},
  {value: 'M', viewValue: 'Male'},
  {value: 'F', viewValue: 'Female'},
  {value: 'O', viewValue: 'Others'},
];

export const LANGUAGE = {
    EN: 'English',
    HI: 'Hindi',
    BN: 'Bengali'
};

export const LANGUAGE_REVERSE = {
  English: 'EN',
  Hindi: 'HI',
  Bengali: 'BN'
};

export const LANGUAGE_FORM_FIELD_OPTIONS = [
  {value: '', viewValue: ''},
  {value: 'EN', viewValue: 'English'},
  {value: 'HI', viewValue: 'Hindi'},
  {value: 'BN', viewValue: 'Bengali'},
];

export const STATE = {
    AN: 'ANDAMAN AND NICOBAR ISLANDS',
    AP: 'ANDHRA PRADESH',
    AR: 'ARUNACHAL PRADESH',
    AS: 'ASSAM',
    BR: 'BIHAR',
    CH: 'CHANDIGARH',
    CT: 'CHHATTISGARH',
    DN: 'DADRA AND NAGAR HAVELI',
    DD: 'DAMAN AND DIU',
    DL: 'DELHI',
    GA: 'GOA',
    GJ: 'GUJARAT',
    HR: 'HARYANA',
    HP: 'HIMACHAL PRADESH',
    JK: 'JAMMU AND KASHMIR',
    JH: 'JHARKHAND',
    KA: 'KARNATAKA',
    KL: 'KERALA',
    LD: 'LAKSHADWEEP',
    MP: 'MADHYA PRADESH',
    MH: 'MAHARASHTRA',
    MR: 'MANIPUR',
    ML: 'MEGHALAYA',
    MZ: 'MIZORAM',
    NL: 'NAGALAND',
    OR: 'ODISHA',
    PD: 'PONDICHERRY',
    PB: 'PUNJAB',
    RJ: 'RAJASHTAN',
    SK: 'SIKKIM',
    TN: 'TAMIL NADU',
    TG: 'TELANGANA',
    TR: 'TRIPURA',
    UP: 'UTTAR PRADESH',
    UK: 'UTTARAKHAND',
    WB: 'WEST BENGAL'
};

export const STATE_FORM_FIELD_OPTIONS = [
  {value: '', viewValue: ''},
  {value: 'AN', viewValue: 'ANDAMAN AND NICOBAR ISLANDS'},
  {value: 'AP', viewValue: 'ANDHRA PRADESH'},
  {value: 'AR', viewValue: 'ARUNACHAL PRADESH'},
  {value: 'AS', viewValue: 'ASSAM'},
  {value: 'BR', viewValue: 'BIHAR'},
  {value: 'CH', viewValue: 'CHANDIGARH'},
  {value: 'CT', viewValue: 'CHHATTISGARH'},
  {value: 'DN', viewValue: 'DADRA AND NAGAR HAVELI'},
  {value: 'DD', viewValue: 'DAMAN AND DIU'},
  {value: 'DL', viewValue: 'DELHI'},
  {value: 'GA', viewValue: 'GOA'},
  {value: 'GJ', viewValue: 'GUJARAT'},
  {value: 'HR', viewValue: 'HARYANA'},
  {value: 'HP', viewValue: 'HIMACHAL PRADESH'},
  {value: 'JK', viewValue: 'JAMMU AND KASHMIR'},
  {value: 'JH', viewValue: 'JHARKHAND'},
  {value: 'KA', viewValue: 'KARNATAKA'},
  {value: 'KL', viewValue: 'KERALA'},
  {value: 'LD', viewValue: 'LAKSHADWEEP'},
  {value: 'MP', viewValue: 'MADHYA PRADESH'},
  {value: 'MH', viewValue: 'MAHARASHTRA'},
  {value: 'MR', viewValue: 'MANIPUR'},
  {value: 'ML', viewValue: 'MEGHALAYA'},
  {value: 'MZ', viewValue: 'MIZORAM'},
  {value: 'NL', viewValue: 'NAGALAND'},
  {value: 'OR', viewValue: 'ODISHA'},
  {value: 'PD', viewValue: 'PONDICHERRY'},
  {value: 'PB', viewValue: 'PUNJAB'},
  {value: 'SK', viewValue: 'SIKKIM'},
  {value: 'TN', viewValue: 'TAMIL NADU'},
  {value: 'TG', viewValue: 'TELANGANA'},
  {value: 'TR', viewValue: 'TRIPURA'},
  {value: 'UP', viewValue: 'UTTAR PRADESH'},
  {value: 'UK', viewValue: 'UTTARAKHAND'},
  {value: 'WB', viewValue: 'WEST BENGAL'},
];

export const INSTITUTE_CATEGORY = {
  E: 'Education',
  A: 'Art',
  M: 'Music',
  D: 'Dance'
};

export const INSTITUTE_CATEGORY_REVERSE = {
  Education: 'E',
  Art: 'A',
  Music: 'M',
  Dance: 'D'
};

export const INSTITUTE_CATEGORY_FORM_FIELD_OPTIONS = [
  {value: '', viewValue: ''},
  {value: 'E', viewValue: 'Education'},
  {value: 'A', viewValue: 'Art'},
  {value: 'M', viewValue: 'Music'},
  {value: 'D', viewValue: 'Dance'}
];

export const INSTITUTE_TYPE = {
  SC: 'School',
  CO: 'College',
  CC: 'Coaching',
};

export const INSTITUTE_TYPE_REVERSE = {
  School: 'SC',
  College: 'CO',
  Coaching: 'CC'
};

export const INSTITUTE_TYPE_FORM_FIELD_OPTIONS = [
  {value: '', viewValue: ''},
  {value: 'SC', viewValue: 'School'},
  {value: 'CO', viewValue: 'College'},
  {value: 'CC', viewValue: 'Coaching'}
];

export const INSTITUTE_ROLE = {
  A: 'Admin',
  S: 'Staff',
  F: 'Faculty'
};

export const INSTITUTE_ROLE_REVERSE = {
  Admin: 'A',
  Staff: 'S',
  Faculty: 'F'
};

export const BILLING_TERM = {
  M: 'MONTHLY',
  A: 'ANNUALLY'
};

export const BILLING_TERM_REVERSE = {
  MONTHLY: 'M',
  ANNUALLY: 'A',
};

export const INSTITUTE_LICENSE_PLANS = {
  BAS: 'BASIC',
  BUS: 'BUSINESS',
  ENT: 'ENTERPRISE'
};

export const INSTITUTE_LICENSE_PLANS_REVERSE = {
  BASIC: 'BAS',
  BUSINESS: 'BUS',
  ENTERPRISE: 'ENT'
};

export const DISCUSSION_FORUM_PER_ATTENDEES = {
  O: '1 per subject',
  S: 'Custom'
};

export const PAYMENT_PORTAL = {
  R: 'RAZORPAY',
};

export const PAYMENT_PORTAL_REVERSE = {
  RAZORPAY: 'R'
};

export const SUBJECT_TYPE = {
  M: 'MANDATORY',
  O: 'OPTIONAL'
}

export const SUBJECT_TYPE_REVERSE = {
  MANDATORY: 'M',
  OPTIONAL: 'O'
}
