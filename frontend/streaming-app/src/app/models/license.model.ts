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

export interface InstituteLicenseOrderCreatedResponse {
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

export interface InstituteStorageLicenseOrderCreatedResponse {
  status: string;
  amount: number;
  key_id: string;
  currency: string;
  order_id: string;
  order_details_id: number;
  email: string;
  contact: string;
  no_of_gb: number;
  months: number;
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
  order_pk: number;
  amount: number;
  order_receipt: string;
  payment_date: number;
  start_date: number;
  end_date: number;
  // For common license
  type?: string;
  billing?: string;
  selected_license_id?: number;
  // For storage license
  months?: number;
  no_of_gb?: number;
}

export interface ExpiredLicenseDetails {
  amount: number;
  order_receipt: string;
  payment_date: number;
  start_date: number;
  end_date: number;
  // For common license
  type?: string;
  billing?: string;
  selected_license_id?: number;
  // For storage license
  months?: number;
  no_of_gb?: number;
}

export interface PendingPaymentLicenseDetails {
  order_created_on: number;
  order_pk: number;
  order_receipt: string;
  amount: number;
  // For common license
  selected_license_id?: number;
  type?: string;
  billing?: string;
  // For storage license
  months?: number;
  no_of_gb?: number;
  cost_per_gb?: number;
}

export interface LicenseOrderResponse {
  active_license: ActiveLicenseDetails[];
  expired_license: ExpiredLicenseDetails[];
  pending_payment_license: PendingPaymentLicenseDetails[];
}

export interface StorageLicenseCredentials {
  price: number;
  gst_percent: number;
  min_storage: number;
}

export interface StorageLicenseOrderCredentialsForRetryPayment {
  id: number;
  amount: number;
  price: number;
  gst_percent: number;
  no_of_gb: number;
  months: number;
  order_created_on: number;
  order_receipt: number;
}

export interface CommonLicenseOrderCredentialsForRetryPayment {
  id: number;
  CMS_exists: boolean;
  LMS_exists: boolean;
  amount: number;
  billing: string;
  classroom_limit: number;
  department_limit: number;
  discount_percent: number;
  discussion_forum: boolean;
  gst_percent: number;
  no_of_admin: number;
  no_of_staff: number;
  no_of_student: number;
  no_of_faculty: number;
  no_of_board_of_members: number;
  order_created_on: number;
  order_receipt: string;
  price: number;
  subject_limit: number;
  type: string;
  video_call_max_attendees: number;
  discount_coupon_code?: string;
  discount_rs?: number;
  selected_license_id: number;
}
