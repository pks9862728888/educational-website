export interface SubjectInchargeDetails {
  id?: number;
  email?: string;
  name?: string;
}

export interface InstituteSubjectDetails {
  id: number;
  name: string;
  subject_slug: string;
  type: string;
  created_on: string;
  has_subject_perm: boolean;
  subject_incharges: SubjectInchargeDetails[]
}

export interface SubjectPermittedUserDetails {
  id: number;
  email: string;
  name?: string;
  invitee_id: string;
  inviter_name?: string;
  inviter_email?: string;
  created_on: string;
  image?: string;
}
