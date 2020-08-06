export interface ClassInchargeDetails {
  id?: number;
  name?: string;
  email?: string;
}

export interface ClassDetailsResponse {
  id?: number;
  name?: string;
  class_slug?: string;
  created_on?: string;
  has_class_perm?: boolean;
  class_incharges?: ClassInchargeDetails[]
}

export interface ClassPermittedUserDetails {
  'id': number;
  'name': string;
  'email': string;
  'invitee_id': number;
  'inviter_name': string;
  'inviter_email': string;
  'created_on': string;
  'image'?: string;
}
