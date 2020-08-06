export interface SectionInchargeDetails {
  id?: number;
  name?: string;
  email?: string;
}

export interface SectionDetailsResponse {
  id?: number;
  name?: string;
  section_slug?: string;
  created_on?: string;
  has_section_perm?: boolean;
  section_incharges?: SectionInchargeDetails[];
}

export interface SectionPermittedUserDetails {
  'id': number;
  'name': string;
  'email': string;
  'invitee_id': number;
  'inviter_name': string;
  'inviter_email': string;
  'created_on': string;
  'image'?: string;
}
