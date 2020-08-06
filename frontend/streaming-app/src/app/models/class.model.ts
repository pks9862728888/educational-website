export interface ClassDetailsResponse {
  id?: number;
  name?: string;
  class_slug?: string;
  created_on?: string;
  has_class_perm?: boolean;
}

export interface ClassPermittedUserDetails {
  'id': number;
  'name': string;
  'email': string;
  'inviter_name': string;
  'inviter_email': string;
  'created_on': string;
  'image'?: string;
}
