export const webAppName = 'ScholarDiet';
export const authTokenName = 'auth-token-edu-website';
export const UNLIMITED = 99999;

// For user
export const userId = 'user_id';
// tslint:disable-next-line: variable-name
export const is_student = 'is_student_qwersf';
// tslint:disable-next-line: variable-name
export const is_teacher = 'is_teacher_jdlfgd';
// tslint:disable-next-line: variable-name
export const is_staff = 'is_staff_xcvxpd';

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
export const actionContent = 'actionContent';
export const activeCreateCourseView = 'createCourseView';
export const previewActionContent = 'previewActionContent';
export const selectedPreviewContentType = 'selectedPreviewContentType';

// For institue section
export const currentSectionSlug = 'currentSectionSlug';
export const hasSectionPerm = 'hasSectionPerm';

// For license
export const selectedLicenseId = 'selectedLicenseId';

// For Course
export const courseContent = 'courseContent';

// For test
export const testMinDetails = 'testMinDetails';

export const TEST_PERM_TYPE_REVERSE = {
  VIEW_ONLY: 'V',
  ROLE_BASED: 'R'
};

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
    F: 'Female',
    '': 'Unknown'
};

export const GENDER_REVERSE = {
  Others: 'O',
  Male: 'M',
  Female: 'F'
};

export const GENDER_FORM_FIELD_OPTIONS = [
  {value: '', viewValue: 'Unknown'},
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
  // {value: '', viewValue: ''},
  {value: 'E', viewValue: 'Education'},
  // {value: 'A', viewValue: 'Art'},
  // {value: 'M', viewValue: 'Music'},
  // {value: 'D', viewValue: 'Dance'}
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

export const PAYMENT_PORTAL = {
  R: 'RAZORPAY',
};

export const PAYMENT_PORTAL_REVERSE = {
  RAZORPAY: 'R'
};

export const SUBJECT_TYPE = {
  M: 'MANDATORY',
  O: 'OPTIONAL'
};

export const SUBJECT_TYPE_REVERSE = {
  MANDATORY: 'M',
  OPTIONAL: 'O'
};

export const SUBJECT_INTRODUCTION_CONTENT_TYPE = {
  I: 'IMAGE',
  P: 'PDF',
  L: 'LINK'
};

export const SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE = {
  IMAGE: 'I',
  PDF: 'P',
  LINK: 'L'
};


export const STUDY_MATERIAL_VIEW = {
  MI: 'MEET YOUR INSTRUCTOR',
  CO: 'COURSE OVERVIEW'
};

export const STUDY_MATERIAL_VIEW_REVERSE = {
  MEET_YOUR_INSTRUCTOR: 'MI',
  COURSE_OVERVIEW: 'CO'
};

// ********************************************
export const STUDY_MATERIAL_VIEW_TYPES = {
  MODULE_VIEW: 'M',
  TEST_VIEW: 'T'
};

export const STUDY_MODULE_VIEW_TYPES = {
  LECTURE_VIEW: 'L',
  TEST_VIEW: 'T'
};

export const LECTURE_TEXT_TYPES = {
  USE_CASE: 'U',
  OBJECTIVES: 'O'
};

export const LECTURE_LINK_TYPES = {
  ADDITIONAL_READING_LINK: 'A',
  USE_CASES_LINK: 'U'
};

export const LECTURE_INTRODUCTORY_CONTENT_TYPES = {
  LINK: 'L',
  PDF: 'P',
  IMAGE: 'I'
};

export const LECTURE_STUDY_MATERIAL_TYPES = {
  PDF: 'P',
  IMAGE: 'I',
  EXTERNAL_LINK: 'E',
  YOUTUBE_LINK: 'Y',
  LIVE_CLASS: 'L'
};

export const TEST_SCHEDULE_TYPES = {
  SPECIFIC_DATE_AND_TIME: 'DT',
  SPECIFIC_DATE: 'D',
  UNSCHEDULED: 'UN'
};

export const GRADED_TYPES = {
  GRADED: 'G',
  UNGRADED: 'U'
};

export const GRADED_TYPES_REVERSE = {
  G: 'Graded',
  U: 'Ungraded'
};

export const GRADED_TYPE_FORM_FIELD_OPTIONS = [
  {value: 'G', viewValue: 'Graded'},
  {value: 'U', viewValue: 'Ungraded'}
];

export const QUESTION_MODE = {
  TYPED: 'T',
  IMAGE: 'I',
  FILE: 'F'
};

export const QUESTION_MODE_REVERSE = {
  T: 'Typed',
  I: 'Separate Image Upload for each question',
  F: 'File Upload'
};

export const QUESTION_MODE_FORM_FIELD_OPTIONS = [
  {value: 'T', viewValue: 'Typed'},
  {value: 'I', viewValue: 'Image'},
  {value: 'F', viewValue: 'File'},
];

export const ANSWER_MODE = {
  TYPED: 'T',
  FILE: 'F'
};

export const ANSWER_MODE_REVERSE = {
  T: 'Typed',
  F: 'File Upload'
};


export const ANSWER_MODE_FORM_FIELD_OPTIONS = [
  {value: 'T', viewValue: 'Typed'},
  {value: 'F', viewValue: 'File'},
];

export const QUESTIONS_CATEGORY = {
  AUTOCHECK_TYPE: 'A',
  ALL_TYPES: 'Z',
  FILE_UPLOAD_TYPE: 'F'
};

export const QUESTIONS_CATEGORY_FORM_FIELD_OPTIONS = [
  {value: 'A', viewValue: 'Automatic checking type questions'},
  {value: 'Z', viewValue: 'All types of questions'},
  {value: 'F', viewValue: 'File will be uploaded'},
];

export const MONTH_FORM_FIELD_OPTIONS = [
  {value: '0', viewValue: 'January'},
  {value: '1', viewValue: 'February'},
  {value: '2', viewValue: 'March'},
  {value: '3', viewValue: 'April'},
  {value: '4', viewValue: 'May'},
  {value: '5', viewValue: 'June'},
  {value: '6', viewValue: 'July'},
  {value: '7', viewValue: 'August'},
  {value: '8', viewValue: 'September'},
  {value: '9', viewValue: 'October'},
  {value: '10', viewValue: 'November'},
  {value: '11', viewValue: 'December'},
];

export const SUBJECT_ADD_TEST_PLACE = {
  GLOBAL: 'G',
  MODULE: 'M',
  LECTURE: 'L'
};

export const SUBJECT_VIEW_TYPE = {
  MODULE_VIEW: 'M',
  TEST_VIEW: 'T'
};

export const PRODUCT_TYPES = {
  LMS_CMS_EXAM_LIVE_STREAM: 'A',
  DIGITAL_EXAM: 'D',
  LIVE_STREAM: 'L',
  STORAGE: 'S'
};

export const QUESTION_SECTION_VIEW_TYPE = {
  SINGLE_QUESTION: 'S',
  MULTIPLE_QUESTION: 'M'
};

export const QUESTION_SECTION_VIEW_TYPE_FORM_FIELD_OPTIONS = [
  {value: 'S', viewValue: 'Only one question'},
  {value: 'M', viewValue: 'Multiple questions'}
];

export const AUTOCHECK_TYPE_QUESTIONS = {
  MCQ: 'M',
  TRUE_FALSE: 'T',
  SELECT_MULTIPLE_CHOICE: 'C',
  NUMERIC_ANSWER: 'N'
};

export const ALL_TYPE_QUESTIONS = {
  MCQ: 'M',
  TRUE_FALSE: 'T',
  SELECT_MULTIPLE_CHOICE: 'C',
  NUMERIC_ANSWER: 'N',
  ASSERTION: 'A',
  SHORT_ANSWER: 'S',
  DESCRIPTIVE_ANSWER: 'D',
  FILL_IN_THE_BLANK: 'F'
};

export const AUTOCHECK_TYPE_QUESTION_FORM_FIELD_OPTIONS = [
  {value: 'M', viewValue: 'MCQ'},
  {value: 'T', viewValue: 'True / False'},
  {value: 'C', viewValue: 'Select Multiple Choice'},
  {value: 'N', viewValue: 'Numeric Answer'},
];

export const ALL_TYPE_QUESTION_FORM_FIELD_OPTIONS = [
  {value: 'M', viewValue: 'MCQ'},
  {value: 'T', viewValue: 'True / False'},
  {value: 'C', viewValue: 'Select Multiple Choice'},
  {value: 'N', viewValue: 'Numeric Answer'},
  {value: 'A', viewValue: 'Assertion'},
  {value: 'S', viewValue: 'Short Answer'},
  {value: 'D', viewValue: 'Descriptive Answer'},
  {value: 'F', viewValue: 'Fill in the blank'},
];
