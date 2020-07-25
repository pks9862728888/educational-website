export interface LicenseDetails {
  'id': string;
  'billing': string;
  'type': string;
  'amount': number;
  'discount_percent': number;
  'storage': number;
  'no_of_admin': number;
  'no_of_staff': number;
  'no_of_faculty': number;
  'no_of_student': number;
  'video_call_max_attendees': number;
  'classroom_limit': number;
  'department_limit': number;
  'subject_limit': number;
  'scheduled_test': boolean;
  'discussion_forum': string;
  'LMS_exists': boolean
}

export interface InstituteLicenseList {
  'monthly_license': LicenseDetails[];
  'yearly_license': LicenseDetails[];
}

export interface InstituteDiscountCouponDetailsResponse {
  'discount_rs': number;
  'active': boolean;
}
