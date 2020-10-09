export interface LicenseDetails {
  id: string;
  billing: string;
  type: string;
  price: number;
  discount_percent: number;
  gst_percent: number;
  no_of_admin: number;
  no_of_staff: number;
  no_of_faculty: number;
  no_of_student: number;
  no_of_board_of_members: number;
  video_call_max_attendees: number;
  classroom_limit: number;
  department_limit: number;
  subject_limit: number;
  digital_test: boolean;
  discussion_forum: string;
  LMS_exists: boolean;
  CMS_exists: boolean;
  discount_coupon?: string;
  discount_rs?: number;
}

export interface InstituteLicenseList {
  monthly_license: LicenseDetails[];
  yearly_license: LicenseDetails[];
}

export interface InstituteDiscountCouponDetailsResponse {
  discount_rs: number;
  active: boolean;
}


export interface InstituteLicenseSelectedResponse {
  status: string;
  net_amount: string;
  selected_license_id: string;
}

export interface InstituteLicenceOrderCreatedResponse {
  status: string;
  amount: number;
  key_id: string;
  currency: string;
  order_id: string;
  order_details_id: string;
  email: string;
  contact: string;
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

export interface ActiveLicenseDetails {
  amount: number;
  order_receipt: string;
  payment_date: number;
  start_date: number;
  end_date: number;
  type: string;
  billing: string;
  selected_license_id: number;
}

export interface ExpiredLicenseDetails {
  amount: number;
  order_receipt: string;
  payment_date: number;
  start_date: number;
  end_date: number;
  type: string;
  billing: string;
  selected_license_id: number;
}

export interface PendingPaymentLicenseDetails {
  order_created_on: number;
  order_pk: number;
  order_receipt: string;
  selected_license_id: number;
  type: string;
  billing: string;
  amount: number;
}

export interface LicenseOrderResponse {
  active_license: ActiveLicenseDetails[];
  expired_license: ExpiredLicenseDetails[];
  pending_payment_license: PendingPaymentLicenseDetails[];
}
