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


export interface InstituteLicenseSelectedResponse {
  'status': string;
  'net_amount': string;
  'selected_license_id': string;
}

export interface InstituteLicenceOrderCreatedResponse {
  status: string;
  amount: number;
  key_id: string;
  currency: string;
  order_id: string;
  order_details_id: string;
  email: string;
  type: string;
}

export interface PaymentSuccessCallbackResponse {
  razorpay_payment_id: string;
  razorpay_order_id: string;
  razorpay_signature: string;
}

export interface PaymentVerificatonResponse {
  status: string;
}
