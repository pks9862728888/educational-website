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

export interface SubjectCourseMinDetails {
  total_storage: number; // In Gb
  storage_used: number;  // In Gb
  MI: number;            // Meet your instructor
  CO: number;            // Course overview
};

export interface SubjectCourseViewDetails {
  MI: number;
  CO: number;
}

export interface StorageStatistics {
  total_storage: number;
  storage_used: number;
}

export interface StudyMaterialDetails {
  id: number;
  order: number;
  target_data?: string;
  title: string;
  uploaded_on: string;
  view: string;
  content_type: string;
  data: {
    url?: string;
    file?: string;
    bit_rate?: number;
    duration?: number;
    total_pages?: number;
    size?: number;
  };
}
