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


export interface ViewDetails {
  key: {
    name: string;
    count: number;
    week_1_count?: number;
    week_2_count?: number;
    week_3_count?: number;
    week_4_count?: number;
  }
}


export interface SubjectCourseMinDetails {
  storage: {
    total_storage: number; // In Gb
    storage_used: number;  // In Gb
  };
  view_order: Array<string>;
  view_details: ViewDetails;
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
  target_date?: string;
  title: string;
  uploaded_on: string;
  view: string;
  content_type: string;
  description?: string;
  data: {
    id?: number;
    url?: string;         // For external link
    file?: string;        // For image and video file download
    bit_rate?: number;    // For video file
    duration?: number;
    stream_file?: string;
    error_transcoding?: boolean;
    size?: number;
    can_download?: boolean;
    total_pages?: number; // For pdf
  };
}
